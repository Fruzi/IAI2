import copy

import graph_util


class State:
    graph = None

    def __init__(self, node_values, agents_locations, deadline=-1, scores=None, current_time=0, agent_turn=0):
        self.node_values = copy.copy(node_values)
        self.current_time = current_time
        self.agent_turn = agent_turn
        self.scores = copy.copy(scores) if scores is not None else [0, 0]
        self.locations = copy.deepcopy(agents_locations)
        self.deadline = deadline

    def expand(self):
        succ_states = []
        if not self.is_state_terminal():  # As long as we are not in a terminal state, we have successors
            # This represents both the moving and termination successor, but if we do have the choice to terminate,
            # we apply it after making sure we can make the choice
            succ_states.append(State(self.node_values, self.locations, self.deadline, self.scores, self.current_time,
                                     self.agent_turn + 1))
            # If the agent is not terminated, and not on an edge, it is on a node and has a decision to make
            if not (self.is_agent_terminated(self.agent_turn) or self.is_agent_moving(self.agent_turn)):
                succ_states[-1].terminate_agent(self.agent_turn)  # The termination option
                currnode = self.locations[self.agent_turn][1]
                for i in self.graph[currnode]:  # For each neighbor of the current node
                    succ_states.append(State(self.node_values, self.locations, self.deadline, self.scores,
                                             self.current_time, self.agent_turn + 1))
                    # By moving the agent with a specified weight, we mark its intention to go on that edge, the other.
                    # This is of course only for the search tree where we consider all options. In reality we do not
                    # know where the other agent wil go until it does the step
                    succ_states[-1].move_agent(self.agent_turn, currnode, i, self.graph[currnode][i]['weight'])
                # Move termination to end of successors
                temp = succ_states[1:]
                temp.append(succ_states[0])
                succ_states = temp
            # We update time and all relevant information to it when we finish a turn (2-plies)
            if self.agent_turn == 1:
                for state in succ_states:
                    state.agent_turn = 0
                    state.advance_time()
                    state.update_moving_agents()
                    # Do not update scores and people if the time unit of the next turn is after the deadline
                    if state.current_time <= state.deadline:
                        state.update_people_and_scores()
        return succ_states

    def advance_time(self, time_units=1):
        self.current_time += time_units

    def get_agent_location(self, aid):
        return self.locations[aid]

    def is_agent_moving(self, aid):
        return self.locations[aid][2] != 0

    def deadline_reached(self):
        return 0 < self.deadline <= self.current_time

    def people_remaining(self):
        return sum(self.node_values)

    def all_agents_terminated(self):
        return all(loc[0] == -1 for loc in self.locations)

    def is_agent_terminated(self, aid):
        return self.locations[aid][0] == -1

    def update_moving_agents(self):
        for i in range(len(self.locations)):
            if self.locations[i][2] > 0:
                self.locations[i][2] -= 1

    def terminate_agent(self, aid):
        self.locations[aid] = [-1, -1, 0]

    def are_all_agents_moving_or_terminated(self):
        return all(loc[2] > 0 or loc[1] == -1 for loc in self.locations)

    def move_agent(self, aid, orig, dest, weight=-1):
        """
        :param aid: Agent id
        :param orig: The starting position of the agent
        :param dest: The destination
        :param weight: The edge weight
        The function sets movement of the agent to a new edge. The -1 in the weight is because we choose the edge we will
        move on and take one step in it at the same turn.
        """
        if weight < 0:
            graph_util.get_edge_weight(State.graph, orig, dest) - 1
        self.locations[aid] = [orig, dest, weight]

    def update_people_and_scores(self):
        for i in range(len(self.locations)):
            if not self.is_agent_moving(i):
                currnode = self.locations[i][1]
                if currnode != -1:
                    self.scores[i] += self.node_values[currnode]
                    self.node_values[currnode] = 0

    def is_state_terminal(self):
        return self.deadline_reached() or self.people_remaining() <= 0 or self.all_agents_terminated()

    def print(self):
        print(f'Current time-step: {self.current_time}')
        print(f"There are {self.people_remaining()} people remaining")
        self.print_graph()
        self.print_agents_locations()

    def print_agents_locations(self):
        for i in range(len(self.locations)):
            if self.locations[i][1] != -1:
                if self.locations[i][2] == 0:
                    print(f"Agent {i} is at node {self.locations[i][1]}")
                else:
                    print(
                        f"Agent {i} is at edge {self.locations[i][0]}-{self.locations[i][1]} with {self.locations[i][2]} steps left")
            else:
                print(f"Agent {i} is terminated")
        print(f'People saved vector: {self.scores}')

    def print_graph(self):
        graph_util.print_graph(self.graph)

    def advance_turn(self):
        self.agent_turn += 1
        if self.agent_turn == len(self.locations):
            self.agent_turn = 0

    def __str__(self):
        return "Locations {}\nagent turn {}\nscores {}".format(self.locations, self.agent_turn, self.scores)
