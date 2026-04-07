from enum import Enum
import re

class BlockType(Enum):
    PARAG = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


class BlockNode:
    pass



def markdown_to_blocks(markdown):
    md_blocks = []
    for md in markdown.split('\n\n'):
        md = md.strip()
        if md == "":
            continue
        md_blocks.append(md)
    return md_blocks


def block_to_block_type(markdown):
    if markdown.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
        return BlockType.HEAD
    if markdown.startswith('```\n') and markdown.endswith('```'):
        return BlockType.CODE
    if markdown.startswith('>'):
        lines = len(re.findall(r'\n', repr(markdown)))
        qlines = len(re.findall(r'\n>', repr(markdown)))
        if lines == qlines:
            return BlockType.QUOTE
    elif markdown.startswith('- '):
        lines = len(re.findall('\n', markdown))
        ulines = len(re.findall('\n- ', markdown))
        if lines == ulines:
            return BlockType.ULIST

    counter = 1
    for line in markdown.split('\n'):
        if not line.startswith(f'{counter}. '):
            return BlockType.PARAG
        counter += 1
    return BlockType.OLIST


        
