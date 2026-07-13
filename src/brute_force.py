import itertools 

def is_safe_all(G, mapping):
    for vertex in G:
        for neighbor in G[vertex]:
            if mapping[vertex] == mapping[neighbor]:
                return False
    return True

def brute_force_coloring(G):
    V = list(G.keys())
    n = len(V)
    for k in range(1, n + 1):
        for colors in itertools.product(range(1, k + 1), repeat=n):
            mapping = dict(zip(V, colors))
            if is_safe_all(G, mapping):
                return k, mapping

    