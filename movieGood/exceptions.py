from typing import Union

import lxml


class InvalidLinkException(Exception):
    def __init__(self, url: str, message: str):
        self.url = url
        self.message = message
        super().__init__(message)


class ParsingFailedException(Exception):
    def __init__(self, url: str, xml: Union[lxml.etree._ElementTree, lxml.etree._Element], message: str):
        self.url = url
        if isinstance(xml, lxml.etree._Element):
            xml = lxml.etree.ElementTree(xml)
        self.tree = xml
        self.message = message
        super().__init__(message)
