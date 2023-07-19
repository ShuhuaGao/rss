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
        - Fs, a list containing sets F0, F1, F2 ⋯
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
        if F1:
            Fs.append(copy.copy(F1))
        F0, F1 = F1, F0  # prepare for the next iteration
    return Fs, U 


def get_Tstar(i: int, Fs: list[set[int]]) -> int:
    """After obtaining `Fs` with `compute_min_time_control`, retrieve the minimum stabilization time 
    of a state `i`.

    Args:
        i (int): state
        Fs (list[set[int]]): a list containing sets F0, F1, F2 ⋯

    Returns:
        int: T*. -1 is returned if the state `i` cannot be stabilized.
    """  # noqa: E501
    for T, F in enumerate(Fs):
        if i in F:
            return T
    return -1

