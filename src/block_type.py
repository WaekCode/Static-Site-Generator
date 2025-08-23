from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block): 
    isit = True
    isitunord = True
    isorderd = True
    count = 1
    quuto = block.split('\n')
    for line in quuto:
        if not line.startswith('>'):
            isit = False
        if not line.startswith('- '):
            isitunord = False

        if line.startswith(f"{count}. "):
            count += 1
        else:
            isorderd = False

    for n in range(1, 7):
        if block.startswith("#" * n + " "):
            return BlockType.HEADING

  
        
    if block.startswith(3*'`') and block.endswith(3*'`'):
        return BlockType.CODE
    elif isorderd:
        return BlockType.ORDERED_LIST
    elif isit:
        return BlockType.QUOTE
    elif isitunord:
        return BlockType.UNORDERED_LIST

    else:
        return BlockType.PARAGRAPH
      
