# Import the library
import tkinter as tk
from tkinter import ttk

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


HEIGHT = 800
WIDTH = 1200


DODGER_BLUE = "#3399FF"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = "#808080"
MAGENTA = "#99004C"
PINK = (255, 0, 127)

RADIUS = 4


# Create an instance of tkinter frame
win = tk.Tk()

# Define the geometry of window
win.geometry(f"{WIDTH}x{HEIGHT}")

# Create a canvas object
c = tk.Canvas(win, width=1200, height=800)
c.pack()


def path_generator():
    for val in dijkstras.shortest_path:
        node = graph.nodes[int(val)]
        yield node.get_pos(), int(val)


def convert_coords():
    for node in graph.nodes.values():
        pos = node.get_pos()
        long = ((pos[0] + 0.6) * HEIGHT) + 30
        lat = ((pos[1] - 51.4) * 3 * HEIGHT) + 30
        graph.nodes[node.id].latitude = lat
        graph.nodes[node.id].longitude = long


convert_coords()


def find_path(from_station, to_station):
    dijkstras.find_path(int(from_station), int(to_station))


to_draw = []
lines = []


def create_circle(x, y, radius, width=0, colour=DODGER_BLUE):
    x0 = x - radius
    x1 = x + radius
    y0 = y - radius
    y1 = y + radius
    return c.create_oval(x0, y0, x1, y1, width=width, fill=colour)


# connections between stations
for edge in graph.edges:
    a = graph.nodes[edge.node1].get_pos()
    b = graph.nodes[edge.node2].get_pos()
    c.create_line(a[0], a[1], b[0], b[1], fill=GREY)


# stations
for node in graph.nodes.values():
    create_circle(node.get_pos()[0], node.get_pos()[1], 3)


things_added = []


def loop():
    global coord, things_added

    # next value visited using path finder
    try:
        coords, val = next(coord)
        to_draw.append(coords)
        lines.append(graph.adj[val])
    except:
        print("?")
        return

    for item in lines:
        for edge in item:
            a = graph.nodes[edge.node1].get_pos()
            b = graph.nodes[edge.node2].get_pos()
            thing = c.create_line(
                a[0], a[1], b[0], b[1], fill=MAGENTA, width=2
            )
            things_added.append(thing)

    win.after(500, None)
    for item in to_draw:
        thing = create_circle(item[0], item[1], 4, colour=MAGENTA)
        things_added.append(thing)

    win.after(500, loop)


from_var = tk.StringVar()
from_label = tk.Label(text="Start station:")
from_label.place(relx=0.7, rely=0.2)
from_station = tk.Entry(win, textvariable=from_var, bd=5)
from_station.place(relx=0.8, rely=0.2)

to_var = tk.StringVar()
to_label = tk.Label(text="End station:")
to_label.place(relx=0.7, rely=0.25)
to_station = tk.Entry(win, textvariable=to_var, bd=5)
to_station.place(relx=0.8, rely=0.25)


def start_path_find():
    print(from_var.get())
    print(to_var.get())
    find_path(from_var.get(), to_var.get())
    global coord, things_added
    coord = path_generator()
    c.delete(things_added)
    loop()


button = tk.Button(win, text="Find path", command=start_path_find)
button.place(relx=0.7, rely=0.3)

# slider current value
current_value = tk.IntVar()


def get_current_value():
    return current_value.get()


def slider_changed(event):
    value_label.configure(text=get_current_value())


# label for the slider
slider_label = ttk.Label(win, text="Line (1-13):")

slider_label.place(relx=0.7, rely=0.4)

#  slider
slider = ttk.Scale(
    win,
    from_=1,
    to=13,
    orient="horizontal",
    command=slider_changed,
    variable=current_value,
)

slider.place(relx=0.7, rely=0.45)

# current value label
current_value_label = ttk.Label(win, text="Current Value:")
current_value_label.place(relx=0.7, rely=0.5)

# value label
value_label = ttk.Label(win, text=get_current_value())
value_label.place(relx=0.8, rely=0.5)


win.mainloop()
