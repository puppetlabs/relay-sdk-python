from requests_mock import Adapter

from relay_sdk.client import new_session
from relay_sdk.events import Events


class TestEvents:

    def test_emit(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'POST', 'http+api://api/events',
            text='OK',
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request:
                request.json() == {'data': {'foo': 'bar'}},
        )
        Events(new_session(api_url='http://api')).emit({'foo': 'bar'})

    def test_emit_with_key(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'POST', 'http+api://api/events',
            text='OK',
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request:
                request.json() == {'data': {'foo': 'bar'}, 'key': 'key'},
        )
        Events(new_session(api_url='http://api')).emit({'foo': 'bar'}, "key")
