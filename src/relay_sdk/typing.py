"""Local data types"""
from typing import Text, Tuple, Union

HTTPTimeout = Union[float, Tuple[float, float], Tuple[float, None]]
HTTPClientCertificate = Union[
    bytes,
    Text,
    Tuple[Union[bytes, Text], Union[bytes, Text]],
]
