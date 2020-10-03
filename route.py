# -*- coding:utf-8 -*-
import sys
import argparse
import csv
from typing import Dict, List
from dataclasses import dataclass
from collections import OrderedDict

DEFAULT_DEST = '-'

parser = argparse.ArgumentParser()
parser.add_argument('src', help='Source file path.')
parser.add_argument('dest', default=DEFAULT_DEST, nargs='?', help='Target file path.')


@dataclass
class Edge:
    pk: int
    src: str
    dest: str
    weight: int

    def __hash__(self):
        return hash(self.pk)

    @classmethod
    def build(cls, k: int, s: str, d: str, w: int):
        s = s.strip().upper()
        d = d.strip().upper()

        return cls(k, s, d, w)

    def serialize(self):
        return self.pk, self.src, self.dest, self.weight


@dataclass
class Circle:
    src: str
    edges: List[Edge]

    @property
    def weight(self) -> int:
        try:
            e = min(self.edges, key=(lambda k: k.weight))
            return e.weight
        except ValueError:
            return 0


class Graph(object):
    routes: Dict[Edge, Edge]
    adj: Dict[str, List[Edge]]

    def __init__(self):
        self.routes = OrderedDict()
        self.adj = dict()

    def add_edge(self, e: Edge):
        self.routes[e] = e

        s = e.src
        if s not in self.adj:
            self.adj[s] = list()

        self.adj[s].append(e)

    @property
    def edges(self) -> int:
        return len(self.routes)

    @property
    def vertices(self) -> int:
        return len(self.adj)

    def serialize(self):
        results = list()
        for e in self.routes.values():
            if 0 == e.weight:
                continue

            results.append(e.serialize())

        return results


def search_circle(g: Graph) -> List[Circle]:
    pass


def main(r, w):
    g = Graph()

    for item in r:
        try:
            k, s, d, w_ = item
            e = Edge.build(int(k), s, d, int(w_))
        except (TypeError, ValueError):
            continue

        g.add_edge(e)

    w.writerows(g.serialize())


if __name__ == '__main__':
    args = parser.parse_args()
    src_ = args.src
    dest_ = args.dest

    fd_src = open(src_, 'r')
    reader = csv.reader(fd_src)

    if DEFAULT_DEST == dest_:
        fd_dest = sys.stdout
    else:
        fd_dest = open(dest_, 'w')

    writer = csv.writer(fd_dest)

    main(reader, writer)
