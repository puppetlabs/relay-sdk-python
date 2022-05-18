import json
from typing import Any, Dict
from urllib.parse import quote

from requests import Session

from .util import JSONEncoder


class Decorators:
    """Manage UI decorators for this step or trigger."""

    def __init__(self, client: Session) -> None:
        self._client = client

    def set_generic(self, type_: str, name: str, **kwargs: Any) -> None:
        """Sets a decorator with the given type and name, attaching any
        additional keyword arguments to the request body."""

        post_data: Dict[str, Any] = dict(kwargs)
        post_data['type'] = type_

        r = self._client.post(
            'http+api://api/decorators/{0}'.format(quote(name)),
            data=json.dumps(post_data, cls=JSONEncoder),
            headers={'content-type': 'application/json'},
        )

        r.raise_for_status()

    def set_link(self, name: str, description: str, uri: str) -> None:
        """Sets a link decorator that will produce a button with the given
        description (label) and link target when rendered."""
        self.set_generic('link', name, description=description, uri=uri)
