"""Computation of the LRCIS
"""
from .estg import ESTG
from .bcn import BCN
import copy
from collections import defaultdict


def compute_LRCIS(Gz: ESTG) -> tuple[set[int], list[set], dict[int, set[int]]]:
    """Compute LRCIS using `Gz`

    Args:
        Gz (ESTG): an ESTG constructed for a target set `Gz.Z`

    Returns:
        the LRCIS,
        the list of Dk sets,
        U1
        
    WARN: this method will change the ESTG `Gz` by deleting edges
    """
    if isinstance(Gz.Z, set):
            Z = Gz.Z
    else:
        Z = set(Gz.Z)
    bcn: BCN = Gz.bcn
    P, S = Gz.P, Gz.S
    R1Z = set()
    for j in range(1, bcn.M + 1):
        R1Z |= bcn.step_set_from_set(Z, j)
    D0 = R1Z - Z
    D = set()
    Ds = [copy.copy(D0)]  # collect all Dk's
    D1 = set()  # the next set
    while D0:   # D0: D_k, D1: D_{k+1}
        # print("D0 len: ", len(D0))
        D1.clear()
        for x̄ in D0:  # x̄ represents x′ here because Python does not allow \prime 
            for (i, j) in P[x̄]:
                if i not in D:
                    # delete the edge i -> bij in both S and P
                    S[i].discard((i, j))
                    P[(i, j)].discard(i)
                    if not S[i]:  # empty 
                        D1.add(i)
        D |= D1
        Ds.append(copy.copy(D1))
        D0, D1 = D1, D0
            
    IcZ = Z - D 
    U1: dict[int, set[int]] = defaultdict(set)
    for x in IcZ:
        for (i, j) in S[x]:
            U1[i].add(j)  # i = x here
    return IcZ, Ds, U1