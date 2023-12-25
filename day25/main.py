import sys
import collections
import networkx as nx
sys.path.append('../')
from utils import *


# https://www.geeksforgeeks.org/disjoint-set-data-structures/
class DisjSet:
    def __init__(self, n):
        # Constructor to create and
        # initialize sets of n items
        self.rank = [1] * n
        self.parent = [i for i in range(n)]

    # Finds set of given item x
    def find(self, x):

        # Finds the representative of the set
        # that x is an element of
        if (self.parent[x] != x):
            # if x is not the parent of itself
            # Then x is not the representative of
            # its set,
            self.parent[x] = self.find(self.parent[x])

            # so we recursively call Find on its parent
            # and move i's node directly under the
            # representative of this set

        return self.parent[x]

    # Do union of two sets represented
    # by x and y.
    def Union(self, x, y):

        # Find current sets of x and y
        xset = self.find(x)
        yset = self.find(y)

        # If they are already in same set
        if xset == yset:
            return

        # Put smaller ranked item under
        # bigger ranked item if ranks are
        # different
        if self.rank[xset] < self.rank[yset]:
            self.parent[xset] = yset

        elif self.rank[xset] > self.rank[yset]:
            self.parent[yset] = xset

        # If ranks are same, then move y under
        # x (doesn't matter which one goes where)
        # and increment rank of x's tree
        else:
            self.parent[yset] = xset
            self.rank[xset] = self.rank[xset] + 1


def s(d):
    G = nx.Graph()

    ll = lines(d)
    nodes = set()
    connections = {}
    for line in ll:
        a, bs = line.split(": ")
        b = bs.split(" ")
        nodes.add(a)
        connections[a] = b
        for bb in b:
            nodes.add(bb)
            G.add_edge(a, bb)

    # Remove Edges
    remove_edges = nx.minimum_edge_cut(G) # Karger Algorithm
    for re in remove_edges:
        if re[0] in connections and re[1] in connections[re[0]]:
            connections[re[0]].remove(re[1])
        else:
            connections[re[1]].remove(re[0])

    # Find how many in each set
    nodes = list(nodes)
    djs = DisjSet(len(nodes))

    for con in connections:
        for c in connections[con]:
            djs.Union(nodes.index(con), nodes.index(c))

    # Count the connections
    cnt = collections.Counter()
    for p in djs.parent:
        cnt[djs.find(p)] += 1

    return math.prod(cnt.values())


def main():
    if test():
        file = inp(os.path.join(os.path.dirname(__file__), 'input.txt'))
        solutions = [s(file)]
        print("\n\n" + BColors.HEADER + "Solutions" + BColors.ENDC)
        for sol in solutions:
            print(sol)
    else:
        print("\n\n" + BColors.FAIL + "Not All Test Successful" + BColors.ENDC)


def test():
    example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    a1 = 54
    return validate_solution([s(example)], [a1])


main()
