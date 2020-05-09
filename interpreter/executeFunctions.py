import copy
from typing import Union, List, Callable

import numpy as np

from interpreter import imageFunctions as imageWrapper
from interpreter import lexer as lexer
from interpreter import tokens as tokens
from interpreter import movementFunctions as movement
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

    # This is the default programState.
    startPosition = position((0, 0))
    pointers = direction((0, 0))
    PS = programState(graph[0], startPosition, pointers)

    result = runProgram(image, PS)
    # Check if executed step had an error
    if isinstance(result, BaseException):
        print("The following exception occured while executing the next step:\n{}".format(result))
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


def countSteps(f: Callable[[np.ndarray, programState], programState]) -> Callable[[np.ndarray, programState], programState]:
    """
    A decorator function to count the steps taken in the program
    :param f: original function to call
    :return: A decorated function
    """
    def inner(image: np.ndarray, PS: programState) -> programState:
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

    # Add additional information to the error message (Position and direction)
    if isinstance(result, BaseException):
        return type(result)("{}, at position {}, direction {}".format(result.args[0], edgePosition,newState.direction))
        # return result

    # If the next token is either white or color, just move along. If the token was black (or terminate), the direction
    # is already changed, but the position shouldn't move
    if isinstance(newToken, (tokens.toWhiteToken, tokens.toColorToken)):
        newState.position = movement.getNextPosition(edgePosition, newState.direction.pointers[0])

    # Use the new direction and stack for the next step
    newState.direction = result[0]
    newState.dataStack = result[1]

    return newState
