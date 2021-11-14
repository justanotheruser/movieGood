import lxml


class InvalidLinkException(Exception):
    def __init__(self, url: str, message: str):
        self.url = url
        self.message = message
        super().__init__(message)


class ParsingFailedException(Exception):
    def __init__(self, url: str, tree: lxml.etree._ElementTree, message: str):
        self.url = url
        self.tree = tree
        self.message = message
        super().__init__(message)
