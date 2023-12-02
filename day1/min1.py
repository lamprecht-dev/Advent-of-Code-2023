import os


def solve(inp):
    total = 0

    for line in inp.split("\n"):
        first = None
        last = None

        for i in range(len(line)):
            val = line[i:i + 1]
            if val.isnumeric():
                last = val
                if first is None:
                    first = val

        total += int(first) * 10 + int(last)

    return total


with open(os.path.join(os.path.dirname(__file__), 'input.txt')) as f:
    print(solve(f.read().strip()))
