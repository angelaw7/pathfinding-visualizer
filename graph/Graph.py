class Node:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        return repr(vars(self))

    def get_pos(self):
        return self.longitude, self.latitude


class Edge:
    def __init__(self, node1: str, node2: str, **kwargs):
        self.node1 = node1
        self.node2 = node2
        self.__dict__.update(kwargs)

    def __repr__(self) -> str:
        return repr(vars(self))


class Graph:
    def __init__(self, nodes: dict[str, Node], edges: list[Edge]):
        self.nodes = nodes
        self.edges = edges
        self.adj = {}

        self.__add_nodes_to_adj()
        self.__add_edges_to_adj()

    def __add_nodes_to_adj(self):
        for node in self.nodes:
            self.adj[node] = []

    def __add_edges_to_adj(self):
        for edge in self.edges:
            self.adj[edge.node1].append(edge)
            self.adj[edge.node2].append(edge)

    def __repr__(self):
        return repr(vars(self))
