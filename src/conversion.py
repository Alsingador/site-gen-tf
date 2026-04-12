from blocks import *
from parentnode import *
from textnode import *


def make_nodes_for_block_type(md_block, block_type):
    match block_type:
        case BlockType.PARAG:
            md_block = md_block.replace("\n", " ")
            leaf_nodes = text_to_leaf_nodes(md_block)
            return ParentNode("p", leaf_nodes)

        case BlockType.HEAD:
            i = 0
            while md_block[i] == '#':
                i+=1
            md_block = md_block.lstrip('# ')
            leaf_nodes = text_to_leaf_nodes(md_block)
            return ParentNode(f"h{i}", leaf_nodes)

        case BlockType.CODE:
            md_block = md_block.strip('`')
            md_block = md_block.lstrip('\n')
            code_text = TextNode(md_block, TextType.CODE)
            code_leaf = [text_node_to_html_node(code_text)]
            return ParentNode("pre", code_leaf)

        case BlockType.QUOTE:
            lines = [line.lstrip('>') for line in md_block.split('\n')]
            leaf_nodes = text_to_leaf_nodes(" ".join(lines))
            return ParentNode("blockquote", quote_line_nodes)

        case BlockType.ULIST:
            lines = [line[2:] for line in md_block.split('\n')]
            item_nodes = []
            for line in lines:
                leaf_nodes = text_to_leaf_nodes(line)
                item_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ul", item_nodes)

        case BlockType.OLIST:
            lines = [line[3:] for line in md_block.split('\n')]
            item_nodes = []
            for line in lines:
                leaf_nodes = text_to_leaf_nodes(line)
                item_nodes.append(ParentNode("li", leaf_nodes))
            return ParentNode("ol", item_nodes)


def text_to_leaf_nodes(md):
    text_nodes = text_to_textnodes(md)
    return list(map(text_node_to_html_node, text_nodes))


def block_and_type(block_md):
    return (block_md, block_to_block_type(block_md))


def markdown_to_html_node(markdown):
    bnts = map(block_and_type, markdown_to_blocks(markdown))
    block_nodes = []
    for bnt in bnts:
        block_nodes.append(make_nodes_for_block_type(*bnt))
    return ParentNode("div", block_nodes)

