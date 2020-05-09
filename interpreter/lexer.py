from typing import List, Union, Tuple
import copy
import numpy as np

import interpreter.colors as colors
import interpreter.imageFunctions as imageWrapper
import interpreter.tokens as tokens
import interpreter.helperFunctions as helperFunctions
import interpreter.movementFunctions as movement
from interpreter.dataStructures import position, codel, edge, graphNode, graph, direction


def cyclePosition(image: np.ndarray, startPosition: position) -> Union[position, bool]:
    """
    :param image: numpy image array
    :param startPosition: from where to go to Tuple (x,y)
    :return: newPosition (x,y), or false if new coords would fall out of bounds
    """
    if not imageWrapper.boundsChecker(image, startPosition):
        return False

    if startPosition.coords[0] == image.shape[1] - 1:
        if startPosition.coords[1] < image.shape[0] - 1:
            return position((0, startPosition.coords[1] + 1))
        return False
    return position((startPosition.coords[0] + 1, startPosition.coords[1]))


def getCodels(image: np.ndarray, positionList: List[position]) -> List[codel]:
    """
    Makes a list of codels from an image and a lits of positions to check
    :param image: an np.ndarray representing the image
    :param positionList: A list of positions, for which to find adjacent pixels of the same color
    :return: A list of codels found in the given image
    """
    if len(positionList) == 0:
        return []

    copiedList = positionList.copy()
    newPosition = copiedList.pop(0)

    if colors.isBlack(imageWrapper.getPixel(image, newPosition)):
        return getCodels(image, copiedList)

    newCodel = imageWrapper.getCodel(image, newPosition)

    # Remove found positions from coords list
    copiedList = list(set(copiedList) - newCodel.codel)
    codelList = getCodels(image, copiedList)

    codelList.append(newCodel)
    return codelList


def edgesToGraphNode(image: np.ndarray, edges: List[edge]) -> Tuple[graphNode, List[BaseException]]:
    """
    Constructs a dictionary with each pointer possibility as key and (token, coords) as value
    :param image: Image required to find calculate tokens
    :param edges: List[Tuple[coords, pointers]]
    :return: A graphNode containing tokens for each edge given, and a list of exceptions occurred during creation
    """
    node = graphNode(dict(map(lambda x, lambdaImage=image: (x.edge[1], (helperFunctions.edgeToToken(lambdaImage, x), x.edge[0])), edges)))
    # Extract the exceptions from each edge
    exceptions = list(map(lambda x: x[1][0], filter(lambda graphNodeItem: isinstance(graphNodeItem[1][0], BaseException), node.graphNode.items())))
    return (node, exceptions)


def isGraphNodeTerminate(inputNode: graphNode) -> bool:
    """
    Gets the token from the graphNode, and compares it against the toBlackToken from tokens.
    :param inputNode: A graph node
    :return: True if all tokens in graph node are toBlackTokens, False otherwise.
    """
    return all(map(lambda x: isinstance(x[1][0], tokens.toBlackToken), inputNode.graphNode.items()))


def graphNodeToTerminate(inputNode: graphNode) -> graphNode:
    """
    Replaces all tokens in the graphNode to terminate tokens
    :param inputNode: A graph node
    :return: A new graph node with only terminateTokens
    """
    return graphNode(dict(map(lambda x: (x[0], (tokens.terminateToken(), x[1][1])), inputNode.graphNode.items())))


def codelToGraphNode(image: np.ndarray, inputCodel: codel, edgePointers: List[direction]) -> Tuple[graphNode, List[BaseException]]:
    """
    :param image: image
    :param inputCodel: set of positions within the same color
    :param edgePointers: list of pointers to find tokens for
    :return: A dictionary with each pointer possibility as key and (token, coords) as value, and a list of exceptions
    """
    # make codel immutable
    copiedCodel = copy.copy(inputCodel)
    # Find all edges along the codel and edgepointers
    edges = list(map(lambda pointers, lambdaCodel=copiedCodel: edge((movement.findEdge(lambdaCodel, pointers), pointers)), edgePointers))
    newGraphNode = edgesToGraphNode(image, edges)

    # If there were exceptions in the graph node, there is no need to terminate them
    if len(newGraphNode[1]) > 0:
        return newGraphNode

    # Check if all tokens go either towards black pixels, or towards the edge. If thats the case, this is a terminate-node
    if isGraphNodeTerminate(newGraphNode[0]):
        return (graphNodeToTerminate(newGraphNode[0]), newGraphNode[1])

    return newGraphNode

def codelsToGraph(image: np.ndarray, codels: List[codel]) -> Tuple[graph, List[BaseException]]:
    """
    Converts a list of codels into a graph
    :param image: Input image
    :param codels: Input list of codels
    :return: A tuple of a graph and a list of exceptions
    """
    codels = codels.copy()
    # Get an iterator of all possible directions (0,0), (0,1), (1,0) etc...
    edgePointers = list(map(lambda i: direction((i % 4, int(i / 4))), iter(range(8))))

    # If no more codels are to be graphed, return
    if len(codels) == 0:
        newGraph = graph(dict())
        return (newGraph, [])

    newNode = codelToGraphNode(image, codels[0], edgePointers)
    newGraph = codelsToGraph(image, codels[1:])
    newGraph[0].graph[codels[0]] = newNode[0]

    errorList = newNode[1]
    errorList.extend(newGraph[1])
    return (newGraph[0], errorList)


def graphImage(image: np.ndarray) -> Tuple[graph, List[BaseException]]:
    """
    Returns a dict with hashes of each codel as keys, and a codelDict as value. That codelDict contains hashed pointers (Tuple[int, int]) as keys to tokens as values.
    :param image:
    :return:
    """
    coords = np.ndindex(image.shape[1], image.shape[0])
    # Converts tuples of coordinates into position objects
    positions = map(position, coords)
    # Makes a list of non-black pixel positions
    nonBlackPositions = list(filter(lambda pos: not colors.isBlack(imageWrapper.getPixel(image, pos)), positions))
    # Gets all codels from all non-black pixel positions
    allCodels = getCodels(image, nonBlackPositions)
    # Makes a graph with the codel as key, and the node as value
    return codelsToGraph(image, allCodels)
