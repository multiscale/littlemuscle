from .configuration import Configuration
from .message import Message
from .model_execution_graph import Inbox, ModelExecutionGraph, ModelNode
from .operator import Operator
from .submodel import Submodel

from typing import Dict


def run_simulation(
        graph: ModelExecutionGraph,
        configurations: Dict[str, Configuration]
        ) -> None:

    for node in graph.nodes():
        if node.operator == Operator.F_INIT:
            node.post_message('', Message(0.0, 0.0, False))

    node = _find_runnable_node(graph)
    while node:
        received_messages = node.take_messages()
        if node.operator == Operator.F_INIT:
            conf = configurations[node.element_name]
            sent_messages = _run_f_init(conf, received_messages, node.implementation)
        elif node.operator == Operator.O_I:
            sent_messages = _run_o_i(received_messages, node.implementation)
        elif node.operator == Operator.S:
            sent_messages = _run_s(received_messages, node.implementation)
        elif node.operator == Operator.B:
            sent_messages = _run_b(received_messages, node.implementation)
        elif node.operator == Operator.O_F:
            sent_messages = _run_o_f(received_messages, node.implementation)

        _deliver_messages(graph, node, sent_messages)
        node = _find_runnable_node(graph)


def _find_runnable_node(graph: ModelExecutionGraph) -> ModelNode:
    for node in graph.nodes():
        if node.inbox_full():
            return node
    return None


def _will_repeat(received_messages: Inbox) -> bool:
    repeat = len(received_messages) > 0

    for _, message in received_messages.items():
        repeat = repeat and message.next_time is not None

    return repeat


def _initial_event(received_messages: Inbox) -> float:
    event = 0.0
    for _, message in received_messages.items():
        event = max(event, message.time)
    return event


def _take_state(received_messages: Inbox) -> (float, float, bool):
    "Returns cur_event, next_event, repeat."
    cur_event = received_messages[''].time
    next_event = received_messages[''].next_time
    repeat = received_messages[''].data
    del(received_messages[''])
    return cur_event, next_event, repeat


def _deliver_messages(graph: ModelExecutionGraph, node: ModelNode, sent_messages: Inbox) -> None:
    for sending_endpoint_name in sent_messages:
        receiver, receiving_endpoint_name = graph.find_receiver(node, sending_endpoint_name)
        receiver.post_message(receiving_endpoint_name, sent_messages[sending_endpoint_name])


def _run_f_init(
        configuration: Configuration,
        received_messages: Inbox,
        implementation: Submodel
        ) -> Inbox:

    _take_state(received_messages)
    repeat = _will_repeat(received_messages)
    cur_event = _initial_event(received_messages)

    next_event = implementation.initialise_state(configuration, cur_event, received_messages)
    return { '__O_I': Message(cur_event, next_event, repeat) }


def _run_o_i(
        received_messages: Inbox,
        implementation: Submodel
        ) -> Inbox:

    cur_event, next_event, repeat = _take_state(received_messages)
    sent_messages = implementation.observe_intermediate_state()
    for endpoint in sent_messages:
        sent_messages[endpoint] = Message(cur_event, next_event, sent_messages[endpoint])
    sent_messages['__S'] = Message(cur_event, next_event, repeat)
    return sent_messages


def _run_s(
        received_messages: Inbox,
        implementation: Submodel
        ) -> Inbox:

    cur_event, next_event, repeat = _take_state(received_messages)
    cur_event = next_event
    next_event = implementation.solve(cur_event, received_messages)
    return { '__B': Message(cur_event, next_event, repeat) }


def _run_b(
        received_messages: Inbox,
        implementation: Submodel
        ) -> Inbox:

    cur_event, next_event, repeat = _take_state(received_messages)
    next_event = implementation.update_boundary_conditions(cur_event, next_event, received_messages)
    if next_event is not None:
        return { '__O_I': Message(cur_event, next_event, repeat) }
    else:
        return { '__O_F': Message(cur_event, next_event, repeat) }


def _run_o_f(
        received_messages: Inbox,
        implementation: Submodel
        ) -> Inbox:

    cur_event, next_event, repeat = _take_state(received_messages)
    sent_messages = implementation.observe_final_state()
    for endpoint in sent_messages:
        sent_messages[endpoint] = Message(cur_event, next_event, sent_messages[endpoint])
    if repeat:
        sent_messages['__F_INIT'] = Message(cur_event, next_event, repeat)
    return sent_messages
