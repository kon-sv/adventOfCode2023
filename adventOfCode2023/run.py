lex = [
    None,
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
]


def expand(line: str):
    newline = ""
    for t in line:
        newline = newline + t
        for (k, v) in enumerate(lex):
            if v is not None:
                newline = newline.replace(v, str(k))
    return newline

def decode(text: str):
    newline = text
    for (k, v) in enumerate(lex):
        if v is not None:
            newline = newline.replace(v, str(k))
    return newline

def extract_digit(text, lexical=True) -> int:
    if lexical:
        text = decode(text)
    for t in text:
        if t.isdigit():
            return int(t)
    return -1


def test(line: str, lexical=False) -> (int, int):
    left = ""
    right = ""
    length = len(line) - 1
    left_digit = right_digit = -1
    for i,v in enumerate(line):
        left = left + line[i]
        right = line[length - i] + right

        if left_digit is None or left_digit == -1:
            left_digit = extract_digit(left, lexical)
        if right_digit is None or right_digit == -1:
            right_digit = extract_digit(right, lexical)

        # print(left, right)

    if left_digit == -1 or right_digit == -1:
        raise Exception("Error")
    
    return (left_digit, right_digit)

def calculate():
    s = 0
    with open("input.txt") as f:
        for rawline in f.readlines():
            nums = test(rawline, True)
            print(nums)
            num = int(str(nums[0]) + str(nums[1]))
            s = sum([s, num])
    return s
    
print(extract_digit("nine"))
test("7pqrstsixteen", True)
print(calculate())
