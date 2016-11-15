from settings import *


def app_settings(request):
    return {
        'APP_ENVIRONMENT': APP_ENVIRONMENT,
    }
