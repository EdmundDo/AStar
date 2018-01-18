""" Main for traversing a maze """

import map2d
import map2d_traverser as map2d_t

maze = map2d.Map2D()

filename = input("Filename: ")
dest_sym = input("Destination symbol: ")

map2d.parse(filename, maze)

m_trav = map2d_t.Map2DTraverser(maze, 1, 1)
m_trav.print_path_to(dest_sym)