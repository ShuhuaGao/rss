"""Computation of the LRCIS
"""
from .estg import ESTG
from .bcn import BCN


def compute_LRCIS(Gz: ESTG) -> set[int]:
    """Compute LRCIS using `Gz`

    Args:
        Gz (ESTG): an ESTG constructed for a target set `Gz.Z`

    Returns:
        set[int]: the LRCIS, i.e., a set of states
        
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
    while D0:   # D0: D_k, D1: D_{k+1}
        # print("D0 len: ", len(D0))
        D1 = set()  # the next set #TODO
        for x̄ in D0:  # x̄ represents x′ here because Python does not allow \prime 
            for (i, j) in P[x̄]:
                if i not in D:
                    # delete the edge i -> bij in both S and P
                    S[i].discard((i, j))
                    P[(i, j)].discard(i)
                    if not S[i]:  # empty 
                        D1.add(i)
        D |= D1
        D0 = D1
    return Z - D