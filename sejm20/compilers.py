import os.path
from django.conf import settings
from pipeline.compilers.sass import SASSCompiler

class SCSSCompiler(SASSCompiler):
    """Works just like the SASS compiler, but with scss binary."""
    def compile_file(self, content, path):
        command = "%s %s %s" % (
            settings.PIPELINE_SCSS_BINARY,
            settings.PIPELINE_SCSS_ARGUMENTS,
            path,
        )
        cwd = os.path.dirname(path)
        return self.execute_command(command, cwd=cwd)
