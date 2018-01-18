import unittest

from map2d import Map2D, parse
from map2d_traverser import Map2DTraverser

class TraverseTest(unittest.TestCase):
    def parse_file(self):
        filename = input("Filename: ")
        maze = Map2D()
        parse(filename, maze)
        return maze

    def print_path(self):
        maze = self.parse_file()
        trav = Map2DTraverser(maze, 1, 1)
        paths = trav.traverse('1')
        for path in paths:
            print(path)

    def print_maze_path(self):
        maze = self.parse_file()
        trav = Map2DTraverser(maze, 1, 1)
        trav.print_path_to('1')
