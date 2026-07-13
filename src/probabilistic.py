import random

def probabilistic_coloring(G, seed=None):
    if seed is not None:
        random.seed(seed)

    V = list(G.keys())
    random.shuffle(V)
    colors = dict.fromkeys(V, 0) 

    for vertex in V:
        used_colors = set()

        for child in G[vertex]:
            if colors[child] != 0:
                used_colors.add(colors[child])
        
        current_color = 0

        while colors[vertex] == 0:
            current_color += 1
            if current_color not in used_colors:
                colors[vertex] = current_color

    num_colors = len(set(colors.values()))
    return num_colors, colors