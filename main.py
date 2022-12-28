import tkinter as tk
from tkinter import ttk

from graph.builder import LondonGraphBuilder
from graph.graph import Graph
from pathfinders.pathfinders import (
    DijkstrasAlgorithm,
    AStarAlgorithm,
    iPathFinder,
)


graph_builder = LondonGraphBuilder(
    "_dataset/london.stations.csv",
    "_dataset/london.connections.csv",
    "_dataset/london.lines.csv",
)
(
    graph_stations,
    graph_connections,
    graph_lines,
) = graph_builder.build_components()
graph = Graph(graph_stations, graph_connections, graph_lines)


sp_algorithm: iPathFinder = DijkstrasAlgorithm(graph)


def select_sp_algorithm():
    global sp_algorithm
    if sp_algorithm_selection.get() == 1:
        print("now using dijkstras")
        sp_algorithm = DijkstrasAlgorithm(graph)
    elif sp_algorithm_selection.get() == 2:
        print("now using astars")
        sp_algorithm = AStarAlgorithm(graph)


HEIGHT = 800
WIDTH = 1200


DODGER_BLUE = "#3399FF"
GREY = "#808080"
MAGENTA = "#99004C"
ORANGE = "#FF9933"


# init tkinter window
win = tk.Tk()
win.geometry(f"{WIDTH}x{HEIGHT}")

# init tk canvas
c = tk.Canvas(win, width=1200, height=800)
c.pack()

path = []


def path_generator():
    global path

    for val in sp_algorithm.nodes_visited:
        node = graph.nodes[int(val)]
        yield node.get_pos(), int(val)
    global colour
    colour = ORANGE
    for val in sp_algorithm.shortest_path:
        node = graph.nodes[int(val)]
        path.append(str(val))
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
    sp_algorithm.find_path(int(from_station), int(to_station))


def create_circle(x, y, radius, width=0, colour=DODGER_BLUE, tags=None):
    x0 = x - radius
    x1 = x + radius
    y0 = y - radius
    y1 = y + radius
    return c.create_oval(x0, y0, x1, y1, width=width, fill=colour, tags=tags)


# connections between stations
for edge in graph.edges:
    a = graph.nodes[edge.node1].get_pos()
    b = graph.nodes[edge.node2].get_pos()
    c.create_line(a[0], a[1], b[0], b[1], fill=GREY)


# stations
for node in graph.nodes.values():
    create_circle(node.get_pos()[0], node.get_pos()[1], 3)


def run_pathfinder():
    global coord, colour, reset_pressed

    # next value visited using path finder
    try:
        coords, val = next(coord)
        if reset_pressed:
            return
    except Exception:
        global path
        route = " -> ".join(path)
        txt.config(text=f"Route: {route}")
        sp_time_taken.config(text=f"Trip time: {sp_algorithm.total_time}")
        return

    # draw edges relaxed
    for edge in graph.adj[val]:
        a = graph.nodes[edge.node1].get_pos()
        b = graph.nodes[edge.node2].get_pos()
        c.create_line(a[0], a[1], b[0], b[1], fill=colour, width=2, tags="tmp")

    # draw node visited
    create_circle(coords[0], coords[1], 4, colour=colour, tags="tmp")

    # delay before checking next node
    win.after(100, run_pathfinder)


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
    global coord, colour, txt

    from_station_label.config(text=f"Start: \t station {from_var.get()}")
    to_station_label.config(text=f"End: \t station {to_var.get()}")

    colour = MAGENTA
    c.delete("tmp")
    find_path(from_var.get(), to_var.get())
    coord = path_generator()
    txt.config(text="Route: calculating...")
    sp_time_taken.config(text="Trip time: calculating...")
    run_pathfinder()


reset_pressed = False


def reset():
    global reset_pressed
    reset_pressed = True
    from_station.delete(0, tk.END)
    to_station.delete(0, tk.END)
    from_station_label.config(text="")
    to_station_label.config(text="")
    txt.config(text="")
    sp_time_taken.config(text="")
    c.delete("tmp")


find_path_button = tk.Button(win, text="Find path", command=start_path_find)
find_path_button.place(relx=0.7, rely=0.3)

reset_button = tk.Button(win, text="Reset", command=reset)
reset_button.place(relx=0.8, rely=0.3)

sp_time_taken = tk.Label(win, text="")
sp_time_taken.place(relx=0.7, rely=0.7)

txt = tk.Label(win, text="", wraplength=300)
txt.place(relx=0.7, rely=0.75)

from_station_label = tk.Label(text="")
from_station_label.place(relx=0.7, rely=0.6)

to_station_label = tk.Label(text="")
to_station_label.place(relx=0.7, rely=0.65)

# slider current value
current_value = tk.IntVar()

line_data = {line: [] for line in range(1, 14)}

for edge in graph.edges:
    line_data[edge.line].append(edge)


new_things = []


def slider_changed(event):
    global new_things

    val = current_value.get()
    value_label.configure(text=val)
    for thing in new_things:
        c.delete(thing)

    if val == 0:
        return

    for edge in line_data[int(val)]:
        a = graph.nodes[edge.node1].get_pos()
        b = graph.nodes[edge.node2].get_pos()
        colour = graph.lines[int(val)][1]
        thing = c.create_line(
            a[0], a[1], b[0], b[1], fill=f"#{colour}", width=4
        )
        new_things.append(thing)


# label for the slider
slider_label = ttk.Label(win, text="Line (1-13):")
slider_label.place(relx=0.7, rely=0.4)

#  slider
slider = ttk.Scale(
    win,
    from_=0,
    to=13,
    orient="horizontal",
    command=slider_changed,
    variable=current_value,
)

slider.place(relx=0.775, rely=0.4)

# value label
value_label = ttk.Label(win, text=current_value.get())
value_label.place(relx=0.875, rely=0.4)

sp_algorithm_selection_label = tk.Label(win, text="Shortest path algorithm:")
sp_algorithm_selection_label.place(relx=0.7, rely=0.075)
sp_algorithm_selection = tk.IntVar(value=1)
select_dijkstras = tk.Radiobutton(
    win,
    text="Dijkstra's",
    variable=sp_algorithm_selection,
    value=1,
    command=select_sp_algorithm,
)
select_dijkstras.place(relx=0.7, rely=0.1)

select_astar = tk.Radiobutton(
    win,
    text="A-Star",
    variable=sp_algorithm_selection,
    value=2,
    command=select_sp_algorithm,
)
select_astar.place(relx=0.7, rely=0.125)


win.mainloop()
