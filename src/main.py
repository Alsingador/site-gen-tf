from textnode import TextNode  
from leafnode import LeafNode 


def main():
    text_node = TextNode("This is some anchor text", "link", url="https://www.boot.dev")
    print(text_node)
    


if __name__ == "__main__":
    main()
