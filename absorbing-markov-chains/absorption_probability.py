import sympy as sp
from math import lcm
from typing import List, Tuple


def identify_states(weights: List[List[int]]) -> Tuple[List[int], List[int]]:
    """Separates state indices into transient and absorbing categories."""
    transient = []
    absorbing = []
    for i, row in enumerate(weights):
        if any(row):
            transient.append(i)
        else:
            absorbing.append(i)
    return transient, absorbing


def calculate_absorption_probabilities(weights):
    """
    Find a probability of each terminal state from a state 0
    1. Identify states, classify transition and absorption states
    2. Check if there is no transient states exist
    3. Create Q - transient to transient matrix;
              R - transient to terminal matrix
              I - absorption to absorption identity matrix
    4. Build B absorption_matrix - probability of ending in each absorption states from the state 0
        (I - Q) * B = R  ->  B = (I - Q).LUsolve(R)
    5. Extract numerators and the common denominator
    B[0, :] is a row vector of probabilities
    :param weights:
    :return: list [numerators, denominator]
    """
    # 1.
    transient_idx, absorbing_idx = identify_states(weights)

    # 2.
    if not transient_idx:
        return [1]

    # 3.
    q_data = []
    r_data = []
    for i in transient_idx:
        row_sum = sum(weights[i])
        q_data.append([sp.Rational(weights[i][j], row_sum) for j in transient_idx])
        r_data.append([sp.Rational(weights[i][j], row_sum) for j in absorbing_idx])

    q_matrix = sp.Matrix(q_data)
    r_matrix = sp.Matrix(r_data)
    i_matrix = sp.eye(len(transient_idx))

    # 4.
    b_matrix = (i_matrix - q_matrix).LUsolve(r_matrix)

    # 5.
    probs = b_matrix.row(0)

    denominators = [p.q for p in probs]
    common_den = lcm(*denominators)

    result = [int(p.p * (common_den // p.q)) for p in probs]
    result.append(common_den)

    return result


weights = [
    [0, 6, 0, 0, 0, 3, 0],
    [3, 0, 5, 1, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

print(calculate_absorption_probabilities(weights))
