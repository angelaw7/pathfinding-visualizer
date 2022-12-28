import tkinter as tk
from tkinter import ttk

from graph.builder import LondonGraphBuilder
from graph.graph import Graph
from pathfinders.pathfinders import (
    DijkstrasAlgorithm,
    AStarAlgorithm,
    iPathFinder,
)


class Colour:
    DODGER_BLUE = "#3399FF"
    GREY = "#808080"
    MAGENTA = "#99004C"
    ORANGE = "#FF9933"


def create_circle(
    c: tk.Canvas,
    x: float,
    y: float,
    radius: float,
    width: float = 0,
    colour: Colour = Colour.DODGER_BLUE,
    tags: str = None,
):
    """helper function for creating a circle on Tkinter canvas"""
    x0 = x - radius
    x1 = x + radius
    y0 = y - radius
    y1 = y + radius
    return c.create_oval(x0, y0, x1, y1, width=width, fill=colour, tags=tags)


class GUI:
    def __init__(self):
        self.graph = None
        self.HEIGHT = 800
        self.WIDTH = 1200
        self.OPT_W = 0.7
        self.delay = 100

        self.sp = []  # nodes in shortest path

        self.__build_graph()
        self.__convert_coordinates()
        self.__init_tk()
        self.__init_graph_UI()
        self.__init_elements_UI()

    def __build_graph(self):
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
        self.graph = Graph(graph_stations, graph_connections, graph_lines)

        self.sp_algorithm: iPathFinder = DijkstrasAlgorithm(self.graph)

    def __convert_coordinates(self):
        """scale original coordinates to map onto UI frame"""
        for node in self.graph.nodes.values():
            pos = node.get_pos()

            long = ((pos[0] + 0.6) * self.HEIGHT) + 30
            lat = ((pos[1] - 51.4) * 3 * self.HEIGHT) + 30
            self.graph.nodes[node.id].latitude = lat
            self.graph.nodes[node.id].longitude = long

    def __init_tk(self):
        # init tkinter window
        self.win = tk.Tk()
        self.win.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # init tk canvas
        self.c = tk.Canvas(self.win, width=self.WIDTH, height=self.HEIGHT)
        self.c.pack()

    def __init_elements_UI(self):
        # shortest path algorithm selection -----------------------------------
        self.sp_algorithm_selection_label = tk.Label(
            self.win, text="Shortest path algorithm:"
        )
        self.sp_algorithm_selection_label.place(relx=self.OPT_W, rely=0.075)
        self.sp_algorithm_selection = tk.IntVar(value=1)

        # shortest path algorithm - select dijkstras option
        self.select_dijkstras = tk.Radiobutton(
            self.win,
            text="Dijkstra's",
            variable=self.sp_algorithm_selection,
            value=1,
            command=self.__select_sp_algorithm,
        )
        self.select_dijkstras.place(relx=self.OPT_W, rely=0.1)

        # shortest path algorithm - select astar option
        self.select_astar = tk.Radiobutton(
            self.win,
            text="A-Star",
            variable=self.sp_algorithm_selection,
            value=2,
            command=self.__select_sp_algorithm,
        )
        self.select_astar.place(relx=self.OPT_W, rely=0.125)

        # from station input --------------------------------------------------
        self.from_var = tk.StringVar()
        self.from_label = tk.Label(text="Start station:")
        self.from_label.place(relx=self.OPT_W, rely=0.2)
        self.from_entry = tk.Entry(self.win, textvariable=self.from_var, bd=5)
        self.from_entry.place(relx=self.OPT_W + 0.1, rely=0.2)

        # to station input ----------------------------------------------------
        self.to_var = tk.StringVar()
        self.to_label = tk.Label(text="End station:")
        self.to_label.place(relx=self.OPT_W, rely=0.25)
        self.to_entry = tk.Entry(self.win, textvariable=self.to_var, bd=5)
        self.to_entry.place(relx=self.OPT_W + 0.1, rely=0.25)

        self.reset_pressed = False

        # find path button ----------------------------------------------------
        self.find_path_button = tk.Button(
            self.win, text="Find path", command=self.__start_path_find
        )
        self.find_path_button.place(relx=self.OPT_W, rely=0.3)

        # reset button --------------------------------------------------------
        self.reset_button = tk.Button(
            self.win, text="Reset", command=self.__reset
        )
        self.reset_button.place(relx=self.OPT_W + 0.1, rely=0.3)

        # lines selection slider init -----------------------------------------
        self.lines_selection = tk.IntVar()
        self.__init_line_data()
        self.stations_in_line = []

        # lines selection slider label
        self.slider_label = ttk.Label(self.win, text="Line (1-13):")
        self.slider_label.place(relx=self.OPT_W, rely=0.4)

        # lines selection slider
        self.lines_slider = ttk.Scale(
            self.win,
            from_=0,
            to=13,
            orient="horizontal",
            command=self.__slider_changed,
            variable=self.lines_selection,
        )
        self.lines_slider.place(relx=self.OPT_W + 0.075, rely=0.4)

        # lines selection value
        self.lines_value_label = ttk.Label(
            self.win, text=self.lines_selection.get()
        )
        self.lines_value_label.place(relx=self.OPT_W + 0.175, rely=0.4)

        # time taken label ----------------------------------------------------
        self.sp_time_taken_label = tk.Label(self.win, text="")
        self.sp_time_taken_label.place(relx=self.OPT_W, rely=0.7)

        # route label ---------------------------------------------------------
        self.route_label = tk.Label(self.win, text="", wraplength=300)
        self.route_label.place(relx=self.OPT_W, rely=0.75)

        # from station label --------------------------------------------------
        self.from_station_label = tk.Label(text="")
        self.from_station_label.place(relx=self.OPT_W, rely=0.6)

        # to station label ----------------------------------------------------
        self.to_station_label = tk.Label(text="")
        self.to_station_label.place(relx=self.OPT_W, rely=0.65)

    def __init_line_data(self):
        self.line_data = {line: [] for line in range(1, 14)}
        for edge in self.graph.edges:
            self.line_data[edge.line].append(edge)

    def __init_graph_UI(self):
        # connections between stations
        for edge in self.graph.edges:
            a = self.graph.nodes[edge.node1].get_pos()
            b = self.graph.nodes[edge.node2].get_pos()
            self.c.create_line(a[0], a[1], b[0], b[1], fill=Colour.GREY)

        # stations
        for node in self.graph.nodes.values():
            create_circle(self.c, node.get_pos()[0], node.get_pos()[1], 3)

    def __path_generator(self):
        # show nodes that algorithm visits in order
        for val in self.sp_algorithm.nodes_visited:
            node = self.graph.nodes[int(val)]
            yield node.get_pos(), int(val)

        self.colour = Colour.ORANGE  # swap colour to highlight shortest path

        # show nodes in shortest path
        for val in self.sp_algorithm.shortest_path:
            node = self.graph.nodes[int(val)]
            self.sp.append(str(val))
            yield node.get_pos(), int(val)

    def __select_sp_algorithm(self):
        # select dijkstras
        if self.sp_algorithm_selection.get() == 1:
            self.sp_algorithm = DijkstrasAlgorithm(self.graph)

        # select astar
        elif self.sp_algorithm_selection.get() == 2:
            self.sp_algorithm = AStarAlgorithm(self.graph)

    def __start_path_find(self):
        # label for to and from station labels
        self.from_station_label.config(
            text=f"Start: \t station {self.from_var.get()}"
        )
        self.to_station_label.config(
            text=f"End: \t station {self.to_var.get()}"
        )

        # remove previously drawn lines
        self.colour = Colour.MAGENTA
        self.c.delete("tmp")

        # run path finding algorithm
        self.sp_algorithm.find_path(
            int(self.from_var.get()), int(self.to_var.get())
        )

        # create instance of sp generator that generates nodes visited
        self.coord_generator = self.__path_generator()

        # labels for route + trip time
        self.route_label.config(text="Route: calculating...")
        self.sp_time_taken_label.config(text="Trip time: calculating...")

        # animate algorithm on UI
        self.__draw_path()

    def __draw_path(self):
        # next value visited using path finder
        try:
            coords, val = next(self.coord_generator)
            if self.reset_pressed:
                return
        except Exception:
            route = " -> ".join(self.sp)
            self.route_label.config(text=f"Route: {route}")
            self.sp = []
            self.sp_time_taken_label.config(
                text=f"Trip time: {self.sp_algorithm.total_time}"
            )
            return

        # draw edges relaxed
        for edge in self.graph.adj[val]:
            a = self.graph.nodes[edge.node1].get_pos()
            b = self.graph.nodes[edge.node2].get_pos()
            self.c.create_line(
                a[0], a[1], b[0], b[1], fill=self.colour, width=2, tags="tmp"
            )

        # draw node visited
        create_circle(
            self.c, coords[0], coords[1], 4, colour=self.colour, tags="tmp"
        )

        # delay before checking next node
        self.win.after(self.delay, self.__draw_path)

    def __reset(self):
        self.reset_pressed = True
        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
        self.from_station_label.config(text="")
        self.to_station_label.config(text="")
        self.route_label.config(text="")
        self.sp_time_taken_label.config(text="")
        self.c.delete("tmp")

    def __slider_changed(self, event):

        val = self.lines_selection.get()
        self.lines_value_label.configure(text=val)

        for connection in self.stations_in_line:
            self.c.delete(connection)

        if val == 0:  # i.e. no line selected
            return

        for edge in self.line_data[int(val)]:
            a = self.graph.nodes[edge.node1].get_pos()
            b = self.graph.nodes[edge.node2].get_pos()
            colour = self.graph.lines[int(val)][1]
            connection = self.c.create_line(
                a[0], a[1], b[0], b[1], fill=f"#{colour}", width=4
            )
            self.stations_in_line.append(connection)

    def run(self):
        self.win.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
