import math

import networkx as nx

from multiplayer_agent import MultiplayerAgent


class SemiCoopAgent(MultiplayerAgent):
    def __init__(self, depth):
        super().__init__(depth)
        self.heuristic = semi_cooperative_heuristic

    def act(self, state):
        if state.is_agent_moving(self.aid):
            return ("noop",)
        self.vertex_id = 0
        tree = nx.DiGraph()
        tree.add_node(self.vertex_id, state=state)
        self.vertex_id += 1
        self.expand_minmax_tree(tree, 0, self.depth)
        self.num_call += 1
        return self.select_best_branch(tree)

    def expand_minmax_tree(self, tree, node, depth):
        """
        :param tree: The tree we're constructing
        :param node: The id (int) of the root of the current subtree
        :param depth: Depth of search tree
        :return: Value of root node
        Both players are trying to maximize their own score, but they break ties cooperatively.
        """
        state = tree.nodes[node]['state']
        if depth == 0 or state.is_state_terminal():
            tree.nodes[node]['value'] = self.heuristic(state)
            return self.heuristic(state)
        value = [-math.inf, -math.inf]  # Value is an ordered pair of [player0, player1]
        for s in state.expand():
            tree.add_node(self.vertex_id, state=s)
            tree.add_edge(node, self.vertex_id, label=self.get_edge_label(state, s))
            self.vertex_id += 1
            s_value = self.expand_minmax_tree(tree, self.vertex_id - 1, depth - 1)
            # If the successor node has better value than the current value (for all successor nodes), update it. If it
            # is equal, use the tiebreaker
            if s_value[state.agent_turn] > value[state.agent_turn]:
                value = s_value
            elif (s_value[state.agent_turn] == value[state.agent_turn]) and (
                    s_value[1 - state.agent_turn] > value[1 - state.agent_turn]):
                value = s_value
        tree.nodes[node]['value'] = value
        return value

    def select_best_branch(self, tree):
        curr_loc = tree.nodes[0]['state'].locations[self.aid][1]
        move_to = -1
        best = [-math.inf, -math.inf]
        for s in tree.successors(0):
            # Pick best action which maximizes the current player's score, break ties cooperatively
            if tree.nodes[s]['value'][self.aid] > best[self.aid]:
                best = tree.nodes[s]['value']
                move_to = tree.nodes[s]['state'].locations[self.aid][1]
            elif (tree.nodes[s]['value'][self.aid]) == best[self.aid] and (
                    tree.nodes[s]['value'][1 - self.aid] > best[1 - self.aid]):
                best = tree.nodes[s]['value']
                move_to = tree.nodes[s]['state'].locations[self.aid][1]
        if move_to != -1:
            action = ("move", curr_loc, move_to)
        else:
            action = ("terminate",)
        return action


def semi_cooperative_heuristic(state):
    p0_score = state.scores[0]
    p1_score = state.scores[1]
    return [p0_score, p1_score]
