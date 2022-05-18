from requests_mock import Adapter

from relay_sdk.client import new_session
from relay_sdk.decorators import Decorators


class TestEvents:

    def test_set_generic(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'POST', 'http+api://api/decorators/test',
            text='OK',
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request:
                request.json() == {'type': 'magic', 'extra': 'foo'},
        )
        Decorators(new_session(api_url='http://api')
                   ).set_generic('magic', 'test', extra='foo')

    def test_set_link(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'POST', 'http+api://api/decorators/test',
            text='OK',
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request:
                request.json() == {
                    'type': 'link',
                    'description': 'Run',
                    'uri': 'https://example.com',
                },
        )
        Decorators(new_session(api_url='http://api')
                   ).set_link('test', 'Run', 'https://example.com')
