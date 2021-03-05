class Agent:
    num_agents = 0

    def __init__(self):
        self.aid = Agent.num_agents
        Agent.num_agents += 1
        self.num_actions = 0

    def act(self, observation):
        return None

    def observe(self, state):
        return state
