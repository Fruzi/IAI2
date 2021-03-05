import networkx as nx


class GraphReader:
    def read(self, path):
        with open(path, 'r') as f:
            next(f)
            deadline = float(self.formatline(f.readline())[1])
            graph = nx.Graph()
            reading_vertices = True  # Are we reading vertices or edges
            for line in f:
                line = self.formatline(line)
                if line:  # The line that marks the switch is a blank line
                    if reading_vertices:  # Currently reading the vertices
                        vertexid = int(line[0][1:])
                        if len(line) == 1:  # A vertex without people
                            graph.add_node(vertexid, value=0)
                        else:
                            graph.add_node(vertexid, value=int(line[1][1:]))
                    else:  # Currently reading the edges
                        edgeid = int(line[0][1:])  # Edge id
                        vertex1id = int(line[1])  # First vertex id
                        vertex2id = int(line[2])  # Second vertex id
                        weight = int(line[3][1:])  # Edge weight
                        graph.add_edge(vertex1id, vertex2id, eid=edgeid, weight=weight)
                else:
                    reading_vertices = False
        print(graph)
        return graph, deadline

    def formatline(self, line: str):
        if line.startswith('#'):
            return line[1:].split(';')[0].strip().split()  # Remove the comment if there is one and split into the parts
        else:  # The empty line that marks the switch from vertices to edges
            return ''
