def dsatur_coloring(G):
    v = list(G.keys())
    colors = dict.fromkeys(v, 0) 
    saturation = {node: 0 for node in v}
    degrees = {node: len(G[node]) for node in v}

    while v:
        best_node = max(v, key=lambda node: (saturation[node], degrees[node]))
        neighbors_colors = {colors[neighbors] for neighbors in G[best_node] if colors[neighbors] != 0}
        
        color = 0
        while color in neighbors_colors:
            color += 1
        colors[best_node] = color
        v.remove(best_node)

        for neighbor in G[best_node]:
            if neighbor in v:
                unique_neighbor_colors = {colors[neighbor] for neighbor in G[neighbor] if colors[neighbor] != 0}
                saturation[neighbor] = len(unique_neighbor_colors)
        
    num_colors = len(set(colors.values()))
    return num_colors, colors
    
    
    
    