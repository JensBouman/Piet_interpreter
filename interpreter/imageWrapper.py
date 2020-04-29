from typing import Tuple, Union, Set, List

from PIL import Image
import numpy as np

import interpreter.movement as movement
import interpreter.colors as colors


def boundsChecker(image: np.ndarray, position: Tuple[int, int]) -> bool:
    # Position 0 = x-axis, while matrix[0] = y-axis. This is why we compare position[0] with matrix[1]
    return 0 <= position[0] < image.shape[1] and \
           0 <= position[1] < image.shape[0]


def getPixel(image: np.ndarray, position: Tuple[int, int]) -> Union[np.ndarray, bool]:
    """
    This function the pixel at a specific location
    :param image: np.ndarray of image
    :param position: wanted position
    :return: either a cell or False, if the cell is not inside the image
    """
    if boundsChecker(image, position):
        return image[position[1]][position[0]]
    else:
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


def getCodel(image: np.ndarray, position: Tuple[int, int], foundPixels: Set[Tuple[int, int]] = None) -> Set[Tuple[int, int]]:
    """
    This function finds all adjacent pixels with the same color as the pixel on the given position

    If you pass a white pixel, this will return a set with only the white pixel in it.

    :param image: The image with all pixel values
    :param position: Starting position
    :param foundPixels: currently found pixels
    :return: A Set with all positions of same-colored pixels (Also known as a codel)
    """
    if foundPixels is None:
        foundPixels = set()

    # If this position is already in the set, it has already been traversed
    if position in foundPixels:
        return foundPixels

    if colors.isWhite(getPixel(image, position)):
        foundPixels.add(position)
        return foundPixels

    x = position[0]
    y = position[1]

    foundPixels.add(position)

    # right
    if boundsChecker(image, (x + 1, y)) and np.all(image[y][x + 1] == image[y][x]):
        newPosition = (position[0] + 1, position[1])
        foundPixels = foundPixels.union(getCodel(image, newPosition, foundPixels))

    # below
    if boundsChecker(image, (x, y - 1)) and np.all(image[y - 1][x] == image[y][x]):
        newPosition = (position[0], position[1] - 1)
        foundPixels = foundPixels.union(getCodel(image, newPosition, foundPixels))

    # left
    if boundsChecker(image, (x - 1, y)) and np.all(image[y][x - 1] == image[y][x]):
        newPosition = (position[0] - 1, position[1])
        foundPixels = foundPixels.union(getCodel(image, newPosition, foundPixels))

    # above
    if boundsChecker(image, (x, y + 1)) and np.all(image[y + 1][x] == image[y][x]):
        newPosition = (position[0], position[1] + 1)
        foundPixels = foundPixels.union(getCodel(image, newPosition, foundPixels))

    return foundPixels


def getWhiteLine(image: np.ndarray, startPosition: Tuple[int, int], directionPointer: int, foundPixels: List[Tuple[int, int]] = None) -> List[Tuple[int, int]]:
    """
    Finds all adjacent white pixels in the same direction
    :param image: base image
    :param startPosition: Starting position from which the white line starts
    :param directionPointer: Direction in which the line goes
    :param foundPixels: already found pixels
    :return: A list of white pixels found
    """

    # Can't give mutable values as default parameter
    if foundPixels is None:
        foundPixels = []

    # If it is already found, skip
    if startPosition in foundPixels:
        return foundPixels

    foundPixels.append(startPosition)

    # Get the new position, and check if the colors match
    newPos = movement.getNextPosition(startPosition, directionPointer)
    if boundsChecker(image, newPos) and colors.isWhite(image[newPos[1]][newPos[0]]):
        return getWhiteLine(image, newPos, directionPointer, foundPixels)
    else:
        return foundPixels


def getNewWhiteDirection(image: np.ndarray, startPosition: Tuple[int, int], directionPointer: int) -> int:
    newPosition = movement.getNextPosition(startPosition, directionPointer)

    if boundsChecker(image, newPosition) and (not colors.isBlack(getPixel(image, newPosition))):
        return directionPointer
    else:
        return getNewWhiteDirection(image, startPosition, movement.flipDP(directionPointer))

