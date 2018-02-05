from .configuration import Configuration
from .message import Message
from .model import ComputeElement, Conduit, Endpoint, KindOfComputeElement
from .model_execution_graph import ModelExecutionGraph
from .model_graph_plotter import plot_model_graph
from .operator import Operator
from .simulation_engine import run_simulation
from .submodel import Scale, Submodel, SubmodelDescription, TimeDrivenSubmodel
from .time_driven_adapter import TimeDrivenAdapter

from typing import List


class Simulation:
    def __init__(self) -> None:
        self.__compute_elements = []    # type: List[ComputeElement]
        self.__conduits = []            # type: List[Conduit]
        self.__configurations = {}       # type: Dict[str, Configuration]


    def add_submodel(self, name: str, submodel: TimeDrivenSubmodel) -> None:
        if isinstance(submodel, TimeDrivenSubmodel):
            submodel = TimeDrivenAdapter(submodel)

        description = submodel.describe()
        new_model = ComputeElement(KindOfComputeElement.SUBMODEL, name, description.endpoints, submodel)
        self.__compute_elements.append(new_model)


    def add_conduit(self,
            from_compute_element: str, from_endpoint: str,
            to_compute_element: str, to_endpoint: str
            ) -> None:

        self.__verify_element_exists(from_compute_element)
        self.__verify_element_exists(to_compute_element)

        from_endpoint = self.__find_endpoint(from_compute_element, from_endpoint)
        to_endpoint = self.__find_endpoint(to_compute_element, to_endpoint)

        new_conduit = Conduit(from_compute_element, from_endpoint, to_compute_element, to_endpoint)
        self.__conduits.append(new_conduit)


    def set_configuration(self, compute_element: str, configuration: Configuration) -> None:
        self.__verify_element_exists(compute_element)
        self.__configurations[compute_element] = configuration


    def run(self) -> None:
        graph = ModelExecutionGraph(self.__compute_elements, self.__conduits)
        plot_model_graph(graph)

        run_simulation(graph, self.__configurations)


    def __verify_element_exists(self, element_name: str) -> None:
        element_names = [e.name for e in self.__compute_elements]
        if element_name not in element_names:
            raise RuntimeError(
                    ('Element with name {} not found').format(element_name))


    def __find_endpoint(self, element_name: str, endpoint_name: str) -> Endpoint:
        for element in self.__compute_elements:
            if element.name != element_name:
                continue
            for endpoint in element.endpoints:
                if endpoint.name == endpoint_name:
                    return endpoint
        raise RuntimeError(
                'Endpoint with name {} not found on element {}'.format(
                    endpoint_name, element_name))
