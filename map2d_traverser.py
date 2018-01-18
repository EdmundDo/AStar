""" Traverse a map to a particular destination from an inital position """

import queue

from map2d import Map2DSymbol

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

class Map2DTraverser:
    """ 
    A traverser for a given map at an initial location

    :attribute list(list(MazeMapNode)) map: the map to traverse
    :attribute int initX: the initial x coordinate
    :attribute int initY: the initial y coordinate
    :attribute function heuristic: the heuristic function to use 
        (default: manhattan)
    """

    def __init__(self, m_map, initX, initY, heuristic = manhattan):
        self.map = m_map
        self.initX = initX
        self.initY = initY
        self.heuristic = heuristic

    def traverse(self, dest_sym):
        """
        Traverse the map to find a valid path toward the destination

        Creates paths such that when given the destination, it could be
        backtracked to the origin.

        :param char dest_sym: a unique symbol for the destination
        :rtype: dict[tup(int,int), MazeMapNode]
        """

        frontier = queue.PriorityQueue()
        start_m_node = self.get_start_node()

        # insert via (priority, value) tuple
        frontier.put((0, start_m_node))
        paths = {start_m_node: None}
        total_cost_at = {start_m_node: 0}

        while not frontier.empty():
            # get the highest priority node to generate shortest path
            m_node = frontier.get()[1]

            if self.map.map_rep[m_node.y][m_node.x].sym == dest_sym:
                break

            # find next step in the path by going through neighbors
            for neighbor in self.map.get_neighbors(m_node):

                if self.map.get_rep(neighbor.sym) != Map2DSymbol.WALL and not self.map.is_visited(neighbor):
                    self.map.add_visited(neighbor)

                    paths[neighbor] = m_node

                    total_cost = self.heuristic(neighbor, self.map.get_marker(dest_sym)) + total_cost_at[m_node]
                    total_cost_at[neighbor] = total_cost

                    # place neighbor into the frontier with a priority based on the heuristic
                    frontier.put((total_cost, neighbor))

        return paths

    def print_path_to(self, dest_sym):
        """
        Print the path to the destination node

        :param char dest_sym: a unique symbol for the destination
        """

        # get a list of nodes traversed by the algorithm
        paths = self.traverse(dest_sym)

        # recreate a valid path to destination
        path = self._build_path(paths, dest_sym)

        map_rep = list(self.map.map_rep)
        
        # replace all nodes in the path and maze to X
        for m_node in path:
            map_rep[m_node.y][m_node.x].sym = 'X'

        map_rep[self.initY][self.initX].sym = 'S'
        
        for row in map_rep:
            for m_node in row:
                print(m_node.sym, end="")
            print()

    def get_start_node(self):
        """
        Get the starting node
        """
        return self.map.map_rep[self.initY][self.initX]

    def _build_path(self, paths, dest_sym):
        """ 
        Backtrack through paths

        :param dict(tuple(int,int), MazeMapNode) paths: paths to backtrack
        :param char dest_sym: a unique symbol for the destination
        :rtype list
        """

        path = []

        dest_node = self.map.get_marker(dest_sym)
        current = paths[dest_node]

        # iterate through paths
        while current is not self.get_start_node():
            path.append(current)
            current = paths[current]
        return path