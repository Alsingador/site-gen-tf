import unittest


from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_with_2_children(self):
        lnode0 = LeafNode("p", "Hello, world!")
        lnode1 = LeafNode("a", "A Link!", props={"hrfs":"https://www.fakeurl.notreal"})
        pnode = ParentNode("span", [lnode0, lnode1])
        self.assertEqual(pnode.to_html(), 
                         '<span><p>Hello, world!</p><a hrfs="https://www.fakeurl.notreal">A Link!</a></span>')


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
