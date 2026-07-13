from __future__ import annotations

import pytest

from algorithm_config import ALGORITHMS, AlgorithmSpec
from manual_graphs import MANUAL_GRAPH_CASES, GraphCase
from validators import (
    assert_expected_chromatic_number,
    validate_coloring_output,
    validate_graph_input,
)


@pytest.mark.parametrize(
    "case",
    MANUAL_GRAPH_CASES,
    ids=lambda case: case.name,
)
def test_manual_graph_definition_is_valid(case: GraphCase) -> None:
    """Valida primero que cada caso manual respete las restricciones."""
    validate_graph_input(
        case.graph,
        reject_edgeless=True,
        reject_complete=True,
    )


@pytest.mark.parametrize(
    "algorithm",
    ALGORITHMS,
    ids=lambda algorithm: algorithm.name,
)
@pytest.mark.parametrize(
    "case",
    MANUAL_GRAPH_CASES,
    ids=lambda case: case.name,
)
def test_algorithm_on_manual_graph(
    algorithm: AlgorithmSpec,
    case: GraphCase,
) -> None:
    """
    Todos los algoritmos deben retornar una coloración válida.

    Los algoritmos exactos también deben encontrar el número cromático.
    Los heurísticos y probabilísticos pueden usar más colores.
    """
    results = []

    for execution in range(algorithm.repetitions):
        result = algorithm.run(
            case.graph,
            seed=case.expected_k * 10_000 + execution,
        )

        k, coloring = validate_coloring_output(case.graph, result)
        results.append((k, coloring))

        assert k >= case.expected_k, (
            f"{algorithm.name} reportó k={k}, menor que el número cromático "
            f"conocido {case.expected_k}."
        )

        if algorithm.exact:
            assert_expected_chromatic_number(
                case.graph,
                result,
                case.expected_k,
            )

    assert results, "El algoritmo no fue ejecutado."
