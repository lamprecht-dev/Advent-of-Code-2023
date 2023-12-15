import sys
import collections

sys.path.append('../')
from utils import *


def s(d):
    ww = words(d, ",")[0]
    hash_sum = 0
    boxes = collections.defaultdict(dict)
    for w in ww:
        hash_value = hashing_value(w)
        lens_value = hashing_value(w[:w.index("=") if "=" in w else w.index("-")])

        if "=" in w:
            lens_focus = int(w[w.index("=")+1:])
            lens_name = w[:w.index("=")]
            boxes[lens_value][lens_name] = lens_focus
        else:
            lens_name = w[:w.index("-")]
            if lens_name in boxes[lens_value]:
                del boxes[lens_value][lens_name]
        hash_sum += hash_value

    focusing_power = 0
    for b in boxes:
        for i, l in enumerate(boxes[b]):
            focusing_power += (b + 1) * (i + 1) * boxes[b][l]

    return hash_sum, focusing_power


def hashing_value(st):
    current = 0
    for c in st:
        current += ord(c)
        current *= 17
        current %= 256
    return current


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = s(file)
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
    a1 = 1320
    a2 = 145
    return validate_solution(s(example), (a1, a2))


main()
