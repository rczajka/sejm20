PIPELINE_CSS = {
    "all": {
        "source_filenames": [
            "css/base.scss",
        ],
        "output_filename": "css/all.?.css",
    }
}

PIPELINE_COMPILERS = (
  'sejm20.compilers.SCSSCompiler',
)
PIPELINE_SCSS_BINARY = '/usr/bin/local/pyscss'
PIPELINE_SCSS_ARGUMENTS = ''
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

# PIPELINE = True
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

