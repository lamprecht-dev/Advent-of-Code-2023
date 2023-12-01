from utils import *


def solve(d):
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    total = 0
    big_total = 0

    ll = lines(d)
    for line in ll:
        first = None
        last = None
        first_digit = None
        last_digit = None

        for i in range(len(line)):
            for j in range(5):
                val = line[i:i+j + 1]
                if val.isnumeric() and j == 0:
                    last_digit = val
                    last = val
                    if first_digit is None:
                        first_digit = val
                    if first is None:
                        first = val

                if val in digits:
                    string_val = digits.index(val)
                    last = string_val
                    if first is None:
                        first = string_val

        if first_digit is not None and last_digit is not None:
            total += int(first_digit) * 10 + int(last_digit)
        big_total += int(first) * 10 + int(last)

    return total, big_total


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

    s2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
    a1 = 142
    a2 = 281
    return validate_solution((solve(s)[0], solve(s2)[1]), (a1, a2))


main()
