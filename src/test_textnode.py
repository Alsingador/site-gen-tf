import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
