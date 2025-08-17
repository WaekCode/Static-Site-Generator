class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise  NotImplementedError() 

    def props_to_html(self):
        if not self.props:
            return ''
        html = []
        for i in self.props:
            html.append(f'{i}="{self.props[i]}"')
        words = ' '+' '.join(html)

        return words
    
    def __repr__(self):
        return f'HTMLNODE({self.tag},{self.value},{self.children},{self.props})'
    


class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    
    def to_html(self):
        if self.value is None:  # Only check for None, not empty string
            raise ValueError("invalid HTML: no value")
        elif self.tag is None:
            return self.value
        else:
            props_str = self.props_to_html()
            return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
        



class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        elif self.children is None:
            raise ValueError("invalid HTML: no children")
        
        attrs = self.props_to_html()
        
        #iterativly
        html_string = []
        for child in self.children:
            html_string.append(child.to_html())

        html_line = ''.join(html_string)

        return f"<{self.tag}{attrs}>{html_line}</{self.tag}>"
        # # Recursively get HTML for all children
        # children_html = ''.join(child.to_html() for child in self.children)
        
        # # Wrap children with parent tag and return
        # return f"<{self.tag}{attrs}>{children_html}</{self.tag}>"

