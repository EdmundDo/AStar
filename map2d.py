""" Utilities for a 2D grid """

import math
from enum import Enum

class Map2DSymbol(Enum):
    """
    Map2DSymbol enums

    :attribute WALL: wall representation, highest precedence
    :attribute PATH: path representation
    :attribute MARKER: specially marked locations on map, lowest precedence
    """

    WALL   = 1
    PATH   = 2
    MARKER = 3


class Map2DNode:
    """
    Rep for a map node

    :attribute int x: x-coordinate of the node
    :attribute int y: y-coordinate of the node
    :attribute char sym: the symbol on the map
    """

    def __init__(self, x, y, sym):
        """
        Constructor for a map node

        :param int x: the x coordinate
        :param int y: the y coordinate
        :param char sym: the symbol at this position
        """
        self.x = x
        self.y = y
        self.sym = sym

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x < other.x or self.y < other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def dist(a, b):
        """
        Gets the distance between nodes

        :param MapNode a: a node
        :param MapNode b: the other node
        """
        return math.sqrt(pow(b.x - a.x, 2) + pow(b.y - a.y, 2))


class Map2D:
    """
    A 2D representation of a map

    :attribute list[list(MapNode)] map_rep: a 2d array of chars
    :attribute dict[char, MapNode] markers: unique points in maze
    :attribute set(Map2DNode) visitedNodes: the visited nodes
    """
    def __init__(self, map_rep = None, markers = None, obst_char = '#', 
        path_char = '.'):
        """
        Constructor for a grid map

        :param list[list(Map2DNode)] map_rep: a 2d array of chars 
            representing the map
        :param dict[char, Map2DNode] markers: mapping of chars to notable
            markers
        :param char obst_char: the obstacle character (default: '#')
        :param char path_char: the path character (default: '.')
        """

        # default values if parameters are default None
        if map_rep is None:
            self.map_rep = []
        else:
            self.map_rep = map_rep

        if markers is None:
            self.markers = {}
        else:
            self.markers = markers

        self.visitedNodes = set()
        self.char_to_rep = {obst_char: Map2DSymbol.WALL, path_char: Map2DSymbol.PATH}

    def __str__(self):
        s = ""
        for row in self.map_rep:
            for map_node in row:
                s += map_node.sym
            s += "\n"
        return s

    def get_neighbors(self, m_node):
        """
        Get neighbors around a given node

        :param Map2DNode m_node: the node to get the neighbors of
        :rtype list(Map2DNode)
        """

        neighbors = []

        x = m_node.x
        y = m_node.y

        # get neighbors on four adjacent sides
        if x + 1 >= 0 and x + 1 < len(self.map_rep[y]):
            neighbors.append(self.map_rep[y][x + 1])

        if y + 1 >= 0 and y + 1 < len(self.map_rep):
            neighbors.append(self.map_rep[y + 1][x])

        if y - 1 >= 0 and y - 1 < len(self.map_rep):
            neighbors.append(self.map_rep[y - 1][x])

        if x - 1 >= 0 and x - 1 < len(self.map_rep[y]):
            neighbors.append(self.map_rep[y][x - 1])

        return neighbors

    def get_marker(self, marker_sym):
        """
        Get the node with the marker symbol

        :param char marker_sym: the marker symbol
        
        :return: if is a marker node, Map2DNode; otherwise -1
        :rtype Map2DNode|int
        """

        for key in self.markers.keys():
            if key == marker_sym:
                return self.markers[key]
        return -1

    def is_pt_marker(self, m_node):
        """
        Determine whether the node is a marker

        :param Map2DNode m_node: the node to check
        :rtype boolean
        """

        for marker in self.markers:
            if marker == m_node:
                return True
        return False

    def add_visited(self, m_node):
        """
        Track which nodes were visited

        :param Map2DNode m_node: the map node to add
        """
        self.visitedNodes.add(m_node)

    def is_visited(self, m_node):
        """
        Check if a node was visited

        :param Map2DNode m_node: the map node to check
        """
        return m_node in self.visitedNodes

    def get_rep(self, sym):
        """
        Gets the representation of the character in the file

        :param char sym: the character for the representation
        :rtype: the type of the symbol in the map
        """

        return self.char_to_rep.get(sym, Map2DSymbol.MARKER)
        
def parse(filename, map2d):
    """
    Parses a file and maps the markers
    
    Modifies map_rep and markers to contain information representative of the
    map in the file.

    :param str filename: the filename to open
    """

    file = open(filename)
    for line in file:
        row = []

        for char in line:
            if char == '\n':
                continue

            # standard info about character in file
            x = len(row)
            y = len(map2d.map_rep)
            rep = map2d.get_rep(char)
            m_node = Map2DNode(x, y, char)

            # track markers
            if rep == Map2DSymbol.MARKER:
                map2d.markers[char] = m_node

            row.append(m_node)

        map2d.map_rep.append(row)
    file.close()