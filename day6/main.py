from utils import *


def solve(d):
    ways_to_beat = 1
    ways_to_beat2 = 0

    btime = ""
    bthresh = ""

    ww = words(d)
    for i in range(1, len(ww[0])):
        btime = btime + ww[0][i]
        bthresh = bthresh + ww[1][i]
        wtb = 0
        time, threshold = int(ww[0][i]), int(ww[1][i])
        for t in range(time):
            distance = (time - t) * t
            if distance > threshold:
                wtb += 1
        ways_to_beat *= wtb

    btime = int(btime)
    bthresh = int(bthresh)

    for t in range(btime):
        distance = (btime - t) * t
        if distance > bthresh:
            ways_to_beat2 += 1

    return ways_to_beat, ways_to_beat2


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
