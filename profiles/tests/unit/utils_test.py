import os

from django.conf import settings
from django.core.exceptions import ValidationError
import pytest

from profiles.utils import validate_input_document


class _FileWrapper(object):

    def __init__(self, file_obj):
        self.__file_obj = file_obj

    def __getattr__(self, name):
        if name == '__file_obj':
            return self.__file_obj

        a = getattr(self.__file_obj, name)
        if not issubclass(type(a), type(0)):
            setattr(self, name, a)
        return a


class TestValidateInputDocument(object):

    def test_validate_twice(self):
        fname = os.path.join(settings.APP_RESUORCES_ROOT, 'data_test', 'profiles', 'ALdata_ivan_small.txt')

        with open(fname) as f:
            validate_input_document(f) # once
            validate_input_document(f) # twice

    def test_content_type(self):
        fname = os.path.join(settings.APP_RESUORCES_ROOT, 'data_test', 'profiles', 'ALdata_ivan_small.txt')
        with open(fname) as f:
            wrapper = _FileWrapper(f)
            wrapper.content_type = 'xxx'

            with pytest.raises(ValidationError) as exinfo:
                validate_input_document(wrapper)

            assert 'xxx' in str(exinfo.value)

            wrapper.content_type = 'text/plain'
            validate_input_document(wrapper)

    def test_invalid_symbol(self):
        fname = os.path.join(settings.APP_RESUORCES_ROOT, 'data_test', 'profiles', 'ALdata_ivan_small_invalid_symbol.txt')
        with open(fname) as f:
            with pytest.raises(ValidationError) as exinfo:
                validate_input_document(f)

            assert 'SYMBOL' in str(exinfo)

    def test_invalid_value(self):
        fname = os.path.join(settings.APP_RESUORCES_ROOT, 'data_test', 'profiles', 'ALdata_ivan_small_invalid_value.txt')
        with open(fname) as f:
            with pytest.raises(ValidationError) as exinfo:
                validate_input_document(f)

            assert 'A_1W_L_14_Tumour' in str(exinfo)
