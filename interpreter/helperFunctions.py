from typing import Union
import numpy as np

from interpreter import imageFunctions as imageWrapper
from interpreter import colors as colors
from interpreter import movementFunctions as movement
from interpreter import tokens as tokens
from interpreter import errors as errors
from interpreter.dataStructures import edge


def edgeToToken(image: np.ndarray, inputEdge: edge) -> Union[tokens.baseLexerToken, BaseException]:
    """
    This function creates a token based on the given edge
    :param image: input image
    :param inputEdge: an edge containing (coords, direction)
    :return: Either a newly created token, or an exception
    """
    if not imageWrapper.boundsChecker(image, inputEdge.edge[0]):
        return IndexError("Edge position {} is not in image".format(inputEdge.edge[0]))

    nextPosition = movement.getNextPosition(inputEdge.edge[0], inputEdge.edge[1].pointers[0])
    if not imageWrapper.boundsChecker(image, nextPosition):
        return tokens.toBlackToken("edge")

    pixel = imageWrapper.getPixel(image, nextPosition)

    if colors.isBlack(pixel):
        return tokens.toBlackToken("toBlack")

    if colors.isWhite(pixel):
        return tokens.toWhiteToken()

    if not colors.isColor(pixel):
        return tokens.toBlackToken("Unknown color")

    colorChange = colors.getPixelChange(imageWrapper.getPixel(image, inputEdge.edge[0]), imageWrapper.getPixel(image, nextPosition))
    if isinstance(colorChange, BaseException):
        # Modify existing error message with location
        newText = "{} at position {}".format(colorChange.args[0], nextPosition)
        return errors.UnknownColorError(newText)

    tokenType = tokens.getTokenType(colorChange['hueChange'], colorChange['lightChange'])
    return tokens.toColorToken(tokenType, len(imageWrapper.getCodel(image, inputEdge.edge[0]).codel))
