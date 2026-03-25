class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children 
        self.props = props 


    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if not self.props:
            return ""
        prop_str = ""
        for p in self.props:
            prop_str = prop_str +f" {p}=\"{self.props[p]}\""
        return prop_str


    def __repr__(self):
        rs = f"HTMLNode(tag={self.tag}, value={self.value}, "
        if self.children:
            rs = rs + f"children=["
            for c in self.children:
                rs = rs + f"\n - {c}"
            rs = rs + f"\n], "
        else:
            rs = rs + f"children={self.children}, "
        if self.props:
            rs = rs + "props={"
            for p in self.props:
                rs = rs + f"\n - {p}"
            rs = rs + "\n}"
        else:
            rs = rs + f"props={self.props}"
        return rs
