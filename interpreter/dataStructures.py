from typing import Set, Tuple, Dict, List
import copy

from interpreter import tokens as tokens

class position():
    """
    A coords is a tuple of x and y coordinates
    """
    def __init__(self, newPosition: Tuple[int, int]):
        self.coords = newPosition

    def __str__(self):
        return "{}".format(self.coords)

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict):
        return position(copy.deepcopy(self.coords))

    # Functions to allow this datatype to behave in sets
    def __hash__(self):
        return hash(self.coords)

    def __eq__(self, other):
        return other.coords == self.coords

    def __ne__(self, other):
        return not self == other


class direction():
    """
    A direction is made up of a Direction Pointer (DP) at .pointers[0] and a Codel Chooser (CC) at .pointers[1].
    """
    def __init__(self, newPointers: Tuple[int, int]):
        self.pointers = newPointers

    def __str__(self):
        return "{}".format(self.pointers)

    def __repr__(self):
        return "{}".format(self.pointers)

    def __deepcopy__(self, memodict):
        return direction(copy.deepcopy(self.pointers))

    # Functions to allow this datatype to behave in sets
    def __eq__(self, other):
        return self.pointers == other.pointers

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.pointers)

class codel():
    """
    A codel is a set of positions adjacent to each other and with the same color as each other
    """
    def __init__(self, newCodel: Set[position]):
        self.codel = newCodel

    def __str__(self):
        return "{}".format(self.codel)

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return codel(copy.copy(self.codel))

    # Functions to allow this datatype to behave in sets
    def __hash__(self):
        # Return a hash of a frozenset, because a normal set can't be hashed
        return hash(frozenset(self.codel))

    def __eq__(self, other):
        return other.codel == self.codel

    def __ne__(self, other):
        return not self == other

class edge():
    """
    The edge contains a position and direction (DP and CC)
    """
    def __init__(self, newEdge: Tuple[position, direction]):
        self.edge = newEdge

    def __str__(self):
        return "{}".format(self.edge)

    def __repr__(self):
        return str(self)


class graphNode():
    """
    The key to the token and coords is a direction
    """
    def __init__(self, newNode: Dict[direction, Tuple[tokens.baseLexerToken, position]]):
        self.graphNode = newNode

    def __str__(self):
        return "{}".format(self.graphNode)

    def __repr__(self):
        return str(self)


class graph():
    """
    Each codel has a node of directions and tokens associated with those directions (and where the edge will start)
    """
    def __init__(self, newGraph: Dict[codel, graphNode]):
        self.graph = newGraph

    def __str__(self):
        return "{}".format(self.graph)

    def __repr__(self):
        return str(self)

class programState():
    """
    The program state contains the graph of the program, the position, direction and stack.
    """
    def __init__(self, newGraph:  graph, newPosition: position, newDirection: direction, dataStack: List[int] = None):
        if dataStack is None:
            dataStack = []

        self.graph = newGraph
        self.position = newPosition
        self.direction = newDirection
        self.dataStack = dataStack

    def __str__(self):
        return "Pos:{pos} / {pointers}. Stack: {stack}".format(pos=self.position, pointers=self.direction, stack=self.dataStack)

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict):
        # Don't copy the graph, because it is not intended to be edited, and it is a slow process
        return programState(self.graph, copy.deepcopy(self.position), copy.deepcopy(self.direction), copy.deepcopy(self.dataStack))
