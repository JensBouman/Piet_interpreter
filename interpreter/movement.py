from typing import Tuple, Set, Union


def getDP(directionPointer: int) -> str:
    if directionPointer == 0:
        return 'r'
    elif directionPointer == 1:
        return 'd'
    elif directionPointer == 2:
        return 'l'
    else:
        return 'u'


def getCC(codelChooser: int) -> str:
    if codelChooser == 0:
        return 'l'
    else:
        return 'r'


def getArrow(pointers: Tuple[int, int]) -> str:
    if pointers[0] == 0:
        if pointers[1] == 0:
            return "\u2197"
        elif pointers[1] == 1:
            return "\u2198"
    elif pointers[0] == 1:
        if pointers[1] == 0:
            return "\u2198"
        elif pointers[1] == 1:
            return "\u2199"
    elif pointers[0] == 2:
        if pointers[1] == 0:
            return "\u2199"
        elif pointers[1] == 1:
            return "\u2196"
    elif pointers[0] == 3:
        if pointers[1] == 0:
            return "\u2196"
        elif pointers[1] == 1:
            return "\u2197"
    else:
        return ""


def flipCC(codelChooser: int) -> int:
    """
    Flips the codelChooser 0 -> 1, 1 -> 0
    :param codelChooser: unflipped codelChooser
    :return: flipped codelChooser
    """
    return int(not codelChooser)


def flipDP(directionPointer: int) -> int:
    """
    Cycles the directionpointer 0 -> 1, 1 -> 2, 2 -> 3, 3 -> 0
    :param directionPointer: unflipped directionPointer
    :return: new DirectionPointer
    """
    if directionPointer != 3:
        return directionPointer + 1
    return 0


def flip(pointers: Tuple[int, int]) -> Tuple[int, int]:
    """
    Chooses what part of the general pointer to flip, by DP%2 == CC rule, providing the following flow:
    (0,0) -> (0,1)
    (0,1) -> (1,1)
    (1,1) -> (1,0)
    (1,0) -> (2,0)
    (2,0) -> (2,1)
    (2,1) -> (3,1)
    (3,1) -> (3,0)
    (3,0) -> (0,0)
    :param pointers: Original state of the pointers
    :return: Tuple of ints containing new pointers
    """
    if pointers[0] % 2 == pointers[1]:
        return (pointers[0], flipCC(pointers[1]))
    else:
        return (flipDP(pointers[0]), pointers[1])


# TODO FIX KEYERROR
def getNextPosition(startPosition: Tuple[int, int], directionPointer: int) -> Union[Tuple[int, int], KeyError]:
    if directionPointer == 0:
        return (startPosition[0] + 1, startPosition[1])
    elif directionPointer == 1:
        return (startPosition[0], startPosition[1] + 1)
    elif directionPointer == 2:
        return (startPosition[0] - 1, startPosition[1])
    elif directionPointer == 3:
        return (startPosition[0], startPosition[1] - 1)
    else:
        return KeyError("Given key {} is no valid Direction Pointer (0, 1, 2, or 3)".format(directionPointer))


def getPreviousPosition(startPosition: Tuple[int, int], directionPointer: int) -> Tuple[int, int]:
    if directionPointer == 0:
        return getNextPosition(startPosition, 2)
    elif directionPointer == 1:
        return getNextPosition(startPosition, 3)
    elif directionPointer == 2:
        return getNextPosition(startPosition, 0)
    return getNextPosition(startPosition, 1)
    # TODO: make the else return an error, and elif return 'd' position


# TODO Error handling
def findEdge(codel: Set[Tuple[int, int]], pointers: Tuple[int, int]) -> Union[Tuple[int, int], bool]:
    """
    Finds the edge of the codel according to the direction pointer and the codel chooser
    :param codel: Set of adjacent positions with the same color
    :param pointers: Tuple where pointers[0] = DP and pointers[1] = CC
    :return: Position within the codel that is adjacent to the next pixel to go to
    """
    dp = pointers[0]
    cc = pointers[1]

    if dp == 0:
        edgePosition = max(codel, key=lambda lambdaPos: lambdaPos[0])
        for pos in codel:
            if pos[0] == edgePosition[0]:
                # -> ^ Right and up
                if cc == 0 and pos[1] < edgePosition[1]:
                    edgePosition = pos
                # -> V Right and down
                elif cc == 1 and pos[1] > edgePosition[1]:
                    edgePosition = pos
        return edgePosition
    elif dp == 1:
        edgePosition = max(codel, key=lambda lambdaPos: lambdaPos[1])
        for pos in codel:
            if pos[1] == edgePosition[1]:
                # V -> Down and right
                if cc == 0 and pos[0] > edgePosition[0]:
                    edgePosition = pos
                # V <- Down and left
                elif cc == 1 and pos[0] < edgePosition[0]:
                    edgePosition = pos
        return edgePosition
    elif dp == 2:
        edgePosition = min(codel, key=lambda lambdaPos: lambdaPos[0])
        for pos in codel:
            if pos[0] == edgePosition[0]:
                # <- V Left and down
                if cc == 0 and pos[1] > edgePosition[1]:
                    edgePosition = pos
                # <- ^ left and up
                elif cc == 1 and pos[1] < edgePosition[1]:
                    edgePosition = pos
        return edgePosition
    elif dp == 3:
        edgePosition = min(codel, key=lambda lambdaPos: lambdaPos[1])
        for pos in codel:
            if pos[1] == edgePosition[1]:
                # ^ <- Up and left
                if cc == 0 and pos[0] < edgePosition[0]:
                    edgePosition = pos
                # ^ -> Up and right
                elif cc == 1 and pos[0] > edgePosition[0]:
                    edgePosition = pos
        return edgePosition
    else:
        raise SyntaxError("DirectionPointer '{}' is unknown".format(dp))
