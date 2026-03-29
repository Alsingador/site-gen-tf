import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
