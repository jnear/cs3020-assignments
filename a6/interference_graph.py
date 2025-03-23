from typing import List, Set, Dict, Tuple, DefaultDict
from collections import defaultdict
from cs3020_support.python import print_ast

class InterferenceGraph:
    """
    A class to represent an interference graph: an undirected graph where nodes
    are str objects and an edge between two nodes indicates that the two
    nodes cannot share the same locations.
    """
    graph: DefaultDict[str, Set[str]]

    def __init__(self):
        self.graph = defaultdict(lambda: set())

    def add_edge(self, a: str, b: str):
        if a != b:
            self.graph[a].add(b)
            self.graph[b].add(a)

    def neighbors(self, a: str) -> Set[str]:
        if a in self.graph:
            return self.graph[a]
        else:
            return set()

    def get_nodes(self):
        return set(self.graph.keys())

    def __str__(self):
        pairs = set()
        for k in self.graph.keys():
            new_pairs = set((k, v) for v in self.graph[k])
            pairs = pairs.union(new_pairs)

        for a, b in list(pairs):
            if (b, a) in pairs:
                pairs.remove((a, b))

        strings = [print_ast(a) + ' -- ' + print_ast(b) for a, b in pairs]
        return 'InterferenceGraph{\n ' + ',\n '.join(strings) + '\n}'
