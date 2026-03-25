from htmlnode import HTMLNode 

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if not self.value:
            raise ValueError()
        if not self.tag:
            return self.value
        prop_html = ""
        if self.props:
            prop_html = self.props_to_html()
        return f"<{self.tag}{prop_html}>{self.value}</{self.tag}>"


    def __repr__(self):
        rs = f"LeafNode(tag={self.tag}, value={self.value}, "
        rs = rs + f"props={self.props}"
        return rs
