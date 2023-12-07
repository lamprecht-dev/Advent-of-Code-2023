from utils import *


def solve(d):
    wtb = 1

    btime = ""
    bthresh = ""

    ww = words(d)
    for i in range(1, len(ww[0])):
        btime = btime + ww[0][i]
        bthresh = bthresh + ww[1][i]
        wtb *= ways_to_beat_simple(int(ww[0][i]), int(ww[1][i]))

    return wtb, ways_to_beat_binary_search(int(btime), int(bthresh))


def ways_to_beat_binary_search(time, threshold):
    # Since the values will have symitry it is easier to just search on one side at a time
    # We want to move two pointers towards one another until we find the spot where they are just beating the thresh

    bottom = 0  # Not beating threshold
    top = time // 2  # Beating threshold

    # check if top is also inside threshold
    if top * (time - top) <= threshold:
        return 0

    while top - bottom > 1:
        half = (top + bottom) // 2
        dist = half * (time - half)

        if dist > threshold:
            top = half
        else:
            bottom = half

    # top now really is the bottom part of the range. Top is mirrored on the other side
    return time - (2 * top) + 1


def ways_to_beat_simple(time, threshold):
    wtb = 0
    for t in range(time):
        distance = (time - t) * t
        if distance > threshold:
            wtb += 1

    return wtb


def main():
    if test():
        solutions = solve(inp(os.path.join(os.path.dirname(__file__), 'input.txt')))
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for s in solutions:
            print(s)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    s = """Time:      7  15   30
Distance:  9  40  200"""
    a1 = 288
    a2 = 71503
    return validate_solution(solve(s), (a1, a2))


main()
