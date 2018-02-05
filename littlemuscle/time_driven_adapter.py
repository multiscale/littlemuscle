from .configuration import Configuration
from .submodel import Submodel, SubmodelDescription, TimeDrivenSubmodel
from .message import Message

from overrides import overrides
from typing import Any, Dict


class TimeDrivenAdapter(Submodel):
    """Adapts a TimeDrivenSubmodel to the Submodel interface."""

    def __init__(self, adaptee: TimeDrivenSubmodel) -> None:
        self.__adaptee = adaptee
        self.__initial_event = None     # type: float


    @overrides
    def describe(self) -> SubmodelDescription:
        return self.__adaptee.describe()


    @overrides
    def initialise_state(self,
            configuration: Configuration,
            initial_event: float,
            input_messages: Dict[str, Message]
            ) -> float:

        self.__time_scale = configuration.time_scale

        self.__initial_event = initial_event

        next_event = self.__initial_event + self.__time_scale.grain
        if self.__initial_event + self.__time_scale.extent < next_event:
            next_event = None
        self.__adaptee.initialise_state(configuration, initial_event, input_messages)
        return next_event

    @overrides
    def solve(self,
            event: float,
            input_messages: Dict[str, Message]) -> float:

        next_event = event + self.__time_scale.grain
        if self.__initial_event + self.__time_scale.extent < next_event:
            next_event = None
        self.__adaptee.solve(event, input_messages)
        return next_event

    @overrides
    def update_boundary_conditions(self,
            event: float, next_event: float,
            input_messages: Dict[str, Message]) -> float:

        self.__adaptee.update_boundary_conditions(event, input_messages)
        if self.__adaptee.has_converged():
            next_event = None
        return next_event

    @overrides
    def observe_intermediate_state(self) -> Dict[str, Any]:
        return self.__adaptee.observe_intermediate_state()

    @overrides
    def observe_final_state(self) -> Dict[str, Any]:
        return self.__adaptee.observe_final_state()
