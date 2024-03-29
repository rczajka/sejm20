from __future__ import with_statement # needed for python 2.5
from fabric.api import *
from fabric.contrib import files

import os


# ==========
# = Config =
# ==========
# Globals
env.project_name = 'sejm20'
env.use_south = True

# Servers
def localhost():
    """SSH to localhost (for debugging).

    This will deploy to `test-deployment` in the project dir.

    """
    import os.path
    from getpass import getuser

    env.hosts = ['localhost']
    env.user = getuser()
    env.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test-deployment')
    env.virtualenv = '/usr/bin/virtualenv'
    # This goes to VHost configuration
    env.server_name = 'sejm20.example.com'
    env.server_admin = 'sejm20 <sejm20@sejm20.example.com>'
    # /var/log/apache2/* logs
    env.access_log = 'sejm20.log'
    env.error_log = 'sejm20-errors.log'


# add additional servers here

def production():
    env.hosts = ['vps17942.ovh.net']
    env.user = 'sejm20'
    env.path = '/srv/sejm20'
    env.virtualenv = '/usr/bin/virtualenv'
    env.server_name = 'sejm20.pl'
    env.server_admin = 'Radek Czajka <radek.czajka@gmail.com>'
    env.access_log = 'sejm20.log'
    env.error_log = 'sejm20-errors.log'


servers = [localhost, production]

# =========
# = Tasks =
# =========
def test():
    "Run the test suite and bail out if it fails"
    require('hosts', 'path', provided_by=servers)
    require('python', provided_by=[find_python])
    result = run('cd %(path)s/%(project_name)s; %(python)s manage.py test' % env)

def setup():
    """
    Setup a fresh virtualenv as well as a few useful directories, then run
    a full deployment. virtualenv with pip should be already installed.
    """
    require('hosts', 'path', 'virtualenv', provided_by=servers)

    run('mkdir -p %(path)s; cd %(path)s; %(virtualenv)s ve;' % env, pty=True)
    run('cd %(path)s; mkdir releases; mkdir packages;' % env, pty=True)
    run('cd %(path)s/releases; ln -s . current; ln -s . previous' % env, pty=True)
    upload_default_localsettings()
    deploy()

def deploy():
    """
    Deploy the latest version of the site to the servers,
    install any required third party modules,
    install the virtual host and then restart the webserver
    """

    import time
    env.release = time.strftime('%Y-%m-%dT%H%M')

    upload_tar_from_git()
    find_python()
    upload_wsgi_script()
    upload_vhost_sample()
    install_requirements()
    copy_localsettings()
    symlink_current_release()
    collectstatic()
    migrate()
    restart_webserver()

def deploy_version(version):
    "Specify a specific version to be made live"
    require('hosts', 'path', provided_by=servers)
    env.version = version
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous;', pty=True)
        run('ln -s %(version)s releases/current' % env, pty=True)
    restart_webserver()

def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    require('hosts', 'path', provided_by=servers)
    with cd(env.path):
        run('mv releases/current releases/_previous;', pty=True)
        run('mv releases/previous releases/current;', pty=True)
        run('mv releases/_previous releases/previous;', pty=True)
    restart_webserver()


# =====================================================================
# = Helpers. These are called by other functions rather than directly =
# =====================================================================
def upload_tar_from_git():
    "Create an archive from the current Git branch and upload it"
    print '>>> upload tar from git'
    require('path', provided_by=servers)
    require('release', provided_by=[deploy])
    local('/bin/bash lib/git-archive-all.sh --format tar %(release)s.tar' % env)
    local('gzip %(release)s.tar' % env)
    run('mkdir -p %(path)s/releases/%(release)s' % env, pty=True)
    run('mkdir -p %(path)s/packages' % env, pty=True)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)

def find_python():
    "Finds where virtualenv Python stuff is"
    print ">>> find Python paths"
    require('path', provided_by=servers)
    env.python = '%(path)s/ve/bin/python' % env
    env.pip = '%(path)s/ve/bin/pip' % env
    env.site_packages = run('%(python)s -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"' % env)

def upload_vhost_sample():
    "Create and upload Apache virtual host configuration sample"
    print ">>> upload vhost sample"
    require('path', 'project_name', 'user', provided_by=servers)
    require('access_log', 'error_log', 'server_admin', 'server_name', provided_by=servers)
    require('site_packages', provided_by=[find_python])
    files.upload_template('%(project_name)s.vhost.template' % env, '%(path)s/%(project_name)s.vhost' % env, context=env)

def upload_wsgi_script():
    "Create and upload a wsgi script sample"
    print ">>> upload wsgi script sample"
    require('path', 'project_name', provided_by=servers)
    require('python', 'site_packages', provided_by=[find_python])
    files.upload_template('%(project_name)s.wsgi.template' % env, '%(path)s/%(project_name)s.wsgi' % env, context=env)
    run('chmod ug+x %(path)s/%(project_name)s.wsgi' % env)

def install_requirements():
    "Install the required packages from the requirements file using pip"
    print '>>> install requirements'
    require('path', provided_by=servers)
    require('release', provided_by=[deploy])
    require('pip', provided_by=[find_python])
    run('%(pip)s install -r %(path)s/releases/%(release)s/requirements.txt' % env, pty=True)

def secret_key():
    """Generates a new SECRET_KEY."""
    from random import Random
    import string

    r = Random()
    return "".join(r.choice(string.printable) for i in range(64))

def upload_default_localsettings():
    "Uploads localsettings.py with media paths and stuff"
    print ">>> upload default localsettings.py"
    require('path', provided_by=servers)

    env.secret_key = secret_key()
    files.upload_template('%(project_name)s/localsettings.py.template' % env, '%(path)s/localsettings.py' % env, context=env)

def copy_localsettings():
    "Copy localsettings.py from root directory to release directory (if this file exists)"
    print ">>> copy localsettings"
    require('path', 'project_name', provided_by=servers)
    require('release', provided_by=[deploy])

    with settings(warn_only=True):
        run('cp %(path)s/localsettings.py %(path)s/releases/%(release)s/%(project_name)s' % env)

def symlink_current_release():
    "Symlink our current release"
    print '>>> symlink current release'
    require('path', provided_by=servers)
    require('release', provided_by=[deploy])
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous')
        run('ln -s %(release)s releases/current' % env)

def collectstatic():
    """Runs collectstatic management command from Django staticfiles."""
    print '>>> collectstatic'
    require('path', 'project_name', provided_by=servers)
    require('python', provided_by=[find_python])
    with cd('%(path)s/releases/current/' % env):
        run('%(python)s manage.py collectstatic --noinput' % env, pty=True)

def migrate():
    "Update the database"
    print '>>> migrate'
    require('path', 'project_name', provided_by=servers)
    require('python', provided_by=[find_python])
    with cd('%(path)s/releases/current/' % env):
        run('%(python)s manage.py syncdb --noinput' % env, pty=True)
        if env.use_south:
            run('%(python)s manage.py migrate' % env, pty=True)

def restart_webserver():
    "Restart the web server"
    print '>>> restart webserver'
    require('path', 'project_name', provided_by=servers)
    run('touch %(path)s/%(project_name)s.wsgi' % env)
