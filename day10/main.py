import sys
sys.path.append('../')
from utils import *


def s(d):
    ll = lines(d)
    loop_items = find_loop(ll)
    ll = sanitize_grid(ll, loop_items)
    inside_count = count_inside(ll)

    return len(loop_items) // 2, inside_count


class DisjSet:
    def __init__(self, rows, cols):
        self.parent = [i for i in range(rows * cols)]
        self.rows = rows

    def find(self, el):
        if not isinstance(el, int):
            el = el[0] * self.rows + el[1]
        if self.parent[el] is not el:
            self.parent[el] = self.find(self.parent[el])  # Path Shortening

        return self.parent[el]

    def union(self, a, b):
        pa = self.find(a)
        pb = self.find(b)
        if pa == pb:
            return False
        self.parent[pa] = pb
        return self.parent[pa]

    def get_all(self, el):
        el = self.find(el)
        return [(i // self.rows, i % self.rows) for i in range(len(self.parent)) if self.find(i) == el]


def find_loop(ll):
    ds = DisjSet(len(ll), len(ll[0]))
    loop_items = []
    for r, l in enumerate(ll):
        for c, ch in enumerate(l):
            # Only union top and right.
            true_neighbors = get_true_neighbor((c, r), ll)
            for tni in true_neighbors:
                tn = true_neighbors[tni]
                if tni in ["r", "u"]:
                    could_union = ds.union((c, r), tn)
                    if could_union is False:
                        loop_items = ds.get_all(tn)
    return loop_items


def sanitize_grid(ll, loop_items):
    # Find and replace S
    S_dirs = set()
    S_coord = None
    for r, l in enumerate(ll):
        for c, ch in enumerate(l):
            # Empty anything non-loop
            if (c, r) not in loop_items:
                ll[r] = ll[r][:c] + "." + ll[r][c + 1:]

            if ch != "S":
                continue
            S_coord = (c, r)
            true_neighbors = get_true_neighbor((c, r), ll)
            for tni in true_neighbors:
                tn = true_neighbors[tni]
                if tn in loop_items:
                    S_dirs.add(tni)
    for d in "|-7LFJ":
        if get_directions(d) == S_dirs:
            ll[S_coord[1]] = ll[S_coord[1]][:S_coord[0]] + d + ll[S_coord[1]][S_coord[0] + 1:]
            break
    return ll


def count_inside(ll):
    inside_count = 0
    for r, l in enumerate(ll):
        inside = False
        for c, ch in enumerate(l):
            if ch == ".":
                inside_count += inside
            elif ch in "|JL":
                inside = not inside
    return inside_count


def get_directions(pipe):
    if pipe == "S":
        return {"u", "d", "r", "l"}
    if pipe == "|":
        return {"u", "d"}
    if pipe == "-":
        return {"r", "l"}
    if pipe == "F":
        return {"r", "d"}
    if pipe == "L":
        return {"r", "u"}
    if pipe == "J":
        return {"u", "l"}
    if pipe == "7":
        return {"d", "l"}
    return {}


def get_neighbors(loc, ll):
    neighbors = {}
    for di in get_directions(ll[loc[1]][loc[0]]):
        d = dirs[di]
        nc, nr = loc[0] + d[0], loc[1] + d[1]
        if not (0 <= nc < len(ll[0]) and 0 <= nr < len(ll)):
            continue
        neighbors[di] = (nc, nr)
    return neighbors


def get_true_neighbor(loc, ll):
    neighbors = get_neighbors(loc, ll)
    true_neighbors = {}
    for n in neighbors:
        nc, nr = neighbors[n]
        neighbors_neighbors = get_neighbors((nc, nr), ll)
        for nn in neighbors_neighbors:
            if does_fit(n, nn):
                true_neighbors[n] = (nc, nr)
    return true_neighbors


def does_fit(a, b):
    if (a == "r" and b == "l" or
            a == "l" and b == "r" or
            a == "u" and b == "d" or
            a == "d" and b == "u"):
        return True
    return False


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
    example = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""
    example2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    a1 = 8
    a2 = 10
    return validate_solution((s(example)[0], s(example2)[1]), (a1, a2))

main()
