import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is node has url", TextType.LINK, "fake_url")
        node4 = TextNode("This is node has url", TextType.IMAGE, "fake_url")

        self.assertEqual(node, node2)
        self.assertEqual(repr(node),repr(node2))
        self.assertEqual(node, node1)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node3)


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node1 = TextNode("Bold", TextType.BOLD)
        html_node1 = text_node_to_html_node(node1)
        self.assertEqual(html_node1.tag, 'b')
        
        node2 = TextNode("alt text", TextType.IMAGE, "fake_url")
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, 'img')
        self.assertEqual(html_node2.value, "")
        self.assertEqual(html_node2.props['alt'], "alt text")
        self.assertEqual(html_node2.props['src'], "fake_url")


    def test_split(self):
        #test empty
        empty = []
        self.assertEqual(split_nodes_delimiter(empty, '**', TextType.BOLD), empty)

        #bold in text
        node0 = TextNode("Test with **BOLD** word", TextType.TEXT)
        input = [node0]
        split0 = split_nodes_delimiter(input, '**', TextType.BOLD)
        expected_split0 = [
            TextNode("Test with ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split0, expected_split0)

        node1 = TextNode("Test **with** two **BOLD** words", TextType.TEXT)
        input = [node1]
        split1 = split_nodes_delimiter(input, '**', TextType.BOLD)
        expected_split1 = [
            TextNode("Test ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" two ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertEqual(split1, expected_split1)

        node0 = TextNode("**JUST BOLD**", TextType.TEXT)
        input = [node0]
        split0 = split_nodes_delimiter(input, '**', TextType.BOLD)
        expected_split0 = [
            #TextNode("", TextType.TEXT),
            TextNode("JUST BOLD", TextType.BOLD),
            #TextNode("", TextType.TEXT),
        ]
        self.assertEqual(split0, expected_split0)

        #delimiter misssmatch
        node0 = TextNode("**JUST BOLD?*", TextType.TEXT)
        input = [node0]
        with self.assertRaises(Exception):
            split0 = split_nodes_delimiter(input, '**', TextType.BOLD)



    def test_split_link(self):
        node0 = TextNode("just text", TextType.TEXT)
        self.assertEqual([node0],split_nodes_link([node0]))
        node1 = TextNode("[just](link)", TextType.TEXT)
        ans1 = [
            TextNode("", TextType.TEXT),
            TextNode("just", TextType.LINK, "link"),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(ans1,split_nodes_link([node1]))
        node2 = TextNode("2 [a](b) link [c](d) here", TextType.TEXT)
        ans2 = [
            TextNode("2 ", TextType.TEXT),
            TextNode("a", TextType.LINK, "b"),
            TextNode(" link ", TextType.TEXT),
            TextNode("c", TextType.LINK, "d"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(ans2,split_nodes_link([node2]))
        self.assertEqual(ans1+ans2, split_nodes_link([node1, node2]))


    def test_split_img(self):
        node0 = TextNode("just text", TextType.TEXT)
        self.assertEqual([node0],split_nodes_image([node0]))
        node1 = TextNode("![just](img)", TextType.TEXT)
        ans1 = [
            TextNode("", TextType.TEXT),
            TextNode("just", TextType.IMAGE, "img"),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(ans1,split_nodes_image([node1]))
        node2 = TextNode("2 ![a](b) imgs ![c](d) here", TextType.TEXT)
        ans2 = [
            TextNode("2 ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "b"),
            TextNode(" imgs ", TextType.TEXT),
            TextNode("c", TextType.IMAGE, "d"),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(ans2,split_nodes_image([node2]))
        self.assertEqual(ans1+ans2, split_nodes_image([node1, node2]))


class TestTextToNodes(unittest.TestCase):
    def test_text_to_nodes(self):
        bold_text = "**bold**"
        bold_node = TextNode("bold", TextType.BOLD)
        self.assertEqual(text_to_textnodes(bold_text), [bold_node])
        italic_text = "_italic_"
        italic_node = TextNode("italic", TextType.ITALIC)
        self.assertEqual(text_to_textnodes(italic_text), [italic_node])
        code_text = "`code`"
        code_node = TextNode("code", TextType.CODE)
        self.assertEqual(text_to_textnodes(code_text), [code_node])

        enode = TextNode("", TextType.TEXT)
        img_text = "![img](path)"
        img_node = TextNode("img", TextType.IMAGE, "path")
        self.assertEqual(text_to_textnodes(img_text), [enode, img_node, enode])
        link_text = "[link](url)"
        link_node = TextNode("link", TextType.LINK, "url")
        self.assertEqual(text_to_textnodes(link_text), [enode, link_node, enode])

        text = " and ".join([bold_text, italic_text, code_text, img_text, link_text])
        anode = TextNode(" and ", TextType.TEXT)
        text_nodes = [bold_node, anode, italic_node, anode, code_node, anode, img_node, anode, link_node, enode]
        self.assertEqual(text_to_textnodes(text), text_nodes)


class TestTextFunctions(unittest.TestCase):
    def test_md_img_extraction(self):
        empty = ""
        self.assertEqual([],extract_markdown_images(empty))
        just_img = "![a](b)"
        self.assertEqual([('a','b')],extract_markdown_images(just_img))
        just_link = "[a](b)"
        self.assertEqual([],extract_markdown_images(just_link))
        img_in_txt = "see ![a](b) image"
        self.assertEqual([('a','b')],extract_markdown_images(img_in_txt))
        two_img_in_txt = "see ![a](b) and ![c](d) here"
        self.assertEqual([('a','b'),('c','d')],extract_markdown_images(two_img_in_txt))
        


    def test_md_link_extraction(self):
        empty = ""
        self.assertEqual([],extract_markdown_links(empty))
        just_img = "![a](b)"
        self.assertEqual([],extract_markdown_links(just_img))
        just_link = "[a](b)"
        self.assertEqual([('a','b')],extract_markdown_links(just_link))
        link_in_txt = "see [a](b) link"
        self.assertEqual([('a','b')],extract_markdown_links(link_in_txt))
        two_link_in_txt = "click [a](b) and [c](d) here"
        self.assertEqual([('a','b'),('c','d')],extract_markdown_links(two_link_in_txt))


if __name__ == "__main__":
    unittest.main()
