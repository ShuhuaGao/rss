"""Minimum time robust set stabilization
"""

import copy
from collections import defaultdict
from .estg import ESTG
from .bcn import BCN


def compute_min_time_control(G: ESTG, IcZ: set[int]) -> tuple[list[set[int]], dict[int, list[int]]]:
    """Minimum time robust set stabilization

    Args:
        G (ESTG): the ESTG for ΔN
        IcZ (set[int]): the LRCIS

    Returns:
        tuple[list[set[int]], dict[int, list[int]]]: two returned values
        - F0, F1, F2 ⋯
        - U with U[x] collecting the controls for state x if x in Ω

    WARN: this method will change the ESTG `G` by deleting edges
    """
    assert IcZ
    P, S = G.P, G.S
    F0 = copy.copy(IcZ)
    F = copy.copy(F0)
    Fs = [copy.copy(F0)]
    U: dict[int, list[int]] = defaultdict(list)
    F1 = set()
    while F0:  # F0: F_k, F1: F_{k+1}
        F1.clear()
        for x in F0:
            to_delete = []
            for (i, j) in P[x]:
                if i not in F:
                    # delete the edge bij -> x
                    S[(i, j)].discard(x)
                    # P[x].discard((i, j))  # cannot delete during iteration
                    to_delete.append((i, j))
                if not S[(i, j)]:
                    F1.add(i)
                    U[i].append(j)
            for (i, j) in to_delete:
                P[x].discard((i, j))
        F |= F1
        Fs.append(copy.copy(F1))
        F0, F1 = F1, F0  # prepare for the next iteration
    return Fs, U 

