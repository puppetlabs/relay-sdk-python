"Allows a step to run a workflow"
import json
import logging
from dataclasses import dataclass
from typing import Any, Mapping
from urllib.parse import quote

from requests import Session

from .util import JSONEncoder

logger = logging.getLogger(__name__)


@dataclass
class Run:
    name: str
    run_number: int
    app_url: str


class Workflows:
    """Use Workflows to run a workflow with parameters"""

    def __init__(self, client: Session) -> None:
        self._client = client

    def run(self, name: str,
            parameters: Mapping[str, Any] = {}) -> Run:
        """run starts a workflow with name and parameters
           and returns the Run object.

        Args:
            name: a string containing the name of the workflow
            parameters: an object that can serialize to JSON
        """
        # transform {key:value} dict into {'key': {'value':value}} format
        params = {'parameters': {k: {'value': v}
                                 for k, v in parameters.items()}}
        r = self._client.post(
            'http+api://api/workflows/{0}/run'.format(quote(name)),
            data=json.dumps(params, cls=JSONEncoder),
            headers={'content-type': 'application/json'},
        )
        r.raise_for_status()

        logger.info('Run workflow %s', repr(name))

        return Run(**r.json()['workflow_run'])
