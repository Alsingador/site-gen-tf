import unittest

from blocks import *


class TestBlocks(unittest.TestCase):
    def test_md_to_block(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

        md = " "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

        md = " \n\n "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


    def test_block_to_blocktype(self):
        text = "just text \nin two lines"
        self.assertEqual(BlockType.PARAG, block_to_block_type(text))
        headline1 = "# headline"
        self.assertEqual(BlockType.HEAD, block_to_block_type(headline1))
        headline6 = "###### headline \nin two lines"
        self.assertEqual(BlockType.HEAD, block_to_block_type(headline6))
        headline7 = "####### headlone"
        self.assertEqual(BlockType.PARAG, block_to_block_type(headline7))

        code = "```\n code```"
        self.assertEqual(BlockType.CODE, block_to_block_type(code))
        code_not1 = "```code```"
        self.assertEqual(BlockType.PARAG, block_to_block_type(code_not1))
        code_not2 = "```\n code```and"
        self.assertEqual(BlockType.PARAG, block_to_block_type(code_not2))
        code_not3 = "``` \n code```"
        self.assertEqual(BlockType.PARAG, block_to_block_type(code_not3))

        quote = "> aq"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote))
        quote3 = ">aq \n> bq \n>  cq"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote3))
        not_quote1 = "aq \n> bq \n>  cq"
        self.assertEqual(BlockType.PARAG, block_to_block_type(not_quote1))

        ulist1 = "- 1"
        self.assertEqual(BlockType.ULIST, block_to_block_type(ulist1))
        ulist4 = "- 1 \n- 2 \n- 3 \n- 4"
        self.assertEqual(BlockType.ULIST, block_to_block_type(ulist4))
        ulist2 = "- 1 - 2 \n- 3 - 4"
        self.assertEqual(BlockType.ULIST, block_to_block_type(ulist2))
        not_ulist3 = "- 1 \n- 2 \n- 3 \n"
        self.assertEqual(BlockType.PARAG, block_to_block_type(not_ulist3))
        not_ulist2 = "- 1 \n-2 \n- 3"
        self.assertEqual(BlockType.PARAG, block_to_block_type(not_ulist2))

        olist1 = "1. a"
        self.assertEqual(BlockType.OLIST, block_to_block_type(olist1))
        olist4 = "1. a \n2. b\n3. c\n4. d"
        self.assertEqual(BlockType.OLIST, block_to_block_type(olist4))
        not_olist4 = "1. a \n2. b\n3. c\n4. d\n"
        self.assertEqual(BlockType.PARAG, block_to_block_type(not_olist4))
        not_olist3 = "1. a \n2. b\n3.c"
        self.assertEqual(BlockType.PARAG, block_to_block_type(not_olist3))
