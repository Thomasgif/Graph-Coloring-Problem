from __future__ import annotations

from typing import Dict, Hashable, Iterable, List, Mapping, Sequence, Tuple

Vertex = Hashable
Graph = Dict[Vertex, List[Vertex]]
Coloring = Dict[Vertex, Hashable]


def edge_count(graph: Mapping[Vertex, Sequence[Vertex]]) -> int:
    """Cuenta las aristas de un grafo simple no dirigido."""
    return sum(len(neighbors) for neighbors in graph.values()) // 2


def validate_graph_input(
    graph: Mapping[Vertex, Sequence[Vertex]],
    *,
    reject_edgeless: bool = True,
    reject_complete: bool = True,
) -> None:
    """
    Valida la estructura exigida por el proyecto:

    - Diccionario {vertice: [vecinos]}.
    - Grafo no dirigido.
    - Sin lazos.
    - Sin aristas múltiples.
    - Todos los vecinos deben existir como vértices.
    - Opcionalmente rechaza grafos sin aristas y grafos completos.

    Lanza AssertionError cuando encuentra una entrada inválida.
    """
    assert isinstance(graph, dict), "El grafo debe ser un diccionario."
    assert graph, "El grafo debe contener al menos un vértice."

    vertices = set(graph.keys())

    for vertex, neighbors in graph.items():
        assert isinstance(
            neighbors, list
        ), f"Los vecinos de {vertex!r} deben estar almacenados en una lista."

        assert len(neighbors) == len(
            set(neighbors)
        ), f"El vértice {vertex!r} contiene vecinos repetidos."

        assert vertex not in neighbors, f"Se encontró un lazo en {vertex!r}."

        for neighbor in neighbors:
            assert (
                neighbor in vertices
            ), f"El vecino {neighbor!r} no aparece como vértice del diccionario."

            assert (
                vertex in graph[neighbor]
            ), (
                f"La arista ({vertex!r}, {neighbor!r}) no es simétrica. "
                "El grafo debe ser no dirigido."
            )

    n = len(graph)
    m = edge_count(graph)

    if reject_edgeless:
        assert m > 0, "Los grafos sin aristas se omiten en este estudio."

    if reject_complete:
        maximum_edges = n * (n - 1) // 2
        assert (
            m != maximum_edges
        ), "Los grafos completos se omiten en este estudio."


def validate_coloring_output(
    graph: Mapping[Vertex, Sequence[Vertex]],
    result: object,
) -> Tuple[int, Coloring]:
    """
    Valida la salida (k, {vertice: color}).

    Retorna la salida tipada cuando es válida y lanza AssertionError
    cuando encuentra un problema.
    """
    assert isinstance(result, tuple), "La salida debe ser una tupla (k, coloracion)."
    assert len(result) == 2, "La salida debe contener exactamente dos elementos."

    k, coloring = result

    assert isinstance(k, int), "k debe ser un número entero."
    assert k >= 1, "k debe ser mayor o igual que 1."
    assert isinstance(
        coloring, dict
    ), "La coloración debe ser un diccionario {vertice: color}."

    graph_vertices = set(graph.keys())
    colored_vertices = set(coloring.keys())

    assert (
        colored_vertices == graph_vertices
    ), "La coloración debe asignar un color a cada vértice y no incluir vértices extra."

    used_colors = set(coloring.values())

    assert len(used_colors) == k, (
        f"k={k}, pero la solución utiliza {len(used_colors)} colores distintos: "
        f"{used_colors!r}."
    )

    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            assert coloring[vertex] != coloring[neighbor], (
                f"Coloración inválida: {vertex!r} y {neighbor!r} son adyacentes "
                f"y tienen el mismo color {coloring[vertex]!r}."
            )

    return k, coloring


def assert_expected_chromatic_number(
    graph: Mapping[Vertex, Sequence[Vertex]],
    result: object,
    expected_k: int,
) -> Tuple[int, Coloring]:
    """Valida la solución y comprueba que k sea el número cromático esperado."""
    k, coloring = validate_coloring_output(graph, result)
    assert (
        k == expected_k
    ), f"Se esperaban {expected_k} colores, pero el algoritmo devolvió {k}."
    return k, coloring
