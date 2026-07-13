def dsatur_coloring(G):
    v = set(G.keys())
    colors = {node: 0 for node in G}
    neighbor_colors_sets = {node: set() for node in G}
    saturation = {node: 0 for node in G}
    degrees = {node: len(G[node]) for node in G}

    while v:
        best_node = max(v, key=lambda node: (saturation[node], degrees[node]))
        used_colors = neighbor_colors_sets[best_node]
        
        color = 1
        while color in used_colors:
            color += 1
        colors[best_node] = color
        v.remove(best_node)

        for neighbor in G[best_node]:
            if neighbor in v:
                neighbor_colors_sets[neighbor].add(color)
                saturation[neighbor] = len(neighbor_colors_sets[neighbor])
        
    num_colors = len(set(colors.values()))
    return num_colors, colors
    
    
    
    