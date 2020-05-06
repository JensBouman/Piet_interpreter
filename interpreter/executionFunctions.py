import copy
from typing import Union, List, Callable
import sys

import numpy as np

# sys.path.insert(0, "../")
from interpreter import imageWrapper as imageWrapper
from interpreter import lexer as lexer
from interpreter import tokens as tokens
from interpreter import movement as movement
from interpreter import colors as colors
from interpreter import tokenFunctions as runner
from interpreter import errors as errors
from interpreter.dataStructures import programState, position, direction


def interpret(image: np.ndarray) -> Union[programState, List[BaseException]]:
    """
    Interprets and executes a Piet image
    :param image: Input image
    :return: Either the final state of the program, or a list of exceptions
    """
    graph = lexer.graphImage(image)
    if len(graph[1]) > 0:
        print("The following exceptions occured while making the graph:\n{}".format("".join(list(map(lambda x: "\t{}\n".format(x), graph[1])))))
        return graph[1]

    startPosition = position((0, 0))
    pointers = direction((0, 0))
    PS = programState(graph[0], startPosition, pointers)

    result = runProgram(image, PS)
    if isinstance(result, BaseException):
        print("The following exceptions occured while executing the next step:\n{}".format(result))
        return [result]
    return result


def runProgram(image: np.ndarray, PS: programState) -> Union[programState, BaseException]:
    """
    Executes all steps from the image
    :param image: input image
    :param PS: current program state with which to make the next step
    :return: Either the last program state, or a runtime exception
    """
    newState = copy.deepcopy(PS)

    if colors.isBlack(imageWrapper.getPixel(image, newState.position)):
        return errors.inBlackPixelError("Programstate starts in black pixel at {}".format(newState.position))

    currentCodel = imageWrapper.getCodel(image, newState.position)
    newGraph = newState.graph.graph
    graphNode = newGraph[currentCodel]
    newToken = graphNode.graphNode[newState.direction][0]

    if isinstance(newToken, tokens.terminateToken):
        return newState

    newState = takeStep(image, newState)
    if isinstance(newState, BaseException):
        return newState

    return runProgram(image, newState)


def countSteps(f: Callable):
    def inner(image: np.ndarray, PS: programState):
        inner.counter += 1
        return f(image, PS)
    inner.counter = 0
    return inner

@countSteps
def takeStep(image: np.ndarray, PS: programState) -> Union[programState, BaseException]:
    """
    Takes a single step from the programstate
    :param image: input image
    :param PS: input programstate
    :return: Returns either the resulting programstate, or an exception that occurred
    """
    newState = copy.deepcopy(PS)
    currentCodel = imageWrapper.getCodel(image, newState.position)

    newGraph = newState.graph.graph
    graphNode = newGraph[currentCodel]
    newToken = graphNode.graphNode[newState.direction][0]

    edgePosition = graphNode.graphNode[newState.direction][1]

    result = runner.executeToken(newToken, newState.direction, newState.dataStack)

    if isinstance(result, BaseException):
        return result

    # If the next token is either white or color, just move along. If the token was black (or terminate), the direction
    # is already changed
    if isinstance(newToken, (tokens.toWhiteToken, tokens.toColorToken)):
        newState.position = movement.getNextPosition(edgePosition, newState.direction.pointers[0])

    newState.direction = result[0]
    newState.dataStack = result[1]

    return newState


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    im = imageWrapper.getImage("../Piet_hello.png")
    interpret(im)
