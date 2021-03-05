import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

from agent import Agent


class MultiplayerAgent(Agent):

    def __init__(self, depth):
        super().__init__()
        self.depth = depth
        self.heuristic = None
        self.vertex_id = 0
        self.num_call = 0

    def get_edge_label(self, curr_state, next_state):
        """
        :param curr_state: Current state
        :param next_state: Successor state
        :return: String representing the action which when taken in current state leads to successor state
        """
        curr_player = curr_state.agent_turn
        curr_loc = curr_state.locations[curr_player][1]
        next_loc = next_state.locations[curr_player][1]
        if next_loc == -1:
            return "T"
        if curr_loc == next_loc:
            return "M"
        else:
            return "C{}".format(next_loc)

    def print_tree(self, tree):
        """
        :param tree: The search tree
        Saves the figure of the tree in the current working directory
        """
        pos = graphviz_layout(tree, prog="dot")
        plt.clf()
        nx.draw_networkx(tree, pos, with_labels=False, node_size=7)
        edge_labels = nx.get_edge_attributes(tree, 'label')
        node_labels = nx.get_node_attributes(tree, 'value')
        nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels, font_size=5)
        nx.draw_networkx_labels(tree, pos, labels=node_labels, font_size=7)
        plt.savefig("tree {} call {}.png".format(self.aid, self.num_call))
