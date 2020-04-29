from typing import Dict, List, Tuple
from copy import deepcopy

import interpreter.lexerTokens as lexerTokens


class programState():
    def __init__(self, graph:  Dict[int, Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]], position: Tuple[int, int], pointers: Tuple[int, int], dataStack: List[int] = None):
        if dataStack is None:
            dataStack = []

        self.graph = graph
        self.pointers = pointers
        self.position = position
        self.dataStack = dataStack

    def __str__(self):
        return "{pos} / {pointers}. Stack: {stack}".format(pos=self.position, pointers=self.pointers, stack=self.dataStack)

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memodict):
        return programState(self.graph, deepcopy(self.position), deepcopy(self.pointers), deepcopy(self.dataStack))
