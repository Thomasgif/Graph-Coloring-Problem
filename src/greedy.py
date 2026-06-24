def greedy_colorin_graph(G, V):

    color = dict.fromkeys(V, 0) 

    for vertex in V:
        used_colors = set()

        for child in G[vertex]:
            if color[child] != 0:
                used_colors.add(color[child])
        
        current_color = 0

        while color[vertex] == 0:
            current_color += 1
            if current_color not in used_colors:
                color[vertex] = current_color
    return color
    