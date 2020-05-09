from typing import Union
from PIL import Image
import numpy as np

import interpreter.colors as colors
from interpreter.dataStructures import position, codel


def boundsChecker(image: np.ndarray, inputPosition: position) -> bool:
    # Position 0 = x-axis, while matrix[0] = y-axis. This is why we compare coords[0] with matrix[1]
    return 0 <= inputPosition.coords[0] < image.shape[1] and \
           0 <= inputPosition.coords[1] < image.shape[0]


def getPixel(image: np.ndarray, inputPosition: position) -> Union[np.ndarray, bool]:
    """
    This function the pixel at a specific location
    :param image: np.ndarray of image
    :param coords: wanted coords
    :return: either a cell or False, if the cell is not inside the image
    """
    if boundsChecker(image, inputPosition):
        return image[inputPosition.coords[1]][inputPosition.coords[0]]
    return False


def getImage(fileName: str) -> np.ndarray:
    """
    Returns an np.ndarray of the image found at the given file location
    :param fileName: Complete filename (including extension)
    :return: np.ndarray of the image
    """
    image = Image.open(fileName)
    if fileName.split('.')[-1] == "gif":
        image = image.convert("RGB")
    return np.array(image)


def getCodel(image: np.ndarray, inputPosition: position, foundPixels: codel = None) -> codel:
    """
    This function finds all adjacent pixels with the same color as the pixel on the given coords

    If you pass a white pixel, this will return a set with only the white pixel in it.

    :param image: The image with all pixel values
    :param coords: Starting coords
    :param foundPixels: currently found pixels
    :return: A Set with all positions of same-colored pixels (Also known as a codel)
    """
    if foundPixels is None:
        foundPixels = codel(set())

    # If this coords is already in the set, it has already been traversed
    if inputPosition in foundPixels.codel:
        return foundPixels

    # Adjacent white colors don't form a codel
    if colors.isWhite(getPixel(image, inputPosition)):
        foundPixels.codel.add(inputPosition)
        return foundPixels

    x = inputPosition.coords[0]
    y = inputPosition.coords[1]

    foundPixels.codel.add(inputPosition)

    # right
    if boundsChecker(image, position((x + 1, y))) and np.all(image[y][x + 1] == image[y][x]):
        newPosition = position((inputPosition.coords[0] + 1, inputPosition.coords[1]))
        foundPixels = codel(foundPixels.codel.union(getCodel(image, newPosition, foundPixels).codel))

    # below
    if boundsChecker(image, position((x, y - 1))) and np.all(image[y - 1][x] == image[y][x]):
        newPosition = position((inputPosition.coords[0], inputPosition.coords[1] - 1))
        foundPixels = codel(foundPixels.codel.union(getCodel(image, newPosition, foundPixels).codel))

    # left
    if boundsChecker(image, position((x - 1, y))) and np.all(image[y][x - 1] == image[y][x]):
        newPosition = position((inputPosition.coords[0] - 1, inputPosition.coords[1]))
        foundPixels = codel(foundPixels.codel.union(getCodel(image, newPosition, foundPixels).codel))

    # above
    if boundsChecker(image, position((x, y + 1))) and np.all(image[y + 1][x] == image[y][x]):
        newPosition = position((inputPosition.coords[0], inputPosition.coords[1] + 1))
        foundPixels = codel(foundPixels.codel.union(getCodel(image, newPosition, foundPixels).codel))

    return foundPixels
