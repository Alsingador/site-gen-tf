from htmlnode import HTMLNode 

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing children")
        child_html = ""
        prop_html = ""
        for child in self.children:
            child_html = child_html + child.to_html()
        if self.props:
            prop_html = self.props_to_html()
        return f"<{self.tag}{prop_html}>{child_html}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag=},{self.children=},{self.props=})"
