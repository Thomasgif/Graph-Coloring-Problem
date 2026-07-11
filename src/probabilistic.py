import random

def probabilistic_coloring(G):

    V = list(G.keys())
    random.shuffle(V)
    colors = dict.fromkeys(V, None) 
    

    for vertex in V:
        used_colors = set()

        for child in G[vertex]:
            if colors[child] != None:
                used_colors.add(colors[child])
        
        current_color = 0

        while colors[vertex] == 0:
            current_color += 1
            if current_color not in used_colors:
                colors[vertex] = current_color

    num_colors = len(set(colors.values()))
    return num_colors, colors