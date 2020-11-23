from typing import List, Tuple, Union
import copy

from interpreter import tokens as lexerTokens
from interpreter import movementFunctions as movement
from interpreter import errors as errors
from interpreter.dataStructures import direction


def executeToken(token: lexerTokens.baseLexerToken, inputDirection: direction, dataStack: List[int]) -> Union[Tuple[direction, List[int]], BaseException]:
    """
    Executes the function associated with tokens
    :param token: Input token
    :param inputDirection: Input direction
    :param dataStack: Input stack
    :return: Either a combination of a new stack and direction, or a runtime Exception
    """
    if isinstance(token, lexerTokens.toBlackToken):
        newPointers = movement.flip(inputDirection)
        return (newPointers, dataStack)
    if isinstance(token, lexerTokens.toWhiteToken):
        return (inputDirection, dataStack)
    if isinstance(token, lexerTokens.toColorToken):
        return executeColorToken(token, inputDirection, dataStack)
    if isinstance(token, lexerTokens.terminateToken):
        return (inputDirection, dataStack)
    return errors.UnknownTokenError("Token of type {} is unknown")



def executeColorToken(token: lexerTokens.toColorToken, inputDirection: direction, dataStack: List[int]) -> Union[Tuple[direction, List[int]], BaseException]:
    """
    Executes the to color operations
    :param token: input token
    :param inputDirection: Input direction
    :param dataStack: Input data stack
    :return: either a combination of a new direction and data stack, or a runtime Exception
    """
    if token.tokenType == "noop":
        return noopOperator(inputDirection, dataStack)
    elif token.tokenType == "push":
        # Needs the codelsize to push
        return pushOperator(token, inputDirection, dataStack)
    elif token.tokenType == "pop":
        return popOperator(inputDirection, dataStack)

    elif token.tokenType == "add":
        return addOperator(inputDirection, dataStack)
    elif token.tokenType == "subtract":
        return subtractOperator(inputDirection, dataStack)
    elif token.tokenType == "multiply":
        return multiplyOperator(inputDirection, dataStack)

    elif token.tokenType == "divide":
        return divideOperator(inputDirection, dataStack)
    elif token.tokenType == "mod":
        return modOperator(inputDirection, dataStack)
    elif token.tokenType == "not":
        return notOperator(inputDirection, dataStack)

    elif token.tokenType == "greater":
        return greaterOperator(inputDirection, dataStack)
    elif token.tokenType == "pointer":
        return pointerOperator(inputDirection, dataStack)
    elif token.tokenType == "switch":
        return switchOperator(inputDirection, dataStack)

    elif token.tokenType == "duplicate":
        return duplicateOperator(inputDirection, dataStack)
    elif token.tokenType == "roll":
        return rollOperator(inputDirection, dataStack)
    elif token.tokenType == "inN":
        return inNOperator(inputDirection, dataStack)

    elif token.tokenType == "inC":
        return inCOperator(inputDirection, dataStack)
    elif token.tokenType == "outN":
        return outNOperator(inputDirection, dataStack)
    elif token.tokenType == "outC":
        return outCOperator(inputDirection, dataStack)
    else:
        return errors.UnknownTokenError("Token {} not found".format(token.tokenType))


def noopOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Does nothing
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: input dataStack
    :return: Tuple of a copy of the dataStack and the endpointers of the token
    """
    return (copy.deepcopy(inputDirection), dataStack.copy())


def addOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pops the two values from the stack and add them together, then pushes the result
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: input datastack
    :return:
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)
    newStack.append(newStack.pop() + newStack.pop())
    return (inputDirection, newStack)


def subtractOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Subtracts the second value from the first value of the stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)

    first = newStack.pop()
    second = newStack.pop()
    newStack.append(second - first)
    return (inputDirection, newStack)


def multiplyOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pops the first 2 values from the stack, and pushes the product of them
    """
    newStack = list(dataStack)
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)
    newStack.append(newStack.pop() * newStack.pop())
    return (inputDirection, newStack)


def divideOperator(inputDirection: direction, dataStack: List[int]) -> Union[Tuple[direction, List[int]], BaseException]:
    """
    Provides integer division (//)
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: A list of ints as stack. last entry is the top
    :return: Tuple with the new data stack and new pointers
    """
    newStack = dataStack.copy()
    newDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (newDirection, newStack)

    first = newStack.pop()
    second = newStack.pop()
    if second == 0:
        return ZeroDivisionError("Division by zero {}/{}".format(first, second))
    newStack.append(int(second / first))
    return (newDirection, newStack)


