import graph_util
from agent import Agent


class HAgent(Agent):
    """
    This is the human agent from assignment 1 for debugging purposes
    """
    def act(self, observation):
        if observation.is_agent_moving(self.aid):
            return ("noop",)
        currnode = observation.get_agent_location(self.aid)[1]
        neighbors = graph_util.get_neighbours(observation.graph, currnode)
        print(f"Human agent {self.aid}, your neighbouring nodes are: {neighbors}")
        while True:
            dest = input(f"Where do you want to go: ")
            if dest.isnumeric():
                dest = int(dest)
                if dest in neighbors:
                    break
            print("Please enter a valid node id")
        self.num_actions += 1
        return ("move", currnode, dest)
