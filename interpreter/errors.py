

class UnknownColorError(BaseException):
    """Raise this when a color is found that is not one of the 18 allowed colors"""

class CommandNotFoundError(BaseException):
    """Raise this when a command of an token is unknown"""

class UnknownTokenError(BaseException):
    """Raise this when a token is unknown"""

class inBlackPixelError(BaseException):
    """Raise this when a programstate begins inside a black pixel"""
