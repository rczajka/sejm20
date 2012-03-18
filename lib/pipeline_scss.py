import os.path
from django.conf import settings
from pipeline.compilers.sass import SASSCompiler

try:
    PIPELINE_SCSS_BINARY = settings.PIPELINE_SCSS_BINARY
except AttributeError:
    PIPELINE_SCSS_BINARY = "/usr/local/bin/pyscss"

try:
    PIPELINE_SCSS_ARGUMENTS = settings.PIPELINE_SCSS_ARGUMENTS
except AttributeError:
    PIPELINE_SCSS_ARGUMENTS = ""

class SCSSCompiler(SASSCompiler):
    """Works just like the SASS compiler, but with scss binary."""
    def compile_file(self, content, path):
        command = "%s %s %s" % (
            PIPELINE_SCSS_BINARY,
            PIPELINE_SCSS_ARGUMENTS,
            path,
        )
        cwd = os.path.dirname(path)
        return self.execute_command(command, cwd=cwd)
