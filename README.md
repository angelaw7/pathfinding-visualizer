# London Subway Network Visualizer

## Table of Contents

- Project Description
- Installation & Usage
- Algorithms

## Project Description

 TLDR: A pathfinding visualizer built using Python's Tkinter library. Good for visualizing how graph algorithms like Dijkstra's, A-Star, and BFS work step-by-step on a graph based on the London subway network.

 There's many other pathfinding visualizers out there but this is one that I created to help strengthen my knowledge of graph algorithms. The goal was not to make a stunning UI, but to have a working interface that does its job of observing how these algorithms perform step by step. I chose to use Python's Tkinter library so that the application stays minimalistic while displaying the graph nodes and edges, along with some pathfinding settings.

## Installation & Usage

1. Clone the repo
```
git clone git@github.com:angelaw7/london-network.git
```

2. Go to project directory
```
cd london-network
```

3. Run the project; this will open the GUI
```
py main.py
```

## Algorithms

1. Dijkstra's Algorithm

Dijkstra's algorithm is used to find the shortest path between two subway stations / nodes. The shortest path is determined by the minimal amount of time to travel between the source and destination stations.

2. A-Star Algorithm

The A-Star algorithm runs similarly to Dijkstra's but also uses a heuristic to guide which node to visit next. The heuristic used for this project was the euclidean distance between two stations, based on their geographical coordinates, as we would expect that choosing the path that gets us closer to the destination station is *usually* a good idea.

3. Breadth First Search

Breadth first search's strengths lie in determining the path with the least connections, rather than the shortest path based on time. This could potentially help to avoid switching lines as a tradeoff for a slightly longer ride.

4. Travelling Salesman Problem (subset of nodes to cover)

The goal of this algorithm is to find the most optimal path to cover all the stations specified in the least amount of time, while returning to the first station in the end. For this problem, the key was to use dynamic programming rather than a brute-force permutations approach to reduce the amount of repetitive computation needed.

## Features

- Highlight a specific subway line
- Select the speed of which to run the visualization
- Show/hide the breakdown of the subway lines in the path found
