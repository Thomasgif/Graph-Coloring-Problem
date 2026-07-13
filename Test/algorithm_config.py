from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

Graph = Dict[Any, List[Any]]
Algorithm = Callable[..., tuple]


@dataclass(frozen=True)
class AlgorithmSpec:
    """
    Configuración de un algoritmo que será probado.

    exact:
        True para fuerza bruta y backtracking exacto.
        False para greedy y algoritmos probabilísticos.

    repetitions:
        Número de ejecuciones por grafo. Para algoritmos deterministas use 1.

    seed_keyword:
        Nombre del argumento de semilla que recibe el algoritmo, por ejemplo
        "seed" o "semilla". Use None si la función no recibe semilla.
    """

    name: str
    function: Algorithm
    exact: bool
    repetitions: int = 1
    seed_keyword: Optional[str] = None

    def run(self, graph: Graph, seed: Optional[int] = None) -> tuple:
        kwargs = {}

        if self.seed_keyword is not None and seed is not None:
            kwargs[self.seed_keyword] = seed

        return self.function(graph, **kwargs)


# -----------------------------------------------------------------
# EDITE SOLAMENTE ESTA SECCIÓN PARA CONECTAR SUS IMPLEMENTACIONES.
# -----------------------------------------------------------------
#
# Ejemplo:
#
# from src.coloring import (
#     backtracking_with_pruning,
#     brute_force_coloring,
#     greedy_coloring,
#     probabilistic_coloring,
# )
#
# ALGORITHMS = [
#     AlgorithmSpec(
#         name="backtracking_con_poda",
#         function=backtracking_with_pruning,
#         exact=True,
#     ),
#     AlgorithmSpec(
#         name="fuerza_bruta",
#         function=brute_force_coloring,
#         exact=True,
#     ),
#     AlgorithmSpec(
#         name="greedy",
#         function=greedy_coloring,
#         exact=False,
#     ),
#     AlgorithmSpec(
#         name="probabilistico",
#         function=probabilistic_coloring,
#         exact=False,
#         repetitions=20,
#         seed_keyword="seed",  # Cambiar a "semilla" si corresponde.
#     ),
# ]
#
# Mientras la lista permanezca vacía, pytest marcará las pruebas de
# algoritmos como omitidas en vez de producir un error de importación.

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.backtracking import encontrar_k
from src.brute_force import brute_force_coloring
from src.greedy import dsatur_coloring
from src.probabilistic import probabilistic_coloring

ALGORITHMS: List[AlgorithmSpec] = [
    AlgorithmSpec(
        name="backtracking_con_poda",
        function=encontrar_k,
        exact=True,
    ),
    AlgorithmSpec(
        name="fuerza_bruta",
        function=brute_force_coloring,
        exact=True,
    ),
    AlgorithmSpec(
        name="greedy",
        function=dsatur_coloring,
        exact=False,
    ),
    AlgorithmSpec(
        name="probabilistico",
        function=probabilistic_coloring,
        exact=False,
        repetitions=20,
        seed_keyword="seed",
    ),
]
