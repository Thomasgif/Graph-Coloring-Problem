def colorind_verify(V, E, n):
    for v in V:
        if V[v] >= n:
            return False
    for e in E:
        if V[e[0]] == V[e[1]]:
            return False
    return True