from oncofinder_utils.django_helpers import JsonResponse


class TestJsonResponseTest(object):

    def test_empty(self):
        resp = JsonResponse({})
        assert resp.content == '{}'

    def test_basic(self):
        resp = JsonResponse({'a': 1})
        assert resp.content == '{"a": 1}'
