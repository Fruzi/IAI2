import math

import networkx as nx

from multiplayer_agent import MultiplayerAgent


class CooperativeAgent(MultiplayerAgent):
    def __init__(self, depth):
        super().__init__(depth)
        self.heuristic = cooperative_heuristic

    def act(self, state):
        if state.is_agent_moving(self.aid):
            return ("noop",)
        self.vertex_id = 0
        tree = nx.DiGraph()
        tree.add_node(self.vertex_id, state=state)
        self.vertex_id += 1
        self.expand_minimax_tree(tree, 0, self.depth)
        self.num_call += 1
        return self.select_best_branch(tree)

    def expand_minimax_tree(self, tree, node, depth):
        """
        :param tree: The tree we're constructing
        :param node: The id (int) of the root of the current subtree
        :param depth: Depth of search tree
        :return: Value of root node
        Both players are trying to maximize the score which is the sum of their scores
        """
        state = tree.nodes[node]['state']
        if depth == 0 or state.is_state_terminal():
            tree.nodes[node]['value'] = self.heuristic(state)
            return self.heuristic(state)
        value = -math.inf
        for s in state.expand():
            tree.add_node(self.vertex_id, state=s)
            tree.add_edge(node, self.vertex_id, label=self.get_edge_label(state, s))
            self.vertex_id += 1
            value = max(value, self.expand_minimax_tree(tree, self.vertex_id - 1, depth - 1))
        tree.nodes[node]['value'] = value
        return value

    def select_best_branch(self, tree):
        curr_loc = tree.nodes[0]['state'].locations[self.aid][1]
        move_to = -1
        best = -math.inf
        for s in tree.successors(0):
            if tree.nodes[s]['value'] > best:
                best = tree.nodes[s]['value']
                move_to = tree.nodes[s]['state'].locations[self.aid][1]
        if move_to != -1:
            action = ("move", curr_loc, move_to)
        else:
            action = ("terminate",)
        return action


def cooperative_heuristic(state):
    p0_score = state.scores[0]
    p1_score = state.scores[1]
    return p0_score + p1_score
