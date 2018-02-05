from .operator import Operator
from .submodel import Endpoint, Submodel

from enum import Enum
from typing import List


class Conduit:
    def __init__(self,
            from_compute_element: str,
            from_endpoint: Endpoint,
            to_compute_element: str,
            to_endpoint: Endpoint
            ) -> None:

        self.from_compute_element = from_compute_element
        self.from_endpoint = from_endpoint
        self.to_compute_element = to_compute_element
        self.to_endpoint = to_endpoint


class KindOfComputeElement(Enum):
    SUBMODEL = 'submodel'


class ComputeElement:
    def __init__(self,
            kind: KindOfComputeElement,
            name: str,
            endpoints: List[Endpoint],
            implementation: Submodel
            ) -> None:

        self.kind = kind
        self.name = name
        self.endpoints = endpoints
        self.implementation = implementation
