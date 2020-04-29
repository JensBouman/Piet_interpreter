from typing import List, Tuple

import interpreter.lexerTokens as lexerTokens
import interpreter.movement as movement


# TODO Nettere afhandeling errors (Union[Tuple[List[int], Tuple[int, int]], bool])
# TODO Test cases maken per token
def executeToken(token: lexerTokens.baseLexerToken, pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    if isinstance(token, lexerTokens.toBlackToken):
        newPointers = movement.flip(pointers)
        return (newPointers, dataStack)
    elif isinstance(token, lexerTokens.toWhiteToken):
        return (pointers, dataStack)
    elif isinstance(token, lexerTokens.toColorToken):
        result = executeColorToken(token, pointers, dataStack)
        return (result[0], result[1])


def executeColorToken(token: lexerTokens.toColorToken, pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    if token.tokenType == "noop":
        return noopOperator(pointers, dataStack)
    elif token.tokenType == "push":
        # Needs the codelsize to push
        return pushOperator(token, pointers, dataStack)
    elif token.tokenType == "pop":
        return popOperator(pointers, dataStack)

    elif token.tokenType == "add":
        return addOperator(pointers, dataStack)
    elif token.tokenType == "subtract":
        return subtractOperator(pointers, dataStack)
    elif token.tokenType == "multiply":
        return multiplyOperator(pointers, dataStack)

    elif token.tokenType == "divide":
        return divideOperator(pointers, dataStack)
    elif token.tokenType == "mod":
        return modOperator(pointers, dataStack)
    elif token.tokenType == "not":
        return notOperator(pointers, dataStack)

    elif token.tokenType == "greater":
        return greaterOperator(pointers, dataStack)
    elif token.tokenType == "pointer":
        return pointerOperator(pointers, dataStack)
    elif token.tokenType == "switch":
        return switchOperator(pointers, dataStack)

    elif token.tokenType == "duplicate":
        return duplicateOperator(pointers, dataStack)
    elif token.tokenType == "roll":
        return rollOperator(pointers, dataStack)
    elif token.tokenType == "inN":
        return inNOperator(pointers, dataStack)

    elif token.tokenType == "inC":
        return inCOperator(pointers, dataStack)
    elif token.tokenType == "outN":
        return outNOperator(pointers, dataStack)
    elif token.tokenType == "outC":
        return outCOperator(pointers, dataStack)
    else:
        # TODO Elegantere manier van afhandelen
        print("Type niet gevonden, noop uitgevoerd")
        return noopOperator(pointers, dataStack)


def noopOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    """
    Does nothing
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: input dataStack
    :return: Tuple of a copy of the dataStack and the endpointers of the token
    """
    return (pointers, list(dataStack))


def addOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    """
    Pops the two values from the stack and add them together, then pushes the result
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: input datastack
    :return:
    """
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)
    newStack.append(newStack.pop() + newStack.pop())
    return (pointers, newStack)


def subtractOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)

    first = newStack.pop()
    second = newStack.pop()
    newStack.append(second - first)
    return (pointers, newStack)


def multiplyOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)
    newStack.append(newStack.pop() * newStack.pop())
    return (pointers, newStack)


def divideOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    """
    Provides integer division (//)
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: A list of ints as stack. last entry is the top
    :return: Tuple with the new data stack and new pointers
    """
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)

    first = newStack.pop()
    second = newStack.pop()
    if second == 0:
        raise ZeroDivisionError("{} / {} ".format(first, second))
    newStack.append(newStack.pop() // newStack.pop())
    return (pointers, newStack)


def modOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)
    valA = newStack.pop()
    valB = newStack.pop()
    if valB == 0:
        return (pointers, newStack)
    newStack.append(valA % valB)
    return (pointers, newStack)


def greaterOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    """
    Compares the second value of the stack with the first value of the stack. If the stack is empty, this gets ignored
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: The list of values as the stack, last entry is the top of the stack
    :return: A tuple of pointers and new data stack
    """
    newStack = list(dataStack)
    if len(newStack) < 2:
        return (pointers, newStack)

    newStack.append(int(newStack.pop() < newStack.pop()))
    return (pointers, newStack)


def notOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    """
    Compares the second value of the stack with the first value of the stack
    :param pointers: The tuple with the direction pointer and codel chooser
    :param dataStack: The input list of ints as stcak. Last entry is the top of the stack
    :return: A tuple of pointers and new data stack
    """
    newStack = list(dataStack)
    if len(newStack) < 1:
        return (pointers, newStack)

    result = 1 if newStack.pop() == 0 else 0
    newStack.append(result)
    return (pointers, newStack)


def pointerOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 1:
        return (pointers, newStack)

    dpTurnCount = newStack.pop() % 4
    newDp = (pointers[0] + dpTurnCount) % 4
    return ((newDp, pointers[1]), newStack)


def switchOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 1:
        return (pointers, newStack)

    ccTurnCount = newStack.pop() % 2
    newCC = (pointers[1] + ccTurnCount) % 2
    return ((pointers[0], newCC), newStack)


# TODO BETERE IO
def inNOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    newVal = int(input("Input number: "))
    newStack.append(newVal)
    return (pointers, newStack)


def inCOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    newVal = input("Input character")
    if len(newVal) < 1:
        return (pointers, newStack)

    appendedStack = pushCharacters(newStack, newVal)
    return (pointers, appendedStack)


def pushCharacters(dataStack: List[int], characters: str) -> List[int]:
    newStack = list(dataStack)
    if len(characters) < 1:
        return newStack
    else:
        newStack.append(ord(characters[0]))
        return pushCharacters(newStack, characters[1:])


def outNOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    print(newStack.pop(), end="")
    return (pointers, newStack)


def outCOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    print(chr(newStack.pop()), end="")
    return (pointers, newStack)


def pushOperator(token: lexerTokens.toColorToken, pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    newStack.append(token.codelSize)
    return (pointers, newStack)


def popOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 1:
        return (pointers, newStack)
    newStack.pop()
    return (pointers, newStack)


def duplicateOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 1:
        return (pointers, newStack)

    val = newStack.pop()
    newStack.append(val)
    newStack.append(val)
    return (pointers, newStack)


def rollOperator(pointers: Tuple[int, int], dataStack: List[int]) -> Tuple[Tuple[int, int], List[int]]:
    newStack = list(dataStack)
    if len(newStack) < 3:
        return (pointers, newStack)
    rolls = newStack.pop()
    depth = newStack.pop()
    insertIndex = len(newStack) - depth

    if depth <= 0 or insertIndex < 0 or insertIndex >= len(newStack) or rolls == 0 or depth == rolls:
        return (pointers, newStack)

    # TODO could also do rolls % depth times, instead of rolls times
    if rolls < 0:
        for i in range(abs(rolls)):
            newStack.append(newStack.pop(insertIndex))
    else:
        for i in range(rolls):
            newStack.insert(insertIndex, newStack.pop())

    return (pointers, newStack)
