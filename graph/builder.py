from abc import ABC, abstractmethod
from typing import Tuple
from .graph import Node, Edge
import csv


class iGraphBuilder(ABC):
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.lines = {}

    @abstractmethod
    def build_components(self) -> Tuple[dict[str, Node], list[Edge]]:
        return self.nodes, self.edges, self.lines


class LondonGraphBuilder(iGraphBuilder):
    def __init__(
        self, stations_file: str, connections_file: str, lines_file: str
    ):
        self.connections_file = connections_file
        self.lines_file = lines_file
        self.stations_file = stations_file
        return super().__init__()

    def __read_station_data(self):

        # open stations file to get station (node) data
        with open(self.stations_file) as csvfile:
            stations = csv.DictReader(csvfile)

            # loop through each station and add as node to graph
            for station in stations:
                station["id"] = int(station["id"])
                station["latitude"] = float(station["latitude"])
                station["longitude"] = float(station["longitude"])
                node = Node(**station)
                self.nodes[station["id"]] = node

    def __read_connection_data(self):

        # open connections file to get connection (edge) data
        with open(self.connections_file) as file:
            connections = csv.DictReader(file)

            # loop through each connection and add as edge to graph
            for connection in connections:
                station1_id, station2_id = int(
                    connection.pop("station1")
                ), int(connection.pop("station2"))
                connection["line"] = int(connection["line"])
                connection["time"] = int(connection["time"])

                edge = Edge(station1_id, station2_id, **connection)
                self.edges.append(edge)

    def __read_line_data(self):
        with open(self.lines_file) as file:
            lines = csv.DictReader(file)

            for line in lines:
                line_number = int(line["line"])
                self.lines[line_number] = (line["name"], line["colour"])

    def build_components(self) -> Tuple[dict[str, Node], list[Edge]]:
        self.__read_station_data()
        self.__read_connection_data()
        self.__read_line_data()

        return super().build_components()
