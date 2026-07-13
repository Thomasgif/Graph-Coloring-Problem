# Pruebas pytest para coloración de grafos

Esta carpeta contiene la suite de pruebas para verificar la validez y el correcto funcionamiento de los algoritmos de coloreado de grafos implementados en `src`.

## Estructura de la carpeta `Test`

- `manual_graphs.py`: Casos de prueba manuales con estructuras de grafos y números cromáticos conocidos.
- `validators.py`: Funciones auxiliares para validar la correctitud del grafo de entrada y la salida de la coloración `(k, coloracion)`.
- `random_graph_factory.py`: Fábrica/Generador de grafos aleatorios conexos simples con número cromático $chi(G) = k$ conocido.
- `algorithm_config.py`: Archivo de configuración que conecta los algoritmos en `src` con la suite de pruebas.
- `test_manual_coloring.py`: Pruebas parametrizadas de los algoritmos sobre grafos manuales.
- `test_random_coloring.py`: Pruebas parametrizadas de los algoritmos sobre grafos aleatorios.
- `test_coloring_ver.py`: Pruebas unitarias para validar la función de verificación de coloreados `colorind_verify`.

## Contrato de Entrada y Salida

### Entrada:
Un grafo representado como un diccionario de adyacencia no dirigido, sin lazos y no multígrafo:
```python
{
    vertice: [vecino_1, vecino_2, ...]
}
```

### Salida:
Una tupla con el número cromático $k$ obtenido y el mapeo de color por cada vértice:
```python
(
    k,
    {
        vertice: color
    }
)
```

## Configuración y Conexión de Algoritmos

Los algoritmos ubicados en `src/` están conectados en `algorithm_config.py` de la siguiente manera:

```python
from src.backtracking import encontrar_k
from src.brute_force import brute_force_coloring
from src.greedy import dsatur_coloring
from src.probabilistic import probabilistic_coloring

ALGORITHMS = [
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
```

## Ejecución de Pruebas

Para instalar dependencias y ejecutar las pruebas desde el directorio raíz del proyecto:

```bash
pip install pytest
python -m pytest -v
```

## Validación Exacta vs Heurística

- **Algoritmos Exactos (`exact=True`)**: Para Fuerza Bruta y Backtracking con poda, la suite de pruebas exige que el número de colores devuelto $k$ coincida exactamente con el número cromático esperado ($k_{obtenido} == k_{esperado}$).
- **Algoritmos Heurísticos/Probabilísticos (`exact=False`)**: Para Greedy (DSATUR) y Probabilístico, se verifica que la coloración sea válida (nodos adyacentes no compartan color) y que use $k \ge k_{esperado}$.
