from typing import Tuple, Union
import numpy as np

import interpreter.imageWrapper as imageWrapper
import interpreter.movement as movement
import interpreter.colors as colors


class baseLexerToken():
    def __init__(self, tokenType: str):
        self.tokenType = tokenType

    def __str__(self):
        return "Token tokenType = {}".format(self.tokenType)

    def __repr__(self):
        return str(self)


class toBlackToken(baseLexerToken):
    def __init__(self, tokenType: str = "toBlack"):
        super().__init__(tokenType)


class toWhiteToken(baseLexerToken):
    def __init__(self):
        super().__init__("toWhite")


class terminateToken(baseLexerToken):
    def __init__(self):
        super().__init__("exit")


class toColorToken(baseLexerToken):
    def __init__(self, tokenType: str, codelSize: int):
        super().__init__(tokenType)
        self.codelSize = codelSize

    def __str__(self):
        return "{}, codelSize = {}".format(super().__str__(), self.codelSize)


def getToken(hueChange: int, lightChange: int) -> str:
    tokens = [
        ["noop", "push", "pop"],
        ["add", "subtract", "multiply"],
        ["divide", "mod", "not"],
        ["greater", "pointer", "switch"],
        ["duplicate", "roll", "inN"],
        ["inC", "outN", "outC"],
    ]
    return tokens[hueChange][lightChange]


def edgeToToken(image: np.ndarray, edge: Tuple[Tuple[int, int], Tuple[int, int]]) -> Union[baseLexerToken, bool]:
    """
    :param image:
    :param edge: (position, direction)
    :return:
    """
    if not imageWrapper.boundsChecker(image, edge[0]):
        return False

    nextPosition = movement.getNextPosition(edge[0], edge[1][0])
    if not imageWrapper.boundsChecker(image, nextPosition):
        return toBlackToken("edge")

    elif colors.isBlack(imageWrapper.getPixel(image, nextPosition)):
        return toBlackToken("toBlack")

    if colors.isWhite(imageWrapper.getPixel(image, nextPosition)):
        return toWhiteToken()

    colorChange = colors.getPixelChange(imageWrapper.getPixel(image, edge[0]), imageWrapper.getPixel(image, nextPosition))
    tokenType = getToken(colorChange['hueChange'], colorChange['lightChange'])
    return toColorToken(tokenType, len(imageWrapper.getCodel(image, edge[0])))
