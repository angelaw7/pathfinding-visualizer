# Pathfinding Visualizer on London's Subway Network 🗺️

## Table of Contents

- [Project Description](https://github.com/angelaw7/pathfinding-visualizer#project-description)
- [Installation & Usage](https://github.com/angelaw7/pathfinding-visualizer#installation--usage)
- [Algorithms](https://github.com/angelaw7/pathfinding-visualizer#algorithms)
- [Features](https://github.com/angelaw7/pathfinding-visualizer#features)

## Project Description


The graph data is based on the London subway network which is openly available and can be found [here](https://commons.wikimedia.org/wiki/London_Underground_geographic_maps/CSV). I used this data rather than generating some random points on a grid to give a more realistic feel to the applications of graph algorithms. This was inspired by one of my course projects based on implementing and evaluating the KPIs on graph algorithms - as a visual learner, I wanted to build a visualizer to actually see how the stations and lines are positioned, and how the algorithms traverses through them.

<div align="center">
<img src="https://user-images.githubusercontent.com/74735037/210927330-9c19bff0-b999-4535-afdb-f53c6a0a7e64.png" width=700/>
</div>

<br/>

There's many other pathfinding visualizers out there but this is one that I created to help strengthen my knowledge of graph algorithms. The goal was not to make a stunning UI, but to have a working interface that does its job of observing how these algorithms perform step by step. I chose to use Python's Tkinter library so that the application stays minimalistic while displaying the necessary graph details and pathfinding inputs/settings. 


## Installation & Usage

1. Clone the repo
```
git clone git@github.com:angelaw7/pathfinding-visualizer.git
```

2. Go to project directory
```
cd pathfinding-visualizer
```

3. Run the project; this will open the GUI
```
py main.py
```

## Algorithms

1. Dijkstra's Algorithm

Dijkstra's algorithm is used to find the shortest path between two subway stations / nodes. The shortest path is determined by the minimal amount of time to travel between the source and destination stations.

https://user-images.githubusercontent.com/74735037/210927645-a3c15b35-2b66-4157-aec8-458a7d6fcd3e.mp4

2. A* Algorithm

The A-Star algorithm runs similarly to Dijkstra's but also uses a heuristic to guide which node to visit next. The heuristic used for this project was the euclidean distance between two stations, based on their geographical coordinates, as we would expect that choosing the path that gets us closer to the destination station is *usually* a good idea.

https://user-images.githubusercontent.com/74735037/210928434-8102ac5f-db87-4967-b45f-0bc4d4b6fc3e.mp4

3. Breadth First Search

Breadth first search's strengths lie in determining the path with the least connections, rather than the shortest path based on time. This could potentially help to avoid switching lines as a tradeoff for a slightly longer ride.

https://user-images.githubusercontent.com/74735037/210928485-1ca06f9a-bd02-45e3-9740-e0fb7723964d.mp4

4. Travelling Salesman Problem (subset of nodes to cover)

This is personally my favourite, although it does lag a bit while running the visualization since it needs to make quite a bit of calculations. The goal of this algorithm is to find the most optimal path to cover all the stations specified in the least amount of time, while returning to the first station in the end. For this problem, it was important to use dynamic programming rather than a brute-force permutations approach to reduce the amount of repetitive computation needed. It uses Dijkstra's to find the path between two stations, although A* could have also been used.

https://user-images.githubusercontent.com/74735037/210928502-cdaf8f5a-0565-4cf9-81b9-6c249ee19181.mp4

## Features

- Highlight a specific subway line
- Select the speed of which to run the visualization
- Show/hide the breakdown of the subway lines in the path found

https://user-images.githubusercontent.com/74735037/210928643-2974cbb5-2cf0-42e1-bbfd-a1eea8bde0ca.mp4



