"Generating events for the service to act on"
import json
from typing import Any, Dict, Mapping, Optional

from requests import Session

from .util import JSONEncoder


class Events:
    """Class for generating event payloads to the service API"""

    def __init__(self, client: Session) -> None:
        self._client = client

    def emit(self, data: Mapping[str, Any], key: Optional[str] = None) -> None:
        """Sends an event to the service.

        Use this from a Trigger handler to start the workflow
        associated with the trigger.

        Accepts a Mapping of data fields from the request payload
        that came in to the Trigger handler.

        A key can be optionally provided to uniquely identify
        the event."""

        post_data: Dict[str, Any] = {'data': data}
        if key:
            post_data['key'] = key

        r = self._client.post(
            'http+api://api/events',
            data=json.dumps(post_data, cls=JSONEncoder),
            headers={'content-type': 'application/json'},
        )

        r.raise_for_status()
