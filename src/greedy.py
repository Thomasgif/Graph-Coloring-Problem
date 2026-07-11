def greedy_coloring(G):
    v = list(G.keys())
    colors = dict.fromkeys(v, 0) 
    

    for vertex in v:
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
    
    
    
    