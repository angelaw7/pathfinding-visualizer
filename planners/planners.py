from sys import maxsize
from graph.graph import Graph
from pathfinders.pathfinders import DijkstrasAlgorithm


class SubwayPatrolPlanning:
    def __init__(self, graph: Graph):
        self.graph = graph

    def find_path(self, list_of_nodes: list[int]):
        self.list_of_nodes = list_of_nodes
        self.dijkstras = DijkstrasAlgorithm(self.graph)
        self.start = self.list_of_nodes[0]
        self.total_time = maxsize
        self.counter = 0
        self.min_path = None
        self.total_path = []
        self.edge_route = []
        self.nodes_visited = []
        self.path = []

        # run helper function to compute min path
        self._find_min_path()
        self._get_total_min_path()

    def _find_min_path(self):
        self.counter = 0
        self.memo = {}

        # start off the recurive function with the main_source and
        # source being the start node
        self.total_time, self.min_path = self._find_min_path_helper(
            self.start, self.start, self.list_of_nodes, []
        )

        # reverse the min path since it was appended in reverse order
        self.min_path.reverse()
        self.min_path.append(self.start)

    def _find_min_path_helper(
        self, main_source: int, source: int, nodes: list[int], path
    ) -> int:
        # if there is only one node in the list, then return distance
        # back to the source and the min_path as just the node visited
        if len(nodes) == 1:
            min_weight = self._get_weight(source, nodes[0]) + self._get_weight(
                main_source, nodes[0]
            )
            return min_weight, [nodes[0]]

        # otherwise, recursively search through the nodes
        else:
            min_weight = maxsize
            min_path = []

            # iterate through each node in the list
            for node in nodes:

                # make a copy of the nodes list, excluding the node visited
                copy_of_nodes = nodes[:]
                copy_of_nodes.remove(node)

                # recursively call helper function with new list that
                # excludes the node that we just visited
                # this starts building up the shortest path starting with
                # the smaller subsets and adding on new node weight each time
                temp_weight, new_path = self._find_min_path_helper(
                    main_source, node, copy_of_nodes, path
                )
                weight = self._get_weight(source, node) + temp_weight
                new_path.append(node)

                # return the min path and min weight computed
                if weight < min_weight:
                    min_path = new_path
                    min_weight = weight
            return min_weight, min_path

    def _get_weight(self, node1: int, node2: int) -> int:
        # search for the weight in memo and return it if found
        if (node1, node2) in self.memo:
            return self.memo[(node1, node2)]
        elif (node2, node1) in self.memo:
            return self.memo[(node2, node1)]

        # if the weight was not in the memo, then compute shortest path by
        # running dijkstras
        self.counter += 1
        self.dijkstras.find_path(node2, node1)
        self.nodes_visited += self.dijkstras.nodes_visited
        weight = self.dijkstras.get_total_weight()

        # add weight to memo
        self.memo[(node1, node2)] = weight
        return weight

    def _get_total_min_path(self):
        # loop through each node in min_path to find
        # intermediate nodes in the path
        for i in range(1, len(self.min_path)):
            self.dijkstras.find_path(
                self.min_path[i - 1],
                self.min_path[i],
            )
            self.total_path.append(self.dijkstras.path)
            self.path += self.dijkstras.path
            self.edge_route += self.dijkstras.edge_route

    def _print_solution(self):
        print(
            f"Most efficient way to cover subset of nodes \
                {self.list_of_nodes} is the following:"
        )
        print(
            f"- Path: \
                {' -> '.join(map(lambda node: str(node), self.min_path))}"
        )
        print("- Total path:")
        for i in range(len(self.total_path)):
            print(f"\t- Trip {i+1}: ", end="")
            print(f"{' -> '.join(self.total_path[i])}")
        print(f"- Time: {self.total_time}")
