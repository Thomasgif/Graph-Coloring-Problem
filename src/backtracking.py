def is_safe(vertex, color, G, colors):
    for child in G[vertex]:
        if colors[child] == color:
            return False
    return True

def backtracking_coloring(G, V, num_colors, index, colors):
   
   if index == len(V):
    return True

    vertex = V[index]

    for color in range(1, num_colors + 1):
        if is_safe(vertex, color, G, colors):
            colors[vertex] = color
            if backtracking_coloring(G, V, num_colors, index + 1, colors):
                return True
            
            colors[vertex] = None

    return False

    

        
    
