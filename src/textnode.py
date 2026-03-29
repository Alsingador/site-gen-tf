from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url


    def __eq__(self, other):
        eq = self.text == other.text
        eq = eq and self.text_type == other.text_type
        eq = eq and self.url == self.url
        return eq 


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    tag = None
    props = None
    match text_node.text_type:
        case TextType.TEXT:
            pass
        case TextType.BOLD:
            tag = "b"
        case TextType.ITALIC:
            tag = "i"
        case TextType.CODE:
            tag = "code"
        case TextType.LINK:
            tag = "a"
            props = {'href': text_node.url}
        case TextType.IMAGE:
            tag = "img"
            props = {'src': text_node.url, 'alt': text_node.text}
            return LeafNode(tag, "", props = props)
    return LeafNode(tag, text_node.text, props = props)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            break
        sub_texts = node.text.split(delimiter)
        if len(sub_texts)%2 == 0:
            raise Exception(f"Invalid Markdown: missmatched delimiter {delimiter} in: {node.text}")
        is_del_type = False
        for text in sub_texts:
            if is_del_type:
                new_nodes.append(TextNode(text, text_type))
            else:
                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))
            is_del_type = not is_del_type
    return new_nodes

