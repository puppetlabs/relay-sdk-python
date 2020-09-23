"""A SDK for interacting with the relay.sh infrastructure services"""
import logging

from .interface import Dynamic, Interface, UnresolvableException
from .util import (NoTerminationPolicy, SignalTerminationPolicy,
                   SoftTerminationPolicy, TerminationPolicy)
from .webhook import WebhookServer

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    'Dynamic',
    'Interface',
    'UnresolvableException',
    'NoTerminationPolicy',
    'SignalTerminationPolicy',
    'SoftTerminationPolicy',
    'TerminationPolicy',
    'WebhookServer',
]
