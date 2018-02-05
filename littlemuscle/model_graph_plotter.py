from .edge_type import EdgeType
from .model_execution_graph import ModelExecutionGraph, ModelNode
from .operator import Operator


import matplotlib.pyplot as plt
import networkx as nx

from math import sqrt
from random import uniform
from typing import Dict, Tuple


def plot_model_graph(graph: ModelExecutionGraph) -> None:

    def offset(
            pos: Dict[int, Tuple[float, float]],
            offset: Tuple[float, float]
            ) -> Dict[int, Tuple[float, float]]:
        result = {}
        for key in pos:
            newpos_x = pos[key][0] + offset[0]
            newpos_y = pos[key][1] + offset[1]
            result[key] = (newpos_x, newpos_y)
        return result


    G = graph

    pos = _layout_graph(G)

    nx.draw_networkx_nodes(G, pos)

    # draw step edges
    step_edges = [(u, v)
            for u, v, t in G.edges.data('edge_type')
            if t == EdgeType.STEP]
    nx.draw_networkx_edges(G, pos, edgelist=step_edges, edge_color='g', arrowsize=20)

    # draw message edges
    message_edges = [(u, v)
            for u, v, t in G.edges.data('edge_type')
            if t == EdgeType.MESSAGE]
    nx.draw_networkx_edges(G, pos, edgelist=message_edges, edge_color='r', arrowsize=20)

    # draw restart edges
    state_edges = [(u, v)
            for u, v, t in G.edges.data('edge_type')
            if t == EdgeType.STATE]
    nx.draw_networkx_edges(G, pos, edgelist=state_edges, edge_color='b', arrowsize=20)

    # label nodes
    node_labels = {node: '{}.{}'.format(node.element_name, node.operator.value)
            for node in G}

    nx.draw_networkx_labels(G, offset(pos, (0.0, -0.0)), node_labels)

    # label edges
    edge_from_labels = {(u, v): '{}'.format(data['from_endpoint_name'])
            for u, v, data in G.edges.data(True)
            if (u, v) in message_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_from_labels, label_pos=0.7)

    edge_to_labels = {(u, v): '{}'.format(data['to_endpoint_name'])
            for u, v, data in G.edges.data(True)
            if (u, v) in message_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_to_labels, label_pos=0.3)

    plt.axis('off')
    plt.show()


def _layout_graph(graph: ModelExecutionGraph) -> Dict[int, Tuple[float, float]]:
    elements = list({node.element_name for node in graph})

    el_pos = [[uniform(-1.0, 1.0), uniform(-1.0, 1.0)] for element in elements]

    # force-equilibrate to get good spacing
    ref_dist = 0.1
    step_size = 0.1

    converged = False
    while not converged:
        force = []
        for e, element in enumerate(elements):
            force.append([0.0, 0.0])
            for n, neighbour in enumerate(elements):
                if e != n:
                    dx = el_pos[n][0] - el_pos[e][0]
                    dy = el_pos[n][1] - el_pos[e][1]
                    dist = sqrt(dx * dx + dy * dy)
                    strength = dist - ref_dist
                    force[e][0] += (el_pos[n][0] - el_pos[e][1]) * strength
                    force[e][1] += (el_pos[n][1] - el_pos[e][1]) * strength

        sum_forces = 0.0
        for e, element in enumerate(elements):
            el_pos[e][0] += force[e][0] * step_size
            el_pos[e][1] += force[e][1] * step_size

            f0 = force[e][0]
            f1 = force[e][1]
            f = sqrt(f0 * f0 + f1 * f1)
            sum_forces += f

        converged = sum_forces < 0.01

    # lay out fixed relative operator positions
    operator_pos = {
            Operator.F_INIT: (-0.02, 0.05),
            Operator.O_I: (0.0, 0.02),
            Operator.S: (0.01, 0.0),
            Operator.B: (-0.01, -0.02),
            Operator.O_F: (-0.02, -0.05)
            }

    pos = dict()
    for node in graph:
        element_index = elements.index(node.element_name)
        pos[node] = (el_pos[element_index][0] + operator_pos[node.operator][0],
                el_pos[element_index][1] + operator_pos[node.operator][1])

    return pos
