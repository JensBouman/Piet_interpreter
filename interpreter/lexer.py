from typing import List, Tuple, Set, Dict, Union

import numpy as np

import interpreter.colors as colors
import interpreter.imageWrapper as imageWrapper
import interpreter.lexerTokens as lexerTokens
import interpreter.movement as movement


def cyclePosition(image: np.ndarray, startPosition: Tuple[int, int]) -> Union[Tuple[int, int], bool]:
    """
    :param image: numpy image array
    :param startPosition: from where to go to Tuple (x,y)
    :return: newPosition (x,y), or false if new position would fall out of bounds
    """
    if not imageWrapper.boundsChecker(image, startPosition):
        return False

    if startPosition[0] == image.shape[1] - 1:
        if startPosition[1] < image.shape[0] - 1:
            return (0, startPosition[1] + 1)
        else:
            return False
    else:
        return (startPosition[0] + 1, startPosition[1])



def getCodelsEfficient(image: np.ndarray, positionList: List[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    if len(positionList) == 0:
        return []
    copiedList = positionList.copy()
    newPosition = copiedList.pop(0)


    if colors.isBlack(imageWrapper.getPixel(image, newPosition)):
        return getCodelsEfficient(image, copiedList)

    newCodel = imageWrapper.getCodel(image, newPosition)

    # print("Original positionList: {}".format(positionList))
    # print("Codel found: {}".format(newCodel))
    # Remove found positions from position list
    copiedList = list(set(copiedList) - newCodel)
    # print("New positionList: {}".format(copiedList))
    codelList = getCodelsEfficient(image, copiedList)

    codelList.append(newCodel)
    return codelList




def getAllCodels(image: np.ndarray, position: Tuple[int, int] = (0, 0),
                 foundCodels: List[Set[Tuple[int, int]]] = None) -> List[Set[Tuple[int, int]]]:
    if foundCodels is None:
        foundCodels = []

    # Checks if the current position is already in a found codel, and also if the current pixel is white or black
    if (True in map(lambda codelSet, lambdaPosition=position: lambdaPosition in codelSet, foundCodels)) or colors.isBlack(imageWrapper.getPixel(image, position)):
        nextPosition = cyclePosition(image, position)
        if type(nextPosition) == bool and not nextPosition:
            return foundCodels
        return getAllCodels(image, nextPosition, foundCodels)

    newCodel = imageWrapper.getCodel(image, position)
    foundCodels.append(newCodel)

    nextPosition = cyclePosition(image, position)
    if type(nextPosition) == bool and nextPosition is False:
        return foundCodels
    else:
        return getAllCodels(image, nextPosition, foundCodels)


def edgesToCodeldict(image: np.ndarray, edges: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]:
    """
    Constructs a dictionary with each pointer possibility as key and (token, position) as value
    :param image: Image required to find calculate tokens
    :param edges: List[Tuple[position, pointers]]
    :return:
    """
    return dict(map(lambda x, lambdaImage=image: (hash(x[1]), (lexerTokens.edgeToToken(lambdaImage, x), x[0])), edges))


def isCodeldictTerminate(codelDict: Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]) -> bool:
    return all(map(lambda x: isinstance(x[1][0], lexerTokens.toBlackToken), codelDict.items()))


def codelDictToTerminate(codelDict: Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]) -> Dict[int, Tuple[lexerTokens.terminateToken, Tuple[int, int]]]:
    return dict(map(lambda x: (x[0], (lexerTokens.terminateToken(), x[1][1])), codelDict.items()))


def codelToCodelDict(image: np.ndarray, codel: Set[Tuple[int, int]], edgePointers: List[Tuple[int, int]]) -> Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]:
    """
    :param image: image
    :param codel: set of positions within the same color
    :param edgePointers: list of pointers to find tokens for
    :return: A dictionary with each pointer possibility as key and (token, position) as value
    """
    # make codel immutable
    copiedCodel = frozenset(codel)
    # Find all edges along the codel and edgepointers
    edges = list(map(lambda pointers, lambdaCodel=copiedCodel: (movement.findEdge(lambdaCodel, pointers), pointers), edgePointers))
    codelDict = edgesToCodeldict(image, edges)

    if isCodeldictTerminate(codelDict):
        codelDict = codelDictToTerminate(codelDict)

    return codelDict


def graphImage(image: np.ndarray, position: Tuple[int, int] = (0, 0)) -> Dict[int, Dict[int, Tuple[lexerTokens.baseLexerToken, Tuple[int, int]]]]:
    """
    Returns a dict with hashes of each codel as keys, and a codelDict as value. That codelDict contains hashed pointers (Tuple[int, int]) as keys to tokens as values.
    :param image:
    :param position:
    :return:
    """
    # allCodels = getAllCodels(image, position)
    allPositions = []
    whiteCodels = []
    print(image)
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            if not colors.isBlack(pixel):
                if colors.isWhite(pixel):
                    whiteCodels.append((x,y))
                else:
                    allPositions.append((x,y))
    print(len(allPositions))


    allCodels = getCodelsEfficient(image, allPositions)
    # Get an iterator of all possible pointers
    edgePointers = list(map(lambda i: (i % 4, int(i / 4)), iter(range(8))))
    return dict(map(lambda x: (hash(frozenset(x)), codelToCodelDict(image, x, edgePointers)), allCodels))
