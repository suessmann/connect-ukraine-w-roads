import networkx as nx
import pandas as pd
import numpy as np

from networkx.utils import UnionFind
from operator import itemgetter
from heapq import heappop, heappush

# TODO: add NaN handling for all algorithms
def boruvka_mst(G):
    """Finds MST using Boruvka's algoritm
    
    Params
    --------
    G: NetworkX Graph
        An input weighted graph to find MST
    
    Returns
    --------
    T: NetworkX Graph
        A minimum spanning tree
    """
    T = nx.Graph()
    T.add_nodes_from(G.nodes)

    forest = UnionFind(G)

    def find_edge(comp):
        """Finds the minimum edge for the given connected component"""

        minw = np.inf
        border = None
        

        for e in nx.edge_boundary(G, comp, data=True):
            w = e[-1].get('weight', 1)

            if w < minw:
                minw = w
                border = e
        
        return border

    min_edges = (find_edge(comp) for comp in forest.to_sets())
    min_edges = [edge for edge in min_edges if edge is not None]

    while min_edges:
        min_edges = (find_edge(comp) for comp in forest.to_sets())
        min_edges = [edge for edge in min_edges if edge is not None]

        for u, v, w in min_edges:
            if forest[u] != forest[v]:
                T.add_edge(u, v, weight=w['weight'])
                forest.union(u, v)

    return T

def kruskal_mst(G):
    """Finds MST using Kruskal's algoritm
    
    Params
    --------
    G: NetworkX Graph
        An input weighted graph to find MST
    
    Returns
    --------
    T: NetworkX Graph
        A minimum spanning tree
    """
    T = nx.Graph()
    T.add_nodes_from(G.nodes)

    forest = UnionFind(G)

    edges = G.edges(data=True)

    def get_weights():
        """Unpacks the weights from a dictionary"""
        for u, v, dct in edges:
            w = dct.get('weight', 1)

            yield w, u, v, dct

    edges = sorted(get_weights(), key=itemgetter(0))

    for w, u, v, _ in edges:
        if forest[u] != forest[v]:
            T.add_edge(u, v, weight=w)
            forest.union(u, v)

    return T


def prim_mst(G):
    """Finds MST using Prim's algoritm
    
    Params
    --------
    G: NetworkX Graph
        An input weighted graph to find MST
    
    Returns
    --------
    T: NetworkX Graph
        A minimum spanning tree
    """
    T = nx.Graph()

    nodes = list(G.nodes)
    i = 0

    while nodes:
        u = nodes.pop(0)
        front = []
        visited = [u]

        for v, d in G.adj[u].items():
            w = d.get('weight', 1)
            i += 1
            heappush(front, (w, i, u, v, d))

            while front:
                wt, _, u, v, d = heappop(front)
                
                if v in visited:
                    continue
                else:
                    T.add_edge(u, v, weight=d['weight'])
                visited.append(v)
                nodes.remove(v)

                for w, d2 in G.adj[v].items():
                    if w in visited:
                        continue
                    new_w = d2.get('weight', 1)
                    i += 1
                    heappush(front, (new_w, i, v, w, d2))
    return T