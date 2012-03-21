import os.path
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, '../media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, '../static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'static/'),
)



PIPELINE_CSS = {
    "all": {
        "source_filenames": [
            "uni_form/uni-form.css",
            "uni_form/default.uni-form.css",
            "css/base.scss",
        ],
        "output_filename": "css/all.css",
    }
}

PIPELINE_JS = {
    "all": {
        "source_filenames": [
            "uni_form/jquery.js",
            "uni_form/uni-form.jquery.js",
        ],
        "output_filename": "js/all.js",
    }
}

PIPELINE_COMPILERS = (
  'pipeline_scss.SCSSCompiler',
)

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
