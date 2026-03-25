import unittest


from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_htm(self):
        node0 = HTMLNode(props = {'a': 'test a', 'b': 'test b'})
        node1 = HTMLNode(props = {'a': 'test a', 'b': 'test b'})

        self.assertEqual(node0.props_to_html(),node1.props_to_html())
