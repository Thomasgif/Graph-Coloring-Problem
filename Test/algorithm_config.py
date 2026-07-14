from __future__ import annotations
from dataclasses import dataclass
import multiprocessing
import time
from typing import Any, Callable, Dict, List, Optional

Graph = Dict[Any, List[Any]]
Algorithm = Callable[..., tuple]

EXECUTION_RESULTS: List[Dict[str, Any]] = []

def _multiprocessing_worker(func, graph, seed_keyword, seed, queue):
    try:
        kwargs = {}
        if seed_keyword is not None and seed is not None:
            kwargs[seed_keyword] = seed
        result = func(graph, **kwargs)
        queue.put((True, result))
    except Exception as e:
        queue.put((False, str(e)))

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

    def run(
        self,
        graph: Graph,
        seed: Optional[int] = None,
        case_name: str = "Unknown",
        repetition: int = 0
    ) -> tuple:
        from validators import edge_count
        num_vertices = len(graph)
        num_edges = edge_count(graph)

        queue = multiprocessing.Queue()
        process = multiprocessing.Process(
            target=_multiprocessing_worker,
            args=(self.function, graph, self.seed_keyword, seed, queue)
        )
        
        start_time = time.perf_counter()
        process.start()
        
        timeout = 5.0
        process.join(timeout=timeout)
        elapsed_time = time.perf_counter() - start_time
        
        if process.is_alive():
            process.terminate()
            process.join()
            
            result_entry = {
                "algorithm": self.name,
                "case": case_name,
                "num_vertices": num_vertices,
                "num_edges": num_edges,
                "seed": seed,
                "repetition": repetition,
                "time_taken": elapsed_time,
                "colors_used": None,
                "status": "Timeout"
            }
            EXECUTION_RESULTS.append(result_entry)
            raise TimeoutError(f"Algorithm {self.name} timed out after {elapsed_time:.4f} seconds on case {case_name}")
            
        if not queue.empty():
            success, value = queue.get()
            queue.close()
            queue.join_thread()
            if success:
                # value is (k, coloring)
                k = value[0]
                result_entry = {
                    "algorithm": self.name,
                    "case": case_name,
                    "num_vertices": num_vertices,
                    "num_edges": num_edges,
                    "seed": seed,
                    "repetition": repetition,
                    "time_taken": elapsed_time,
                    "colors_used": k,
                    "status": "Completed"
                }
                EXECUTION_RESULTS.append(result_entry)
                return value
            else:
                result_entry = {
                    "algorithm": self.name,
                    "case": case_name,
                    "num_vertices": num_vertices,
                    "num_edges": num_edges,
                    "seed": seed,
                    "repetition": repetition,
                    "time_taken": elapsed_time,
                    "colors_used": None,
                    "status": f"Error: {value}"
                }
                EXECUTION_RESULTS.append(result_entry)
                raise Exception(f"Algorithm {self.name} failed with error: {value}")
        else:
            queue.close()
            queue.join_thread()
            result_entry = {
                "algorithm": self.name,
                "case": case_name,
                "num_vertices": num_vertices,
                "num_edges": num_edges,
                "seed": seed,
                "repetition": repetition,
                "time_taken": elapsed_time,
                "colors_used": None,
                "status": "No Output"
            }
            EXECUTION_RESULTS.append(result_entry)
            raise Exception(f"Algorithm {self.name} exited without putting result to queue.")


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
