# webapp debug flag
DEBUG = True

# appstats
ENABLE_APPSTATS = False

# installed apps
APPS = [
    # (r'^/$', 'apps.toppage.application'),
]

# global middleware
MIDDLEWARE = [
    'core.middleware.not_found_middleware',
]

# not found app
NOT_FOUND_APP = 'core.defaultapps.not_found'

MEDIA_URL = '/'



###############################################
# loading development settings(config_local.py)
# describe settings before this
###############################################
def is_development():
    """detect development environment
    """
    import os
    return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
# load local config
if is_development():
    import logging
    logging.info('---- development ----')
    try:
        from config_local import *
    except ImportError:
        logging.warn('---- config_local is not exist. using default config.  ----')
