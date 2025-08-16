

def test():
    people = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
    html = []
    for i in people:
        html.append(f'{i}="{people[i]}" ')
    
    words = ''.join(html)
    return words
print(test())