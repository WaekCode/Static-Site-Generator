l = [["This has a `code block` and another `example` here"]]


for list in l:
    for sentence in list:
        convert = str(sentence)
        parts = convert.split("`")
        for i, part in enumerate(parts):
            if i % 2 == 1:  # odd indexes = inside backticks
                print("Inside:", part)
            else:           # even indexes = outside backticks
                print("Outside:", part)

