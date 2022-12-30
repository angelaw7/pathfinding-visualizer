from graph.graph import Graph
from abc import ABC, abstractmethod
from collections import deque
from graph.graph import Edge
import queue as Q
import sys


class iPathFinder(ABC):
    def __init__(
        self,
        graph: Graph,
        print_solution: bool = True,
    ):
        self.nodes = graph.nodes
        self.adj = graph.adj
        self.pq = Q.PriorityQueue()
        self.edge_to = [""] * (len(self.nodes) + 2)
        self.dist_to = [sys.maxsize] * (len(self.nodes) + 2)

        self.found_end = False
        self.print_solution = print_solution

    def find_path(self, start: int, end: int):
        self.path = []
        self.edge_to = [""] * (len(self.nodes) + 2)
        self.dist_to = [sys.maxsize] * (len(self.nodes) + 2)
        self.end = end
        self.start = start
        self.dist_to[start] = 0
        self.pq.put((0, start))
        self.nodes_visited = []

        return self._find_path()

    def _find_path(self):

        while not (self.pq.empty()):
            _, node = self.pq.get()
            self.nodes_visited.append(node)
            self._relax(node)

            if node == self.end:
                self.found_end = True
                break

        self._format_solution(self.print_solution)
        return self.path

    def _relax(self, node: int):
        edges_connected_to_node = self.adj[node]

        for edge in edges_connected_to_node:

            adjacent_node = self._get_other_node(edge, node)
            weight_of_edge = edge.time

            if (
                self.dist_to[adjacent_node]
                > self.dist_to[node] + weight_of_edge
            ):
                self.dist_to[adjacent_node] = (
                    self.dist_to[node] + weight_of_edge
                )

                self.edge_to[adjacent_node] = edge

                priority = self._get_priority(adjacent_node, node)

                self.pq.put((priority, adjacent_node))

    def _get_other_node(self, edge: Edge, this_node: int) -> int:
        if edge.node1 == this_node:
            return edge.node2
        return edge.node1

    @abstractmethod
    def _get_priority(self, adjacent_node, node):
        pass

    @abstractmethod
    def _get_heuristic(self, adjacent_node, node):
        pass

    def _format_solution(self, print_solution: bool):
        route = [self.end]
        edge = self.edge_to[self.end]
        prev_node = self.end
        edge_route = []

        while edge != "":
            prev_node = self._get_other_node(edge, prev_node)
            edge_route.append(edge)
            edge = self.edge_to[prev_node]
            route.append(prev_node)

        route.reverse()
        edge_route.reverse()
        self.edge_route = edge_route
        self.path = list(map(lambda edge: str(edge), route))
        self.total_time = self.dist_to[self.end]

        if print_solution:
            print(
                f"Start: \t\t Station {self.start}\nDestination: \t Station {self.end}\n"  # noqa
            )
            print("Route: " + " -> ".join(self.path))
            print("Take ", end="")
            station_from = route[0]
            for i in range(1, len(route) - 1):
                if edge_route[i].line != edge_route[i - 1].line:
                    station_to = route[i]
                    conn = edge_route[i - 1]
                    print(
                        f"line {conn.line} from Station {station_from} \
                            to Station {station_to},"
                    )
                    station_from = station_to
            if edge_route[-2] != edge_route[-1]:
                print(
                    f"line {edge_route[-1].line} from Station {station_from} \
                        to Station {route[-1]}.\n"
                )
            print(f"Total trip time: {self.total_time}")


class DijkstrasAlgorithm(iPathFinder):
    def _get_priority(self, adjacent_node: int, node: int) -> float:
        return self.dist_to[adjacent_node]

    def _get_heuristic(self, adjacent_node, node):
        return 0

    def get_num_nodes_visited_before_end(self) -> int:
        return self.nodes_visited_before_end

    def get_num_edges_relaxed_before_end(self) -> int:
        return self.edges_relaxed_before_end

    def get_total_weight(self) -> int:
        return self.dist_to[self.end]


class AStarAlgorithm(iPathFinder):
    def _find_path(self):
        self.end_node = self.nodes[self.end]
        return super()._find_path()

    def _get_priority(self, adjacent_node: int, node: int) -> float:
        return (
            self._get_heuristic(self.nodes[node], self.end_node)
            + self.dist_to[adjacent_node]
        )

    def _get_heuristic(self, start_node: int, end_node: int) -> float:
        node1x, node1y = start_node.latitude, start_node.longitude
        node2x, node2y = end_node.latitude, end_node.longitude
        heuristic = (
            (float(node1x) - float(node2x)) ** 2
            + (float(node1y) - float(node2y)) ** 2
        ) ** 0.5
        return heuristic


class BFSAlgorithm(iPathFinder):
    def _find_path(self):
        self.q = deque([self.start])
        self.visited = [False] * (len(self.nodes) + 2)
        self.visited[self.start] = True

        # deque for which node to visit
        while self.q:
            node = self.q.popleft()
            self.nodes_visited.append(node)

            if node == self.end:  # found destination node
                break

            # check all neighbours of node
            for edge in self.adj[node]:
                neighbour = self._get_other_node(edge, node)

                # add neighbour to queue if not already seen
                if not self.visited[neighbour]:
                    self.q.append(neighbour)
                    self.visited[neighbour] = True
                    self.edge_to[neighbour] = edge
                    self.dist_to[neighbour] = self.dist_to[node] + edge.time

        # format solution and return path
        super()._format_solution(False)
        return self.path

    def _get_heuristic(self, adjacent_node, node):
        return 0

    def _get_priority(self, adjacent_node, node):
        return 0
