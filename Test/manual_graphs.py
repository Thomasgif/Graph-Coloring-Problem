from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Hashable, List

Vertex = Hashable
Graph = Dict[Vertex, List[Vertex]]


@dataclass(frozen=True)
class GraphCase:
    name: str
    graph: Graph
    expected_k: int
    description: str = ""


MANUAL_GRAPH_CASES = [
    GraphCase(
        name="camino_p5",
        graph={
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3],
        },
        expected_k=2,
        description="Camino con cinco vértices.",
    ),
    GraphCase(
        name="ciclo_par_c4",
        graph={
            0: [1, 3],
            1: [0, 2],
            2: [1, 3],
            3: [0, 2],
        },
        expected_k=2,
        description="Ciclo par; es bipartito.",
    ),
    GraphCase(
        name="ciclo_impar_c5",
        graph={
            0: [1, 4],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [0, 3],
        },
        expected_k=3,
        description="Ciclo impar; requiere tres colores.",
    ),
    GraphCase(
        name="estrella_k1_5",
        graph={
            0: [1, 2, 3, 4, 5],
            1: [0],
            2: [0],
            3: [0],
            4: [0],
            5: [0],
        },
        expected_k=2,
        description="Árbol con un vértice de grado alto.",
    ),
    GraphCase(
        name="bipartito_completo_k2_3",
        graph={
            "a": [1, 2, 3],
            "b": [1, 2, 3],
            1: ["a", "b"],
            2: ["a", "b"],
            3: ["a", "b"],
        },
        expected_k=2,
        description="Bipartito completo no trivial.",
    ),
    GraphCase(
        name="grafo_casa",
        graph={
            0: [1, 3],
            1: [0, 2],
            2: [1, 3, 4],
            3: [0, 2, 4],
            4: [2, 3],
        },
        expected_k=3,
        description="Cuadrado con techo triangular.",
    ),
    GraphCase(
        name="grafo_diamante",
        graph={
            0: [1, 2, 3],
            1: [0, 2, 3],
            2: [0, 1],
            3: [0, 1],
        },
        expected_k=3,
        description="K4 menos una arista.",
    ),
    GraphCase(
        name="dos_triangulos_comparten_vertice",
        graph={
            0: [1, 2, 3, 4],
            1: [0, 2],
            2: [0, 1],
            3: [0, 4],
            4: [0, 3],
        },
        expected_k=3,
        description="Dos triángulos que comparten un único vértice.",
    ),
    GraphCase(
        name="rueda_sobre_c4",
        graph={
            0: [1, 3, 4],
            1: [0, 2, 4],
            2: [1, 3, 4],
            3: [0, 2, 4],
            4: [0, 1, 2, 3],
        },
        expected_k=3,
        description="Un centro conectado a todos los vértices de C4.",
    ),
    GraphCase(
        name="rueda_sobre_c5",
        graph={
            0: [1, 4, 5],
            1: [0, 2, 5],
            2: [1, 3, 5],
            3: [2, 4, 5],
            4: [0, 3, 5],
            5: [0, 1, 2, 3, 4],
        },
        expected_k=4,
        description="Un centro conectado a todos los vértices de C5.",
    ),
    GraphCase(
        name="tripartito_completo_k2_2_2",
        graph={
            0: [2, 3, 4, 5],
            1: [2, 3, 4, 5],
            2: [0, 1, 4, 5],
            3: [0, 1, 4, 5],
            4: [0, 1, 2, 3],
            5: [0, 1, 2, 3],
        },
        expected_k=3,
        description="Tres partes independientes de tamaño dos.",
    ),
    GraphCase(
        name="cuatripartito_completo_k2_2_2_2",
        graph={
            0: [2, 3, 4, 5, 6, 7],
            1: [2, 3, 4, 5, 6, 7],
            2: [0, 1, 4, 5, 6, 7],
            3: [0, 1, 4, 5, 6, 7],
            4: [0, 1, 2, 3, 6, 7],
            5: [0, 1, 2, 3, 6, 7],
            6: [0, 1, 2, 3, 4, 5],
            7: [0, 1, 2, 3, 4, 5],
        },
        expected_k=4,
        description="Cuatro partes independientes de tamaño dos.",
    ),
    GraphCase(
        name="grafo_petersen",
        graph={
            0: [1, 4, 5],
            1: [0, 2, 6],
            2: [1, 3, 7],
            3: [2, 4, 8],
            4: [0, 3, 9],
            5: [0, 7, 8],
            6: [1, 8, 9],
            7: [2, 5, 9],
            8: [3, 5, 6],
            9: [4, 6, 7],
        },
        expected_k=3,
        description="Grafo de Petersen.",
    ),
    GraphCase(
        name="crown_graph_4",
        graph={
            "u0": ["v1", "v2", "v3"],
            "u1": ["v0", "v2", "v3"],
            "u2": ["v0", "v1", "v3"],
            "u3": ["v0", "v1", "v2"],
            "v0": ["u1", "u2", "u3"],
            "v1": ["u0", "u2", "u3"],
            "v2": ["u0", "u1", "u3"],
            "v3": ["u0", "u1", "u2"],
        },
        expected_k=2,
        description="K4,4 menos un emparejamiento perfecto.",
    ),
]
