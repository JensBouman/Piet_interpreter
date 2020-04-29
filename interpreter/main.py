import copy
from typing import Union
import threading
import time
import sys

import numpy as np

import interpreter.imageWrapper as imageWrapper
import interpreter.lexer as lexer
import interpreter.lexerTokens as lexerTokens
import interpreter.movement as movement
import interpreter.programState as programState
import interpreter.runner as runner


def interpret(image: np.ndarray):
    graph = lexer.graphImage(im)
    position = (0, 0)
    pointers = (0, 0)
    PS = programState.programState(graph, position, pointers)

    runProgram(image, PS)


def runProgram(image: np.ndarray, PS: programState) -> programState:
    newState = PS
    currentCodel = imageWrapper.getCodel(image, newState.position)

    frozencodel = frozenset(currentCodel)
    newToken = newState.graph[hash(frozencodel)][hash(newState.pointers)][0]

    if isinstance(newToken, lexerTokens.terminateToken):
        print("")
        print("TERMINATE!")
        return newState

    newState = takeStep(image, newState)

    return runProgram(image, newState)


def takeStep(image: np.ndarray, PS: programState.programState) -> Union[programState.programState, bool]:
    newState = copy.deepcopy(PS)
    currentCodel = imageWrapper.getCodel(image, newState.position)

    frozencodel = frozenset(currentCodel)
    newToken = newState.graph[hash(frozencodel)][hash(newState.pointers)][0]
    edgePosition = newState.graph[hash(frozencodel)][hash(newState.pointers)][1]
    result = runner.executeToken(newToken, newState.pointers, newState.dataStack)

    if result is None:
        print("TERMINATE")
        return False

    if isinstance(newToken, lexerTokens.toWhiteToken) or isinstance(newToken, lexerTokens.toColorToken):
        newState.position = movement.getNextPosition(edgePosition, newState.pointers[0])

    newState.pointers = result[0]
    newState.dataStack = result[1]

    return newState


class run:
    def __init__(self, image: np.ndarray):
        self.image = image


    def __call__(self):
        self.run_program(self.image, programState.programState(lexer.graphImage(self.image), (0,0), (0,0)) )


    def run_program(self,image: np.ndarray, PS: programState) -> programState:
        currentCodel = imageWrapper.getCodel(image, PS.position)

        frozencodel = frozenset(currentCodel)
        newToken = PS.graph[hash(frozencodel)][hash(PS.pointers)][0]

        if isinstance(newToken, lexerTokens.terminateToken):
            print("")
            print("TERMINATE!")
            return PS
        return self.run_program(image, takeStep(image, PS))


if __name__ == "__main__":
    im = imageWrapper.getImage("../brainfuck_interpreter_black.png")
    interpret(im)

    start_time = time.time()
    sys.setrecursionlimit(0x100000)
    threading.stack_size(256000000) #set stack to 256mb
    t = threading.Thread(target=run(im))
    t.start()
    t.join()
