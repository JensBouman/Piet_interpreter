class baseLexerToken():
    def __init__(self, tokenType: str):
        self.tokenType = tokenType

    def __str__(self):
        return "Token type = {}".format(self.tokenType)

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


def getTokenType(hueChange: int, lightChange: int) -> str:
    tokens = [
        ["noop", "push", "pop"],
        ["add", "subtract", "multiply"],
        ["divide", "mod", "not"],
        ["greater", "pointer", "switch"],
        ["duplicate", "roll", "inN"],
        ["inC", "outN", "outC"],
    ]
    return tokens[hueChange][lightChange]
