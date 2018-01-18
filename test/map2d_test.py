import unittest

from map2d import Map2D, Map2DNode, parse

class Map2DTest(unittest.TestCase):
    def test_neighbors(self):
        maze = Map2D()
        parse("test/maze1.txt", maze)

        neighbors = maze.get_neighbors(maze.map_rep[0][0])
        assert len(neighbors) == 2, "Length of neighbors not 2. It is " + str(len(neighbors))

        neighbors = maze.get_neighbors(maze.map_rep[1][1])
        assert len(neighbors) == 4, "Length of neighbors not 4. It is " + str(len(neighbors))

        for neighbor in neighbors:
            assert Map2DNode.dist(maze.map_rep[1][1], neighbor) <= 1
            assert Map2DNode.dist(maze.map_rep[1][1], neighbor) > 0

    def print_maze(self):
        maze = Map2D()
        parse("test/maze1.txt", maze)
        print(maze)
