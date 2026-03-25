import unittest


from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node0 = LeafNode("p", "Hello, world!")
        node1 = LeafNode("a", "A Link!", props={"hrfs":"https://www.fakeurl.notreal"})
        
        self.assertEqual(node0.to_html(), "<p>Hello, world!</p>")
        self.assertNotEqual(node1.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node1.to_html(), '<a hrfs="https://www.fakeurl.notreal">A Link!</a>')
