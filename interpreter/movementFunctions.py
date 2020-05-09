from typing import Union
import operator

from interpreter.dataStructures import direction, position, codel

def getDP(directionPointer: int) -> str:
    """
    Finds the correct direction pointer string
    :param directionPointer: Input direction pointer
    :return: direction pointer string
    """
    if directionPointer == 0:
        return 'r'
    if directionPointer == 1:
        return 'd'
    if directionPointer == 2:
        return 'l'
    return 'u'


def getCC(codelChooser: int) -> str:
    """
    finds the correct codel chooser direction string
    :param codelChooser: input codel chooser
    :return: codel chooser direction string
    """
    if codelChooser == 0:
        return 'l'
    return 'r'


def getArrow(direction: direction) -> str:
    """
    Returns the Unicode arrow from the direction
    :param direction: Input direction
    :return: Unicode arrow string
    """
    if direction.pointers[0] == 0:
        if direction.pointers[1] == 0:
            return "\u2197"
        if direction.pointers[1] == 1:
            return "\u2198"
        return ""

    if direction.pointers[0] == 1:
        if direction.pointers[1] == 0:
            return "\u2198"
        if direction.pointers[1] == 1:
            return "\u2199"
        return ""

    if direction.pointers[0] == 2:
        if direction.pointers[1] == 0:
            return "\u2199"
        if direction.pointers[1] == 1:
            return "\u2196"
        return ""

    if direction.pointers[0] == 3:
        if direction.pointers[1] == 0:
            return "\u2196"
        if direction.pointers[1] == 1:
            return "\u2197"
        return ""
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

def flipDPInvert(directionPointer: int, count = 0) -> int:
    if count >= 0:
        return directionPointer
    else:
        if directionPointer != 0:
            return flipDPInvert(directionPointer - 1, count + 1)
        return flipDPInvert(3, count + 1)

def flip(inputDirection: direction) -> direction:
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
    :param inputDirection: Original state of the pointers
    :return: Tuple of ints containing new pointers
    """
    if inputDirection.pointers[0] % 2 == inputDirection.pointers[1]:
        return direction((inputDirection.pointers[0], flipCC(inputDirection.pointers[1])))
    return direction((flipDP(inputDirection.pointers[0]), inputDirection.pointers[1]))


def getNextPosition(startPosition: position, directionPointer: int) -> Union[position, KeyError]:
    """
    Finds next position along the direction pointer
    :param startPosition: start position
    :param directionPointer: direction pointer
    :return: next position
    """
    if directionPointer == 0:
        return position((startPosition.coords[0] + 1, startPosition.coords[1]))
    if directionPointer == 1:
        return position((startPosition.coords[0], startPosition.coords[1] + 1))
    if directionPointer == 2:
        return position((startPosition.coords[0] - 1, startPosition.coords[1]))
    if directionPointer == 3:
        return position((startPosition.coords[0], startPosition.coords[1] - 1))
    return KeyError("Given key {} is no valid Direction Pointer (0, 1, 2, or 3)".format(directionPointer))


def getPreviousPosition(startPosition: position, directionPointer: int) -> position:
    """
    Inverts the directionPointer, and finds the next position
    :param startPosition: Input position
    :param directionPointer: Input directionpointer
    :return: Previous position
    """
    if directionPointer == 0:
        return getNextPosition(startPosition, 2)
    if directionPointer == 1:
        return getNextPosition(startPosition, 3)
    if directionPointer == 2:
        return getNextPosition(startPosition, 0)
    return getNextPosition(startPosition, 1)


def findEdge(inputCodel: codel, inputDirection: direction) -> Union[position, bool]:
    """
    Finds the edge of the codel according to the direction pointer and the codel chooser
    :param inputCodel: Set of adjacent positions with the same color
    :param pointers: Tuple where pointers[0] = DP and pointers[1] = CC
    :return: Position within the codel that is adjacent to the next pixel to go to
    """
    dp = inputDirection.pointers[0]
    cc = inputDirection.pointers[1]

    # Right side
    if dp == 0:
        edgePosition = max(inputCodel.codel, key=lambda lambdaPos: lambdaPos.coords[0])
        maxValues = list(filter(lambda lambdaPos: lambdaPos.coords[0] == edgePosition.coords[0], inputCodel.codel))
        if cc == 0:
            # -> ^ Right and up
            return min(maxValues, key=lambda lambdaPos: lambdaPos.coords[1])
        else:
            # -> V Right and down
            return max(maxValues, key=lambda lambdaPos: lambdaPos.coords[1])
    # Bottom side
    elif dp == 1:
        edgePosition = max(inputCodel.codel, key=lambda lambdaPos: lambdaPos.coords[1])
        maxValues = list(filter(lambda lambdaPos: lambdaPos.coords[1] == edgePosition.coords[1], inputCodel.codel))
        if cc == 0:
            # V -> Down and right
            return max(maxValues, key=lambda lambaPos: lambaPos.coords[0])
        else:
            # V <- Down and left
            return min(maxValues, key=lambda lambdaPos: lambdaPos.coords[0])
    # Left side
    elif dp == 2:
        edgePosition = min(inputCodel.codel, key=lambda lambdaPos: lambdaPos.coords[0])
        minValues = list(filter(lambda lambdaPos: lambdaPos.coords[0] == edgePosition.coords[0], inputCodel.codel))
        if cc == 0:
            # <- V Left and down
            return max(minValues, key=lambda lambaPos: lambaPos.coords[1])
        else:
            # <- ^ left and up
            return min(minValues, key=lambda lambdaPos: lambdaPos.coords[1])

    # Top side
    else: # dp == 3
        edgePosition = min(inputCodel.codel, key=lambda lambdaPos: lambdaPos.coords[1])
        maxValues = list(filter(lambda lambdaPos: lambdaPos.coords[1] == edgePosition.coords[1], inputCodel.codel))
        if cc == 0:
            # ^ <- Up and left
            return min(maxValues, key=lambda lambaPos: lambaPos.coords[0])
        else:
            # ^ -> Up and right
            return max(maxValues, key=lambda lambdaPos: lambdaPos.coords[0])
