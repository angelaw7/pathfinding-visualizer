import tkinter as tk
from tkinter import ttk

from graph.builder import LondonGraphBuilder
from graph.graph import Graph
from pathfinders.pathfinders import (
    DijkstrasAlgorithm,
    AStarAlgorithm,
    BFSAlgorithm,
    iPathFinder,
)
from planners.planners import SubwayPatrolPlanning
from styles.colours import Colour
from styles.customtk import Button, create_circle


class GUI:
    def __init__(self):
        self.graph = None
        self.HEIGHT = 800
        self.WIDTH = 1200
        self.OPT_W = 0.7
        self.delay = 1

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

        self.path_algo: iPathFinder = DijkstrasAlgorithm(self.graph)

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
        self.win.title("Pathfinding Visualizer")

        # init tk canvas
        self.c = tk.Canvas(self.win, width=self.WIDTH, height=self.HEIGHT)
        self.c.pack()

    def __init_elements_UI(self):
        # path algorithm selection -----------------------------------
        self.path_algo_selection_label = tk.Label(
            self.win, text="Pathfinding algorithm:"
        )
        self.path_algo_selection_label.place(relx=self.OPT_W, rely=0.075)
        self.path_algo_selection = tk.IntVar(value=1)

        # pathfinding algorithm - select dijkstras option
        self.select_dijkstras = tk.Radiobutton(
            self.win,
            text="Dijkstra's",
            variable=self.path_algo_selection,
            value=1,
            command=self.__select_path_algo,
        )
        self.select_dijkstras.place(relx=self.OPT_W, rely=0.1)

        # pathfinding algorithm - select astar option
        self.select_astar = tk.Radiobutton(
            self.win,
            text="A-Star",
            variable=self.path_algo_selection,
            value=2,
            command=self.__select_path_algo,
        )
        self.select_astar.place(relx=self.OPT_W, rely=0.125)

        # pathfinding algorithm - select BFS option
        self.selectBFS = tk.Radiobutton(
            self.win,
            text="BFS",
            variable=self.path_algo_selection,
            value=3,
            command=self.__select_path_algo,
        )
        self.selectBFS.place(relx=self.OPT_W, rely=0.15)

        # pathfinding algorithm - select BFS option
        self.selectTSP = tk.Radiobutton(
            self.win,
            text="Traveling salesman",
            variable=self.path_algo_selection,
            value=4,
            command=self.__select_path_algo,
        )
        self.selectTSP.place(relx=self.OPT_W, rely=0.175)

        # from station input --------------------------------------------------
        self.from_var = tk.StringVar()
        self.from_label = tk.Label(text="Start station:")
        self.from_label.place(relx=self.OPT_W, rely=0.225)
        self.from_entry = tk.Entry(self.win, textvariable=self.from_var)
        self.from_entry.place(relx=self.OPT_W + 0.08, rely=0.225)

        # to station input ----------------------------------------------------
        self.to_var = tk.StringVar()
        self.to_label = tk.Label(text="End station:")
        self.to_label.place(relx=self.OPT_W, rely=0.25)
        self.to_entry = tk.Entry(self.win, textvariable=self.to_var)
        self.to_entry.place(relx=self.OPT_W + 0.08, rely=0.25)

        self.stations_subset = tk.StringVar()
        self.stations_subset_label = tk.Label(text="Stations:")
        self.stations_subset_entry = tk.Entry(
            self.win, textvariable=self.stations_subset
        )

        self.reset_pressed = False

        # find path button ----------------------------------------------------
        self.find_path_button = Button(
            self.win,
            text="Find path",
            command=self.__start_path_find,
        )
        self.find_path_button.place(relx=self.OPT_W, rely=0.3)

        # reset button --------------------------------------------------------
        self.reset_button = Button(
            self.win,
            text="Reset",
            command=self.__reset,
        )
        self.reset_button.place(relx=self.OPT_W + 0.075, rely=0.3)

        # show lines button ---------------------------------------------------
        self.show_lines_button = Button(
            self.win,
            text="Show lines",
            command=self.__show_lines,
        )
        self.show_lines_button.place(relx=self.OPT_W + 0.125, rely=0.3)
        self.show_lines = False

        # lines selection slider init -----------------------------------------
        self.lines_selection = tk.IntVar()
        self.__init_line_data()
        self.stations_in_line = []

        # lines selection slider label
        self.slider_label = ttk.Label(self.win, text="View line (1-13):")
        self.slider_label.place(relx=self.OPT_W - 0.25, rely=0.08)

        # lines selection slider
        self.lines_slider = ttk.Scale(
            self.win,
            from_=0,
            to=13,
            orient="horizontal",
            command=self.__slider_changed,
            variable=self.lines_selection,
        )
        self.lines_slider.place(relx=self.OPT_W - 0.25 + 0.08, rely=0.08)

        # lines selection value
        self.lines_value_label = ttk.Label(
            self.win, text=self.lines_selection.get()
        )
        self.lines_value_label.place(relx=self.OPT_W - 0.25 + 0.18, rely=0.08)

        # error label --------------------------------------------------
        self.error_label = tk.Label(text="", fg=Colour.RED, wraplength=300)
        self.error_label.place(relx=self.OPT_W, rely=0.35)

        # from station label --------------------------------------------------
        self.from_station_label = tk.Label(text="")
        self.from_station_label.place(relx=self.OPT_W, rely=0.4)

        # to station label ----------------------------------------------------
        self.to_station_label = tk.Label(text="")
        self.to_station_label.place(relx=self.OPT_W, rely=0.425)

        # time taken label ----------------------------------------------------
        self.sp_time_taken_label = tk.Label(self.win, text="")
        self.sp_time_taken_label.place(relx=self.OPT_W, rely=0.475)

        # route label ---------------------------------------------------------
        self.route_label = tk.Label(self.win, text="", wraplength=300)
        self.route_label.place(relx=self.OPT_W, rely=0.525)

        # lines label ---------------------------------------------------------
        self.lines_label = tk.Label(
            self.win, text="", wraplength=300, justify=tk.LEFT
        )
        self.lines_label.place(relx=self.OPT_W, rely=0.6)

    def __init_line_data(self):
        self.line_data = {line: [] for line in range(1, 14)}
        for edge in self.graph.edges:
            self.line_data[edge.line].append(edge)

    def __init_graph_UI(self):
        title = tk.Label(text="London Subway Network")
        title.place(relx=0.025, rely=0.025)

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
        self.tag = "tmp"
        for val in self.path_algo.nodes_visited:
            node = self.graph.nodes[int(val)]
            yield node.get_pos(), int(val)

        # show nodes in shortest path
        self.colour = Colour.ORANGE  # swap colour to highlight shortest path
        prev = None
        for val in self.path_algo.path:
            if str(val) != prev:
                self.sp.append(str(val))
                prev = str(val)
                node = self.graph.nodes[int(val)]
                yield node.get_pos(), int(val)

    def __select_path_algo(self):
        option = self.path_algo_selection.get()

        if option < 4:
            self.stations_subset_label.place_forget()
            self.stations_subset_entry.place_forget()
            self.from_label.place(relx=self.OPT_W, rely=0.225)
            self.from_entry.place(relx=self.OPT_W + 0.08, rely=0.225)
            self.to_label.place(relx=self.OPT_W, rely=0.25)
            self.to_entry.place(relx=self.OPT_W + 0.08, rely=0.25)

        # select dijkstras
        if option == 1:
            self.path_algo = DijkstrasAlgorithm(self.graph)

        # select astar
        elif option == 2:
            self.path_algo = AStarAlgorithm(self.graph)

        # select BFS
        elif option == 3:
            self.path_algo = BFSAlgorithm(self.graph)

        # select traveling salesman
        elif option == 4:
            self.path_algo = SubwayPatrolPlanning(self.graph)
            self.stations_subset_label.place(relx=self.OPT_W, rely=0.225)
            self.stations_subset_entry.place(
                relx=self.OPT_W + 0.08, rely=0.225
            )
            self.to_entry.place_forget()
            self.to_label.place_forget()
            self.from_entry.place_forget()
            self.from_label.place_forget()

    def __start_path_find(self):
        if isinstance(self.path_algo, iPathFinder):
            try:
                from_val = int(self.from_var.get())
                to_val = int(self.to_var.get())
                if (
                    from_val < 1
                    or from_val > 303
                    or to_val < 1
                    or to_val > 303
                ):
                    raise ValueError
            except ValueError:
                self.error_label.config(
                    text="Error: station inputs must be integers between 1-303"
                )
                return
        else:
            try:
                stations = list(
                    map(int, self.stations_subset_entry.get().split(","))
                )
                if min(stations) < 0 or max(stations) > 303:
                    raise ValueError
            except ValueError:
                self.error_label.config(
                    text="Error: invalid subset; "
                    + "stations must be between 1-303 and separated by ','"
                )
                return

        self.__reset(entry=False)

        if isinstance(self.path_algo, iPathFinder):
            # label for to and from station labels
            self.from_station_label.config(
                text=f"Start: \t station {self.from_var.get()}"
            )
            self.to_station_label.config(
                text=f"End: \t station {self.to_var.get()}"
            )
            self.path_algo.find_path(
                int(self.from_var.get()), int(self.to_var.get())
            )
        else:
            self.from_station_label.config(
                text=f"Stations to cover: \t {stations}"
            )
            self.path_algo.find_path(stations)

        # create instance of generator that generates nodes visited
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
            self.__finalize()
            return

        # draw edges relaxed
        for edge in self.graph.adj[val]:
            a = self.graph.nodes[edge.node1].get_pos()
            b = self.graph.nodes[edge.node2].get_pos()
            self.c.create_line(
                a[0],
                a[1],
                b[0],
                b[1],
                fill=self.colour,
                width=2,
                tags=self.tag,
            )

        # draw node visited
        create_circle(
            self.c, coords[0], coords[1], 4, colour=self.colour, tags=self.tag
        )

        # delay before checking next node
        self.win.after(self.delay, self.__draw_path)

    def __finalize(self):
        if isinstance(self.path_algo, iPathFinder):
            self.lines_label.place(relx=self.OPT_W, rely=0.6)
            self.__format_lines()
            route = " -> ".join(self.sp)
        else:
            self.lines_label.place_forget()
            route = ""
            for i in range(len(self.path_algo.total_path)):
                route += f"    - {' -> '.join(self.path_algo.total_path[i])}\n"

        self.route_label.config(text=f"Route: \n{route}")
        self.sp_time_taken_label.config(
            text=f"Trip time: {self.path_algo.total_time}"
        )

        if isinstance(self.path_algo, iPathFinder):
            start = self.from_var.get()
            end = self.to_var.get()
            nodes = [start, end]
        else:
            nodes = list(map(int, self.stations_subset.get().split(",")))

        for node in nodes:
            pos = self.graph.nodes[int(node)].get_pos()
            create_circle(
                self.c,
                pos[0],
                pos[1],
                12,
                width=2,
                tags="tmp",
                colour=Colour.YELLOW,
            )
            self.c.create_text(pos[0], pos[1], text=node, tags="tmp")

    def __reset(self, entry=True):
        self.reset_pressed = True
        self.sp = []
        if entry:
            self.from_entry.delete(0, tk.END)
            self.to_entry.delete(0, tk.END)
        self.error_label.config(text="")
        self.from_station_label.config(text="")
        self.to_station_label.config(text="")
        self.route_label.config(text="", justify=tk.LEFT)
        self.sp_time_taken_label.config(text="")
        self.lines_label.config(text="")
        self.c.delete("tmp")
        self.c.delete("lines")
        self.colour = Colour.MAGENTA
        self.reset_pressed = False

    def __show_lines(self):
        if not self.sp:
            self.error_label.config(text="Error: no path selected")
            return
        if not self.show_lines:
            for edge in self.path_algo.edge_route:
                a = self.graph.nodes[edge.node1].get_pos()
                b = self.graph.nodes[edge.node2].get_pos()
                colour = self.graph.lines[edge.line][1]
                self.c.create_line(
                    a[0],
                    a[1],
                    b[0],
                    b[1],
                    fill=f"#{colour}",
                    tags="lines",
                    width=4,
                )
            self.show_lines_button.config(text="Hide lines")
            self.show_lines = True
        else:
            self.c.delete("lines")
            self.show_lines = False
            self.show_lines_button.config(text="Show lines")

    def __format_lines(self):
        line_label = ""
        station_from = self.sp[0]

        for i in range(1, len(self.sp) - 1):

            if (
                self.path_algo.edge_route[i].line
                != self.path_algo.edge_route[i - 1].line
            ):
                station_to = self.sp[i]
                conn = self.path_algo.edge_route[i - 1]
                line_label += (
                    f"    - line {conn.line} from station"
                    + f" {station_from} to station {station_to}\n"
                )
                station_from = station_to

        if self.path_algo.edge_route[-2] != self.path_algo.edge_route[-1]:
            line_label += (
                f"    - line {self.path_algo.edge_route[-1].line} "
                + f"from station {station_from} to station {self.sp[-1]}\n"
            )

        self.lines_label.config(text=f"Line:\n{line_label}")

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
