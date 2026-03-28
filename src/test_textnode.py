import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()
