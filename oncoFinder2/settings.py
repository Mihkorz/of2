import os


def __module_exists(name):
    return os.path.isfile(os.path.join(os.path.dirname(__file__), name + '.py'))


if __module_exists('settings_secret'):
    # noinspection PyUnresolvedReferences
    from settings_secret import *
else:
    if __module_exists('settings_local'):
        # noinspection PyUnresolvedReferences
        from settings_local import *
    else:
        from settings_default import *
