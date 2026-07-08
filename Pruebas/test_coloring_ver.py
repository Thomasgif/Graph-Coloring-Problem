import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Verificacion.coloring_ver import colorind_verify

# Lista de casos de prueba
test_cases = [
    {
        "name": "1. Coloreado incorrecto (vértices adyacentes mismo color)",
        "V": {0: 0, 1: 0, 2: 1},
        "E": [(0, 1), (1, 2)],
        "n": 3,
        "expected": False
    },
    {
        "name": "2. Exceso de colores en grafo cuadrado (color de vértice mayor o igual a n)",
        "V": {0: 0, 1: 1, 2: 2, 3: 1},
        "E": [(0, 1), (1, 2), (2, 3), (3, 0)],
        "n": 2,
        "expected": False
    },
    {
        "name": "3. Grafo completo K_4 válido",
        "V": {0: 0, 1: 1, 2: 2, 3: 3},
        "E": [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
        "n": 4,
        "expected": True
    },
    {
        "name": "4. Grafo bipartito C_4 válido",
        "V": {0: 0, 1: 1, 2: 0, 3: 1},
        "E": [(0, 1), (1, 2), (2, 3), (3, 0)],
        "n": 2,
        "expected": True
    },
    {
        "name": "5. Falla del algoritmo por coloreado incompleto (vértice sin asignar)",
        "V": {0: 0}, 
        "E": [(0, 1)],
        "n": 2,
        "expected": KeyError
    }
]

@pytest.mark.parametrize("case", test_cases, ids=lambda c: c["name"])
def test_colorind_verify(case):
    V = case["V"]
    E = case["E"]
    n = case["n"]
    expected = case["expected"]
    
    if isinstance(expected, bool):
        # Si el resultado esperado es un booleano, realizamos la aserción normal
        assert colorind_verify(V, E, n) == expected
    else:
        # Si el resultado esperado es una excepción, verificamos que se lance correctamente
        with pytest.raises(expected):
            colorind_verify(V, E, n)

if __name__ == "__main__":
    pytest.main([__file__])
