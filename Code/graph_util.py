import math

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


def total_node_value(graph):
    """
    :param graph: the graph
    :return: number of people remaining to be saved
    """
    return sum(node[1]['value'] for node in graph.nodes.data())


def set_node_value(graph, node, value):
    graph.nodes[node]['value'] = value


def graph_to_node_value_list(graph):
    value_list = [0] * graph.number_of_nodes()
    for i in graph.nodes:
        value_list[i] = graph.nodes[i]['value']
    return value_list


def get_node_value(graph, node):
    return graph.nodes[node]['value']


def gas_node_value(graph, node, value):
    # Get and set
    prev_value = graph.nodes[node]['value']
    graph.nodes[node]['value'] = value
    return prev_value


def remove_edge(graph, nid1, nid2):
    graph.remove_edge(nid1, nid2)


def get_edge_weight(graph, nid1, nid2):
    return graph[nid1][nid2]['weight']


def get_neighbours(graph, node):
    return [n for n in graph.neighbors(node)]


def get_num_positive_nodes(graph):
    """
    :param graph: The graph
    :return: The number of nodes with people in them
    """
    return len([n for n in graph.nodes(data=True) if n[1]['value'] > 0])


def get_num_positive_nodes_excluding_current(graph, currnode):
    """
    :param graph: The graph
    :return: The number of nodes with people in them excluding current
    """
    return get_num_positive_nodes(graph) - (graph.nodes[currnode]['value'] > 0)


def get_minimum_edge_neighbour(graph, node):
    """
    :param graph: The graph
    :param node: Current node to search from
    :return: The neighbouring node with the minimal weight from the current node
    """
    neighbors_edges_dict = graph[node]
    if len(neighbors_edges_dict) == 0:
        return -1
    mindest = None
    minweight = math.inf
    for dest in neighbors_edges_dict:
        weight = neighbors_edges_dict[dest]["weight"]
        if mindest is None:
            mindest = dest
            minweight = weight
        else:
            if weight < minweight:
                mindest = dest
                minweight = weight
            elif weight == minweight:
                # Prefer lower numbered nodes
                if neighbors_edges_dict[dest]["eid"] < neighbors_edges_dict[mindest]["eid"]:
                    mindest = dest
                    minweight = weight
    return mindest


def get_min_path_value_to_people(graph, currnode):
    if get_num_positive_nodes(graph) == 0:  # If goal return 0
        return 0
    # If the node has people, return 0 (as the path to people is to stay in the node)
    if graph.nodes[currnode]['value'] > 0:
        return 0
    paths_value = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(graph, currnode)[0]
    min_value = math.inf
    for n in paths_value:
        if n != currnode and graph.nodes[n]['value'] > 0:
            if paths_value[n] < min_value:
                min_value = paths_value[n]
    return min_value


def print_graph(graph):
    for n in range(graph.number_of_nodes()):
        print(f'{n}v{graph.nodes[n]["value"]}= ', end="")
        print(', '.join(
            f'{neighbour}:e{graph[n][neighbour]["eid"]}w{graph[n][neighbour]["weight"]}' for neighbour in graph[n]))


def get_min_path_to_people(graph, currnode):
    if get_num_positive_nodes_excluding_current(graph, currnode) == 0:
        return []
    paths_values, paths = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(graph, currnode)
    min_path_value = math.inf
    min_path = []
    for i in range(graph.number_of_nodes()):
        if i != currnode and graph.nodes[i]['value'] > 0:
            if paths_values[i] < min_path_value:
                min_path_value = paths_values[i]
                min_path = paths[i]
            elif paths_values[i] == min_path_value:
                if i < min_path[-1]:
                    min_path_value = paths_values[i]
                    min_path = paths[i]
    return min_path[1:]


def draw_graph(self, tree):
    pos = graphviz_layout(tree, prog="dot")
    plt.clf()
    nx.draw_networkx(tree, pos, with_labels=True, node_size=20)
    edge_labels = nx.get_edge_attributes(tree, 'weight')
    nx.draw_networkx_edge_labels(tree, edge_labels=edge_labels, font_size=5)
    plt.savefig("tree {} call {}.png".format(self.aid, self.num_call))

