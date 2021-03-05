import random


class GraphGenerator:
    def __init__(self):
        self.node_values_sample_list = [0] * 10
        self.node_values_sample_list.extend(i for i in range(1, 11))
        self.edge_values_sample_list = [1] * 5
        self.edge_values_sample_list.extend(i for i in range(2, 6))

    def generate_graph(self, file_path, num_nodes, num_edges, deadline=1):
        if num_edges > num_nodes * (num_nodes - 1) / 2:
            raise ValueError('Too many edges')
        if num_edges < num_nodes - 1:
            raise ValueError('Too few edges, graph must be connected')
        with open(file_path, 'w+') as f:
            f.write(f'#N {num_nodes}\n')
            f.write(f'#D {deadline}\n')
            for i in range(num_nodes):
                node_value = random.choice(self.node_values_sample_list)
                f.write(f'#V{i}')
                if node_value:
                    f.write(f' P{node_value}')
                f.write('\n')
            f.write('\n')
            # The graph must be connected and therefore we create a path between all nodes in random order
            # If there are more edges to count for, they will be sampled from a list containing all pairs instead of
            # randomly picking two nodes to prevent long calculation time (it needs to reroll if edge already existS)
            path_nodes = [i for i in range(num_nodes)]
            random.shuffle(path_nodes)
            edge_count = 0
            possible_edges = self.generate_all_node_pairs(num_nodes)
            for i in range(num_nodes - 1):
                edge = (min(path_nodes[i], path_nodes[i + 1]), max(path_nodes[i], path_nodes[i + 1]))
                f.write(f'#E{edge_count} {edge[0]} {edge[1]} W{random.choice(self.edge_values_sample_list)}\n')
                edge_count += 1
                possible_edges.remove(edge)
            for i in range(num_edges - num_nodes + 1):
                edge = random.choice(possible_edges)
                f.write(f'#E{edge_count} {edge[0]} {edge[1]} W{random.choice(self.edge_values_sample_list)}\n')
                edge_count += 1
                possible_edges.remove(edge)

    def generate_all_node_pairs(self, num_nodes):
        pairs = []
        for i in range(num_nodes):
            pairs.extend((i, j) for j in range(i + 1, num_nodes))
        return pairs


if __name__ == '__main__':
    GraphGenerator().generate_graph(r"C:\Users\Lior\Desktop\f.txt", 10, 25)
