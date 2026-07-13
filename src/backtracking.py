def is_safe(vertex, color, G, colors):
    for child in G[vertex]:
        if colors[child] == color:
            return False
    return True

def backtracking_coloring(G, V, index, colors, variables_globales, num_colores):
   
    if index == len(V):

        colores_usados = len(num_colores)
        
        if colores_usados < variables_globales['mejor_num_colores']:
            variables_globales['mejor_num_colores'] = colores_usados
            variables_globales['mejor_colores'] = colors.copy()
        return

    vertex = V[index]

    colores_unicos = len(num_colores)
    if colores_unicos >= variables_globales['mejor_num_colores']:
        return
    
    limite_busqueda = min(len(V), variables_globales['mejor_num_colores']-1)

    for color in range(1, limite_busqueda + 1):
        if is_safe(vertex, color, G, colors):
            colors[vertex] = color

            num_colores[color] = num_colores.get(color, 0) + 1
            backtracking_coloring(G, V, index + 1, colors, variables_globales, num_colores)
            num_colores[color] -= 1
            if num_colores[color] == 0:
                del num_colores[color]
            colors[vertex] = 0

def encontrar_k(G):
    V = list(G.keys())
    colors = {vertex: 0 for vertex in V}
    variables_globales = {'mejor_num_colores': len(V), 'mejor_colores': None}
    num_colores = {}

    backtracking_coloring(G, V, 0, colors, variables_globales, num_colores)
    
    return variables_globales['mejor_num_colores'], variables_globales['mejor_colores']

    
    
