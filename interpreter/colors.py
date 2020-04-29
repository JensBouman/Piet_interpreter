from typing import Dict

import numpy as np


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


def getPixelChange(colorStart: np.ndarray, colorEnd: np.ndarray) -> Dict[str, int]:
    pixelsColors = possiblePixels()


    if isWhite(colorStart) or isWhite(colorEnd):
        return {"hueChange": 0, "lightChange": 0}

    # Converting np arrays to common lists
    colorStart = list(colorStart)[:3]
    colorEnd = list(colorEnd)[:3]
    indexStart = pixelsColors.colors.index(colorStart)
    indexEnd = pixelsColors.colors.index(colorEnd)

    # Calculating hue and lightness changes
    hueChange = (int(indexEnd / 3) - int(indexStart / 3)) % 6
    lightChange = (indexEnd - indexStart) % 3

    return {"hueChange": hueChange, "lightChange": lightChange}


def isWhite(testColor: np.ndarray) -> bool:
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor == colors.white


def isBlack(testColor: np.ndarray) -> bool:
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor == colors.black


def isColor(testColor: np.ndarray) -> bool:
    colors = possiblePixels()
    testColor = list(testColor)[:3]
    return testColor in colors.colors
