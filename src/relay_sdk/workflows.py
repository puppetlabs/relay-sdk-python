"Allows a step to run a workflow"
import json
import logging
from typing import Any
from collections.abc import Mapping
from urllib.parse import quote

from requests import Session

from .util import JSONEncoder

logger = logging.getLogger(__name__)


class Workflows:
    """Use Workflows to run a workflow with parameters"""

    def __init__(self, client: Session) -> None:
        self._client = client

    def run(self, name: str, parameters: Mapping[str, Any] = {}) -> None:
        """run starts a workflow with name and parameters

        Args:
            name: a string containing the name of the workflow
            parameters: an object that can serialize to JSON
        """
        # transform parameters {key:value} dict into {'key': {'value':value}} format
        params = {'parameters': {k: {'value': v}
                                 for k, v in parameters.items()}}
        r = self._client.post(
            'http+api://api/workflows/{0}/run'.format(quote(name)),
            data=json.dumps(params, cls=JSONEncoder),
            headers={'content-type': 'application/json'},
        )
        r.raise_for_status()

        logger.info('Run workflow %s', repr(name))
