import math

import networkx as nx

from multiplayer_agent import MultiplayerAgent


class AdversarialAgent(MultiplayerAgent):
    def __init__(self, depth):
        super().__init__(depth)
        self.heuristic = adversarial_heuristic

    def act(self, state):
        if state.is_agent_moving(self.aid):
            return ("noop",)
        # Creating a search tree, keep this field to keep track of vertex ids
        self.vertex_id = 0
        tree = nx.DiGraph()
        # Add the root to the tree
        tree.add_node(self.vertex_id, state=state)
        self.vertex_id += 1
        # Populate tree
        self.alphabeta(tree, 0, self.depth, -math.inf, math.inf)
        # self.print_tree(tree)
        self.num_call += 1
        return self.select_best_branch(tree)

    def alphabeta(self, tree, node, depth, alpha, beta, ):
        """
        :param tree: The tree we're constructing
        :param node: The id (int) of the root of the current subtree
        :param depth: Depth of search tree
        :param alpha: Alpha parameter
        :param beta: Beta parameter
        :return: Value of root node
        """
        # Get the state of the root node
        state = tree.nodes[node]['state']
        # If we reached the cutoff we call the static heuristic evaluation function.
        # We also call it if we reached a terminal node because we use the same function for eval and true score
        if depth == 0 or state.is_state_terminal():
            tree.nodes[node]['value'] = self.heuristic(state)
            return self.heuristic(state)
        # Check if max player's turn or min player's turn
        if state.agent_turn == 0:  # Max player
            value = -math.inf  # Value of current node, initially is set to -infinity
            for s in state.expand():
                tree.add_node(self.vertex_id, state=s)
                tree.add_edge(node, self.vertex_id, label=self.get_edge_label(state, s))
                self.vertex_id += 1
                # Value is the maximum between the current value and a successor
                value = max(value, self.alphabeta(tree, self.vertex_id - 1, depth - 1, alpha, beta))
                alpha = max(value, alpha)
                if alpha >= beta:
                    break
            tree.nodes[node]['value'] = value  # Update value
            return value
        else:  # Min player, the same, but with minimum
            value = math.inf
            for s in state.expand():
                tree.add_node(self.vertex_id, state=s)
                tree.add_edge(node, self.vertex_id, label=self.get_edge_label(state, s))
                self.vertex_id += 1
                value = min(value, self.alphabeta(tree, self.vertex_id - 1, depth - 1, alpha, beta))
                beta = min(value, beta)
                if alpha >= beta:
                    break
            tree.nodes[node]['value'] = value
            return value

    def select_best_branch(self, tree):
        curr_loc = tree.nodes[0]['state'].locations[self.aid][1]
        move_to = -1
        if self.aid == 0:  # Max player
            best = -math.inf
            for s in tree.successors(0):
                if tree.nodes[s]['value'] > best:
                    best = tree.nodes[s]['value']
                    move_to = tree.nodes[s]['state'].locations[self.aid][1]
        else:  # Min player
            best = math.inf
            for s in tree.successors(0):
                if tree.nodes[s]['value'] < best:
                    best = tree.nodes[s]['value']
                    move_to = tree.nodes[s]['state'].locations[self.aid][1]
        if move_to != -1:  # Moving to -1 means terminating
            action = ("move", curr_loc, move_to)
        else:
            action = ("terminate",)
        return action


def adversarial_heuristic(state):
    p0_score = state.scores[0]
    p1_score = state.scores[1]
    return p0_score - p1_score
