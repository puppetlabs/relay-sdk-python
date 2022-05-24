from requests_mock import Adapter

from relay_sdk.client import new_session
from relay_sdk.workflows import Workflows


class TestWorkflows:

    def test_run(self, requests_mock: Adapter) -> None:
        requests_mock.register_uri(
            'POST', 'http+api://api/workflows/myworkflow/run',
            json={'workflow_run': {
                'name': 'name', 'run_number': 13, 'app_url': 'url'}
                },
            request_headers={'content-type': 'application/json'},
            additional_matcher=lambda request:
                request.json() == {"parameters": {"foo": {"value": "bar"}}},
        )
        Workflows(new_session(api_url='http://api')
                  ).run('myworkflow', {'foo': 'bar'})
