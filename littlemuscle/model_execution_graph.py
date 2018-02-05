from .configuration import Configuration
from .edge_type import EdgeType
from .message import Message
from .model import ComputeElement, Conduit
from .operator import Operator
from .submodel import Endpoint, Submodel

from copy import deepcopy
from enum import Enum
from typing import Dict, Iterator, List, Tuple

import networkx as nx


Inbox = Dict[str, Message]


class ModelNode:
    def __init__(self,
            element_name: str,
            operator: Operator,
            implementation: Submodel,
            empty_inbox: Inbox
            ) -> None:

        super().__init__()

        self.element_name = element_name
        self.operator = operator
        self.implementation = implementation
        self.inbox = deepcopy(empty_inbox)

        self.__empty_inbox = empty_inbox


    def __hash__(self) -> int:
        return hash((self.element_name, self.operator))


    def post_message(self, endpoint: str, message: Message) -> None:
        self.inbox[endpoint] = message


    def inbox_full(self) -> bool:
        for key in self.inbox:
            if self.inbox[key] is None:
                return False
        return True


    def take_messages(self) -> Inbox:
        """Also empties inbox."""
        messages = self.inbox
        self.inbox = deepcopy(self.__empty_inbox)
        return messages


class ModelExecutionGraph(nx.DiGraph):
    def __init__(self,
            compute_elements: List[ComputeElement],
            conduits: List[Conduit]
            ) -> None:

        super().__init__()

        for submodel in compute_elements:
            self.__add_submodel_to_graph(submodel)

        for conduit in conduits:
            self.__add_conduit_to_graph(conduit)


    def find_receiver(self, model_node: ModelNode, endpoint_name: str) -> ModelNode:
        for u, v, data in super().edges(data=True):
            if u == model_node:
                if data['from_endpoint_name'] == endpoint_name:
                    return v, data['to_endpoint_name']


    def __add_submodel_to_graph(self, element: ComputeElement) -> None:
        f_init_node = self.__add_element_node(element, Operator.F_INIT)
        o_i_node = self.__add_element_node(element, Operator.O_I)
        s_node = self.__add_element_node(element, Operator.S)
        b_node = self.__add_element_node(element, Operator.B)
        o_f_node = self.__add_element_node(element, Operator.O_F)

        self.__add_step_edge(f_init_node, o_i_node, '__O_I')
        self.__add_step_edge(o_i_node, s_node, '__S')
        self.__add_step_edge(s_node, b_node, '__B')
        self.__add_step_edge(b_node, o_i_node, '__O_I')
        self.__add_step_edge(b_node, o_f_node, '__O_F')
        self.__add_step_edge(o_f_node, f_init_node, '__F_INIT', EdgeType.STATE)


    def __add_element_node(self, element: ComputeElement, operator: Operator) -> ModelNode:
        empty_inbox = self.__make_empty_inbox(element.endpoints, operator)
        node = ModelNode(element.name, operator, element.implementation, empty_inbox)
        super().add_node(node)
        return node


    def __add_step_edge(self,
            from_node: ModelNode, to_node: ModelNode,
            operator_name: str,
            edge_type: EdgeType = EdgeType.STEP
            ) -> None:

        super().add_edge(from_node, to_node,
                edge_type=edge_type,
                from_endpoint_name=operator_name, to_endpoint_name='')



    def __make_empty_inbox(self, endpoints: List[Endpoint], operator: Operator) -> Inbox:
        inbox = { '': None }

        if operator.may_receive():
            for endpoint in endpoints:
                if endpoint.operator == operator:
                    inbox[endpoint.name] = None
        return inbox


    def __add_conduit_to_graph(self, conduit: Conduit) -> None:
        from_node = self.__find_node_by_endpoint(conduit.from_compute_element, conduit.from_endpoint)
        to_node = self.__find_node_by_endpoint(conduit.to_compute_element, conduit.to_endpoint)
        super().add_edge(from_node, to_node,
                edge_type=EdgeType.MESSAGE,
                from_endpoint_name=conduit.from_endpoint.name,
                to_endpoint_name=conduit.to_endpoint.name)


    def __find_node_by_endpoint(self, element_name: str, endpoint: Endpoint) -> int:
        nodes = [n for n in super().nodes
                if n.element_name == element_name
                and n.operator == endpoint.operator]
        assert len(nodes) == 1
        return nodes[0]
