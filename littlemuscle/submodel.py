# Describing submodels

from .configuration import Configuration
from .message import Message
from .operator import Operator
from .scale import Scale

from abc import ABC, abstractmethod
from enum import Enum, unique
from overrides import overrides
from typing import Any, Dict, Generic, List, Tuple, TypeVar, Union


class Endpoint:
    def __init__(self, operator: Operator, name: str):
        self.operator = operator
        self.name = name


class SubmodelDescription:
    def __init__(self,
            num_spatial_dimensions: int
            ) -> None:
        self.num_spatial_dimensions = num_spatial_dimensions
        self.endpoints = []                     # type: List[Endpoint]
        self.parameters = []                    # type: Dict[str, type]


    def add_endpoint(self, operator: Operator, name: str) -> None:
        endpoint = Endpoint(operator, name)
        self.endpoints.append(endpoint)


class Submodel(ABC):

    @abstractmethod
    def describe(self) -> SubmodelDescription:
        pass


    @abstractmethod
    def initialise_state(self,
            configuration: Configuration,
            initial_event: float,
            input_messages: Dict[str, Message]) -> float:
        pass

    @abstractmethod
    def solve(self,
            event: float,
            input_messages: Dict[str, Message]) -> float:
        """Solve for the given event, based on previous state and input."""
        pass

    @abstractmethod
    def update_boundary_conditions(self,
            event: float, next_event: float,
            input_messages: Dict[str, Message]) -> float:
        """Update boundary conditions at the given event, based on previous state and input."""
        pass

    @abstractmethod
    def observe_intermediate_state(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def observe_final_state(self) -> Dict[str, Any]:
        pass


class TimeDrivenSubmodel(ABC):

    @abstractmethod
    def describe(self) -> SubmodelDescription:
        pass


    @abstractmethod
    def initialise_state(self,
            configuration: Configuration,
            initial_time: float,
            input_messages: Dict[str, Message]
            ) -> None:
        pass

    @abstractmethod
    def solve(self,
            time: float,
            input_messages: Dict[str, Message]
            ) -> None:
        """Solve for the given time, based on previous state and input."""
        pass

    @abstractmethod
    def update_boundary_conditions(self,
            time: float,
            input_messages: Dict[str, Message]) -> None:
        """Update boundary conditions to the given time, based on previous state and input."""
        pass

    @abstractmethod
    def has_converged(self) -> bool:
        pass

    @abstractmethod
    def observe_intermediate_state(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def observe_final_state(self) -> Dict[str, Any]:
        pass
