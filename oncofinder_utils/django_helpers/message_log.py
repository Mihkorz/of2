from django.contrib import messages


class MessageLog(object):
    """
    Wrapper for django.contrib.messages.api.
    To be used in functions that are not aware of request.
    """

    def __init__(self, request):
        self._request = request

    def add_message(self, level, message, extra_tags='', fail_silently=False):
        messages.add_message(self._request, level, message, extra_tags, fail_silently)

    def get_messages(self):
        messages.get_messages(self._request)

    def get_level(self):
        messages.get_level(self._request)

    def set_level(self, level):
        messages.set_level(self._request, level)

    def debug(self, message, extra_tags='', fail_silently=False):
        messages.debug(self._request, message, extra_tags, fail_silently)

    def info(self, message, extra_tags='', fail_silently=False):
        messages.info(self._request, message, extra_tags, fail_silently)

    def success(self, message, extra_tags='', fail_silently=False):
        messages.success(self._request, message, extra_tags, fail_silently)

    def warning(self, message, extra_tags='', fail_silently=False):
        messages.warning(self._request, message, extra_tags, fail_silently)

    def error(self, message, extra_tags='', fail_silently=False):
        messages.error(self._request, message, extra_tags, fail_silently)


class NullLog(object):

    def __init__(self, request):
        pass

    def add_message(self, level, message, extra_tags='', fail_silently=False):
        pass

    def get_messages(self):
        pass

    def get_level(self):
        pass

    def set_level(self, level):
        pass

    def debug(self, message, extra_tags='', fail_silently=False):
        pass

    def info(self, message, extra_tags='', fail_silently=False):
        pass

    def success(self, message, extra_tags='', fail_silently=False):
        pass

    def warning(self, message, extra_tags='', fail_silently=False):
        pass

    def error(self, message, extra_tags='', fail_silently=False):
        pass