def modOperator(inputDirection: direction, dataStack: List[int]) -> Union[Tuple[direction, List[int]], BaseException]:
    """
    Pops the first two values of the stack, mods the second value by the first value and pushes the result back to the stack
    :param inputDirection:
    :param dataStack:
    :return: Tuple of direction and new data stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)
    valA = newStack.pop()
    valB = newStack.pop()
    if valB == 0:
        return ZeroDivisionError("Second value is 0: {}%{}".format(valA, valB))
    newStack.append(valB % valA)
    return (inputDirection, newStack)


def greaterOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Compares the second value of the stack with the first value of the stack. If the stack is empty, this gets ignored
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: The list of values as the stack, last entry is the top of the stack
    :return: A tuple of pointers and new data stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)

    valA = newStack.pop()
    valB = newStack.pop()

    newStack.append(int(valB > valA))
    return (inputDirection, newStack)


def notOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Compares the second value of the stack with the first value of the stack
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: The input list of ints as stcak. Last entry is the top of the stack
    :return: A tuple of pointers and new data stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)

    result = 1 if newStack.pop() == 0 else 0
    newStack.append(result)
    return (inputDirection, newStack)


def pointerOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pop the top value of the stack, and turn the direction pointer that many times. (counter clockwise if negative)
    :param inputDirection:
    :param dataStack:
    :return:
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)

    dp = inputDirection.pointers[0]
    dpTurnCount = newStack.pop()
    # Python module makes negative modulo's positive, so we need to manually flip the DP the required amount of times
    if dpTurnCount < 0:
        dp = movement.flipDPInvert(dp, dpTurnCount)
        return (direction((dp, inputDirection.pointers[1])), newStack)
    else:
        # Cycle the DP forward by using the module operator
        newDP = (inputDirection.pointers[0] + (dpTurnCount % 4)) % 4
        return (direction((newDP, inputDirection.pointers[1])), newStack)


def switchOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pop the first value of the stack, and turn the codel chooser that many times.
    :param pointers:
    :param dataStack:
    :return:
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)

    ccTurnCount = abs(newStack.pop()) % 2
    newCC = (inputDirection.pointers[1] + ccTurnCount) % 2
    return (direction((inputDirection.pointers[0], newCC)), newStack)


def inNOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Add a number from the input. If it isn't a number, nothing is added instead
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    newVal = input("Input number: ")
    if newVal.isdigit():
        newStack.append(int(newVal))
    return (inputDirection, newStack)


def inCOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Add a numeric representation of a character to the stack.
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    newVal = input("Input character")
    if len(newVal) < 1:
        return (inputDirection, newStack)

    newStack.append(ord(newVal[0]))
    return (inputDirection, newStack)


def outNOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pops the top number from the stack and outputs it as a number
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)
    print(newStack.pop(), end="")
    return (inputDirection, newStack)


def outCOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pops the top number from the stack and outputs it as a number. Does nothing if top value is negative
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)
    valA = newStack.pop()
    if valA < 0:
        newStack.append(valA)
        return (inputDirection, newStack)

    print(chr(valA), end="")
    return (inputDirection, newStack)


def pushOperator(token: lexerTokens.toColorToken, inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pushes the codelsize of the token to the stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    newStack.append(token.codelSize)
    return (inputDirection, newStack)


def popOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Pops and discards the top number of the stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)
    newStack.pop()
    return (inputDirection, newStack)


def duplicateOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Duplicates the top value of the stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 1:
        return (inputDirection, newStack)

    val = newStack.pop()
    newStack.append(val)
    newStack.append(val)
    return (inputDirection, newStack)


def rollOperator(inputDirection: direction, dataStack: List[int]) -> Tuple[direction, List[int]]:
    """
    Rolls the stack x times, to a depth of y, where x is equal to the top value of the stack, and y is equal to the second value of the stack
    """
    newStack = dataStack.copy()
    inputDirection = copy.deepcopy(inputDirection)
    if len(newStack) < 2:
        return (inputDirection, newStack)

    rolls = newStack.pop()
    depth = newStack.pop()
    insertIndex = len(newStack) - depth
    newStack = rollStack(newStack, rolls, insertIndex)

    return (inputDirection, newStack)

def rollStack(dataStack: List[int], numberOfRolls: int, insertIndex: int) -> List[int]:
    """
    Rolls the stack recursively, and inverted when negative number of rolls
    :param dataStack: Input stack
    :param numberOfRolls: Number of rolls
    :param insertIndex: At which index to either insert new values, or to get values from
    :return: Rolled data stack
    """
    newStack = dataStack.copy()
    if numberOfRolls > 0:
        newStack.insert(insertIndex, newStack.pop())
        return rollStack(newStack, numberOfRolls - 1, insertIndex)
    elif numberOfRolls < 0:
        newStack.append(newStack.pop(insertIndex))
        return rollStack(newStack, numberOfRolls + 1, insertIndex)
    else:
        return newStack
