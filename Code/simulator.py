from enum import Enum

import graph_util
from adversarial_agent import AdversarialAgent
from cooperative_agent import CooperativeAgent
from graph_reader import GraphReader
from human_agent import HAgent
from semi_coop_agent import SemiCoopAgent
from state import State


class GameType(Enum):
    ADVERSARIAL = 0
    SEMICOOP = 1
    COOP = 2


class Simulator:
    def __init__(self):
        self.game_type = -1
        self.state = None
        self.agents = []
        self.user_input()

    def run_environment(self):
        self.start_print()
        self.state.update_people_and_scores()
        self.print()

        while True:
            for agent in self.agents:
                observation = agent.observe(self.state)
                action = agent.act(observation)
                self.update_state(action, agent.aid)
            if not self.state.are_all_agents_moving_or_terminated():
                self.print()
            if self.termination():
                break
        self.end_print()

    def update_state(self, action, aid):
        if action[0] != "noop":
            # Move does not advance the player in the edge, but used to mark the edge the agent wants to traverse, it
            # will be updated when we call state.update_moving_agents() which updates all agents
            if action[0] == "move":
                weight = graph_util.get_edge_weight(self.state.graph, action[1], action[2])
                self.state.move_agent(aid, action[1], action[2], weight)
            elif action[0] == "terminate":
                self.state.terminate_agent(aid)
        self.state.advance_turn()
        if aid == len(self.agents) - 1:  # If the last agent has acted, we update the game in one time unit
            self.state.update_moving_agents()
            self.state.advance_time()
            # Do not update if the current time is greater than the deadline (e.g., current time 2, deadline is 2.5, and
            # we advance to 3)
            if self.state.current_time <= self.state.deadline:
                self.state.update_people_and_scores()

    def termination(self):
        return self.state.is_state_terminal()

    def user_input(self):
        print("Insert graph file path:")
        graph, deadline = GraphReader().read(input().replace('"', ''))
        cutoff_depth = int(input("Enter cutoff depth: "))
        gametype = input("Enter game type: ").lower()
        # Add correct agent types
        if gametype in ["0", "a"]:
            self.game_type = GameType.ADVERSARIAL
            self.agents = [AdversarialAgent(cutoff_depth), AdversarialAgent(cutoff_depth)]
        elif gametype in ["1", "s", "sc"]:
            self.game_type = GameType.SEMICOOP
            self.agents = [SemiCoopAgent(cutoff_depth), SemiCoopAgent(cutoff_depth)]
        elif gametype in ["2", "c"]:
            self.game_type = GameType.COOP
            self.agents = [CooperativeAgent(cutoff_depth), CooperativeAgent(cutoff_depth)]
        elif gametype in ["h"]:
            self.agents = [HAgent(), HAgent()]
        else:
            raise ValueError('Game type not recognized')

        locs = [int(input("Starting vertex id for agent 0: ")), int(input("Starting vertex id for agent 1: "))]
        State.graph = graph
        self.state = State(graph_util.graph_to_node_value_list(graph),
                           [[locs[0], locs[0], 0], [locs[1], locs[1], 0]],
                           deadline=deadline)

    def print(self):
        print('-' * 20)
        self.state.print()

    def start_print(self):
        print("STARTING SIMULATION")
        print('-' * 20)

    def end_print(self):
        print('-' * 20)
        print("END OF RUN")
