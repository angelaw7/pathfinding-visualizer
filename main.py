import pygame
from graph.builder import LondonGraphBuilder
from graph.graph import Graph
from pathfinders.pathfinders import DijkstrasAlgorithm, AStarAlgorithm

graph_builder = LondonGraphBuilder(
    "_dataset/london.stations.csv",
    "_dataset/london.connections.csv",
    "_dataset/london.lines.csv",
)
graph_stations, graph_connections = graph_builder.build_components()
graph = Graph(graph_stations, graph_connections)


dijkstras = DijkstrasAlgorithm(graph)
dijkstras.find_path(77, 155)
print(dijkstras.shortest_path)


pygame.init()

screen = pygame.display.set_mode([800, 800])

running = True


def n():
    for val in dijkstras.shortest_path:
        node = graph.nodes[int(val)]
        yield node.get_pos(), int(val)


x = n()


def convert_coords():
    for node in graph.nodes.values():
        pos = node.get_pos()
        long = ((pos[0] + 0.6) * 800) + 30
        lat = ((pos[1] - 51.4) * 3 * 800) + 30
        graph.nodes[node.id].latitude = lat
        graph.nodes[node.id].longitude = long


convert_coords()
to_draw = []
lines = []

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for node in graph.nodes.values():
        pygame.draw.circle(screen, (0, 0, 255), node.get_pos(), 4)

    for edge in graph.edges:
        pygame.draw.line(
            screen,
            (0, 0, 0),
            graph.nodes[edge.node1].get_pos(),
            graph.nodes[edge.node2].get_pos(),
        )

    try:
        coords, val = next(x)
        to_draw.append(coords)
        lines.append(graph.adj[val])
    except:
        pass

    for item in to_draw:
        pygame.draw.circle(screen, (255, 0, 0), item, 4)

    for item in lines:
        for edge in item:
            pygame.draw.line(
                screen,
                (0, 255, 0),
                graph.nodes[edge.node1].get_pos(),
                graph.nodes[edge.node2].get_pos(),
            )
    print("tick")
    pygame.display.flip()
    pygame.time.wait(1000)

pygame.quit()
