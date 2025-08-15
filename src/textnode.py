from enum import Enum


class TextType(Enum):
    BOLD  = '**Bold text**'
    Italic = '_Italic text_'
    Code = '`Code text`'


class TextNode():
    def __init__(self,text,text_type:TextType,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        

    def __eq__(self,other):
        if not isinstance(other, TextNode):
            return False
        return (
        other.text == self.text
        and other.url == self.url
        and other.text_type == self.text_type)

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'