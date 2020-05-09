from typing import Dict, Union

import numpy as np

from interpreter import errors as errors

class possiblePixels:
    def __init__(self):
        self.colors = [
            [255, 192, 192],  # Light red
            [255, 0, 0],  # Red
            [192, 0, 0],  # Dark red
            [255, 255, 192],  # Light yellow
            [255, 255, 0],  # Yellow
            [192, 192, 0],  # Dark yellow
            [192, 255, 192],  # Light green
            [0, 255, 0],  # Green
            [0, 192, 0],  # Dark green
            [192, 255, 255],  # Light cyan
            [0, 255, 255],  # Cyan
            [0, 192, 192],  # Dark cyan
            [192, 192, 255],  # Light blue
            [0, 0, 255],  # Blue
            [0, 0, 192],  # Dark blue
            [255, 192, 255],  # Light magenta
            [255, 0, 255],  # Magenta
            [192, 0, 192]  # Dark magenta
        ]
        self.white = [255, 255, 255]
        self.black = [0, 0, 0]


def getPixelChange(colorStart: np.ndarray, colorEnd: np.ndarray) -> Union[Dict[str, int], BaseException]:
    """
    Gets the Hue change and the light change from two different colors
    :param colorStart: Starting color
    :param colorEnd: Final color
    :return: Either a dictionary {'hueChange': int, 'lightChange': int}, or an Exception
    """
    if type(colorStart) is not np.ndarray:
        return TypeError("Start color is not of type np.ndarray, but {}".format(type(colorStart)))
    if type(colorEnd) is not np.ndarray:
        return TypeError("End color is not of type np.ndarray, but {}".format(type(colorStart)))
    if len(colorStart) < 3:
        return ValueError("Start color does contain at least 3 values, but {}".format(colorStart))
    if len(colorEnd) < 3:
        return ValueError("Start color does contain at least 3 values, but {}".format(colorEnd))


    # If either the starting or leaving color is white, there is no change (It is considered a noop)
    if isWhite(colorStart) or isWhite(colorEnd):
        return {"hueChange": 0, "lightChange": 0}

    pixelsColors = possiblePixels()
    # Converting np arrays to normal lists
    colorStart = list(colorStart)[:3]
    colorEnd = list(colorEnd)[:3]

    if colorStart not in pixelsColors.colors:
        return errors.UnknownColorError("Color {} is not recognized as a correct color".format(colorStart))
    if colorEnd not in pixelsColors.colors:
        return errors.UnknownColorError("Color {} is not recognized as a correct color".format(colorEnd))

    indexStart = pixelsColors.colors.index(colorStart)
    indexEnd = pixelsColors.colors.index(colorEnd)

    # Calculating hue and lightness changes
    hueChange = (int(indexEnd / 3) - int(indexStart / 3)) % 6
    lightChange = (indexEnd - indexStart) % 3

    return {"hueChange": hueChange, "lightChange": lightChange}


def isWhite(testColor: np.ndarray) -> bool:
    """
    Compares the color to white
    :param testColor: Input color
    :return: Boolean whether the input color is white (255, 255, 255)
    """
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor == colors.white


def isBlack(testColor: np.ndarray) -> bool:
    """
    Compares the color to black
    :param testColor: Input color
    :return: Boolean whether the input color is black (0, 0, 0)
    """
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor == colors.black


def isColor(testColor: np.ndarray) -> bool:
    """
    Compares the color to the 18 pre-defined Piet colors
    :param testColor: Input color
    :return: Boolean whether the input color is a Piet-color
    """
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor in colors.colors
