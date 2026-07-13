from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from random import Random
from typing import Dict, List, Optional

from validators import validate_coloring_output, validate_graph_input

Graph = Dict[int, List[int]]
Coloring = Dict[int, int]


@dataclass(frozen=True)
class RandomGraphCase:
    name: str
    graph: Graph
    expected_k: int
    planted_coloring: Coloring
    seed: int


class RandomKChromaticGraphFactory:
    """
    Genera grafos simples, no dirigidos, conexos, no completos y con
    número cromático conocido exactamente.

    Estrategia:
    1. Divide los vértices en k conjuntos independientes.
    2. Construye un K_k usando un representante de cada conjunto.
    3. Solo agrega aristas entre conjuntos diferentes.

    La partición demuestra que chi(G) <= k y el K_k demuestra que
    chi(G) >= k. Por tanto, chi(G) = k.
    """

    def __init__(self, default_edge_probability: float = 0.35) -> None:
        if not 0.0 <= default_edge_probability <= 1.0:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        self.default_edge_probability = default_edge_probability

    def generate(
        self,
        *,
        n: int,
        k: int,
        seed: int,
        edge_probability: Optional[float] = None,
    ) -> RandomGraphCase:
        if not isinstance(n, int) or not isinstance(k, int):
            raise TypeError("n y k deben ser enteros.")

        if not 2 <= k < n:
            raise ValueError(
                "Debe cumplirse 2 <= k < n para evitar grafos sin aristas "
                "y grafos completos triviales."
            )

        probability = (
            self.default_edge_probability
            if edge_probability is None
            else edge_probability
        )

        if not 0.0 <= probability <= 1.0:
            raise ValueError("La probabilidad debe estar entre 0 y 1.")

        rng = Random(seed)
        vertices = list(range(n))
        shuffled_vertices = vertices.copy()
        rng.shuffle(shuffled_vertices)

        groups = [[] for _ in range(k)]

        for index, vertex in enumerate(shuffled_vertices):
            groups[index % k].append(vertex)

        planted_coloring: Coloring = {}

        for color, group in enumerate(groups):
            for vertex in group:
                planted_coloring[vertex] = color

        edges = set()

        def add_edge(u: int, v: int) -> None:
            if u == v:
                raise AssertionError("El generador intentó crear un lazo.")

            edges.add((min(u, v), max(u, v)))

        representatives = [group[0] for group in groups]

        # Clique K_k que fuerza el uso de al menos k colores.
        for u, v in combinations(representatives, 2):
            add_edge(u, v)

        # Conecta los vértices restantes al núcleo para garantizar conexión.
        for group_index, group in enumerate(groups):
            other_representatives = [
                representative
                for other_index, representative in enumerate(representatives)
                if other_index != group_index
            ]

            for vertex in group[1:]:
                add_edge(vertex, rng.choice(other_representatives))

        # Aristas aleatorias adicionales entre grupos de colores distintos.
        for u, v in combinations(vertices, 2):
            if planted_coloring[u] == planted_coloring[v]:
                continue

            if rng.random() < probability:
                add_edge(u, v)

        adjacency_sets = {vertex: set() for vertex in vertices}

        for u, v in edges:
            adjacency_sets[u].add(v)
            adjacency_sets[v].add(u)

        graph: Graph = {
            vertex: sorted(neighbors)
            for vertex, neighbors in adjacency_sets.items()
        }

        case = RandomGraphCase(
            name=f"aleatorio_n{n}_k{k}_seed{seed}",
            graph=graph,
            expected_k=k,
            planted_coloring=planted_coloring,
            seed=seed,
        )

        self.validate_generated_case(case)
        return case

    def generate_suite(self) -> List[RandomGraphCase]:
        """
        Suite moderada para pytest.

        Los tamaños pequeños son apropiados para fuerza bruta.
        Puede ampliar esta lista para pruebas de rendimiento separadas.
        """
        configurations = [
            # n, k, seed, probabilidad
            (5, 2, 101, 0.25),
            (6, 2, 102, 0.55),
            (6, 3, 103, 0.25),
            (7, 3, 104, 0.45),
            (7, 4, 105, 0.30),
            (8, 2, 106, 0.60),
            (8, 3, 107, 0.35),
            (8, 4, 108, 0.30),
            (9, 3, 109, 0.50),
            (9, 4, 110, 0.35),
        ]

        return [
            self.generate(
                n=n,
                k=k,
                seed=seed,
                edge_probability=probability,
            )
            for n, k, seed, probability in configurations
        ]

    @staticmethod
    def validate_generated_case(case: RandomGraphCase) -> None:
        validate_graph_input(
            case.graph,
            reject_edgeless=True,
            reject_complete=True,
        )

        # La coloración plantada debe ser una salida válida con k colores.
        validate_coloring_output(
            case.graph,
            (case.expected_k, case.planted_coloring),
        )

        # Verificación explícita de conexión.
        start = next(iter(case.graph))
        visited = {start}
        pending = [start]

        while pending:
            vertex = pending.pop()

            for neighbor in case.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    pending.append(neighbor)

        assert len(visited) == len(
            case.graph
        ), "El generador produjo un grafo no conexo."
