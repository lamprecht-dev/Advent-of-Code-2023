import os


def solve(inp):
    total = 0
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    for line in inp.split("\n"):
        first = None
        last = None

        for i in range(len(line)):
            for j in range(5):
                val = line[i:i+j + 1]
                if val.isnumeric():
                    last = val
                    if first is None:
                        first = val

                if val in digits:
                    string_val = digits.index(val)
                    last = string_val
                    if first is None:
                        first = string_val

        total += int(first) * 10 + int(last)

    return total


with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    print(solve(f.read().strip()))
