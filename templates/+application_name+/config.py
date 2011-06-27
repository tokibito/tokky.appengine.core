# webapp debug flag
DEBUG = True

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