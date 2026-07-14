from __future__ import annotations

import pytest

from algorithm_config import ALGORITHMS, AlgorithmSpec
from random_graph_factory import (
    RandomGraphCase,
    RandomKChromaticGraphFactory,
)
from validators import (
    assert_expected_chromatic_number,
    validate_coloring_output,
)


RANDOM_CASES = RandomKChromaticGraphFactory(
    default_edge_probability=0.35
).generate_suite()


@pytest.mark.parametrize(
    "case",
    RANDOM_CASES,
    ids=lambda case: case.name,
)
def test_random_case_has_valid_planted_solution(
    case: RandomGraphCase,
) -> None:
    """Comprueba independientemente la estructura y coloración generadas."""
    k, coloring = validate_coloring_output(
        case.graph,
        (case.expected_k, case.planted_coloring),
    )

    assert k == case.expected_k
    assert len(set(coloring.values())) == case.expected_k


@pytest.mark.parametrize(
    "algorithm",
    ALGORITHMS,
    ids=lambda algorithm: algorithm.name,
)
@pytest.mark.parametrize(
    "case",
    RANDOM_CASES,
    ids=lambda case: case.name,
)
def test_algorithm_on_random_graph(
    algorithm: AlgorithmSpec,
    case: RandomGraphCase,
) -> None:
    """
    Valida estructura y corrección en grafos aleatorios con chi(G) conocido.

    Para algoritmos probabilísticos se ejecutan varias semillas según
    AlgorithmSpec.repetitions.
    """
    obtained_values = []

    for execution in range(algorithm.repetitions):
        seed = case.seed * 1_000 + execution
        result = algorithm.run(
            case.graph,
            seed=seed,
            case_name=case.name,
            repetition=execution,
        )
        k, _ = validate_coloring_output(case.graph, result)
        obtained_values.append(k)

        assert k >= case.expected_k

        if algorithm.exact:
            assert_expected_chromatic_number(
                case.graph,
                result,
                case.expected_k,
            )

    assert len(obtained_values) == algorithm.repetitions

    # Para algoritmos no exactos se conserva el mejor resultado para que
    # pytest lo muestre al fallar alguna validación posterior.
    best_k = min(obtained_values)
    assert best_k <= len(case.graph)
