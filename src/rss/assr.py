# Compute the ASSR for a given Boolean network subject to disturbances 
from collections.abc import Callable
import numpy as np
import itertools
from collections.abc import Iterable


def _logical_vector_product(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    # a vector δ_n^i is represented by (n, i)
    n0 = (a[1] - 1) * b[0]
    pos1 = n0 + b[1]
    return (a[0] * b[0], pos1)


def _to_logical_vector(s: Iterable[int|bool]) -> tuple[int, int]:
    """
    Convert a sequence of binary integers to a logical vector.

    Args:
        s (Iterable[int|bool]): A sequence of binary integers.

    Returns:
        tuple[int, int]: The result of the logical vector conversion.
    """
    # s is a sequence of binary integers
    r = (1, 1)
    for b in s:
        bl = (2, 1) if b else (2, 2)  # 1 ~ δ21, 0 ~δ22
        r = _logical_vector_product(r, bl)
    return r


def compute_ASSR(fs: list[Callable], m: int, q: int) -> np.ndarray:
    """Compute ASSR for n Boolean functions in `fs` with `m` control variables and 
    `q` disturbance variables.
    Each function in `fs` is `f(x, u, ξ)`.
    """
    n = len(fs)
    Q = 2 ** q
    M = 2 ** m
    N = 2 ** n
    L = np.zeros(Q * M * N, dtype=int)

    x_next = np.zeros(len(fs), dtype=int)
    for ib in itertools.product(*itertools.repeat([0, 1], n)):
        for jb in itertools.product(*itertools.repeat([0, 1], m)):
            for kb in itertools.product(*itertools.repeat([0, 1], q)):  
                # get the next state via Eq. (4)
                # first get the STP vector form of each binary sequence
                il = _to_logical_vector(ib)
                jl = _to_logical_vector(jb)
                kl = _to_logical_vector(kb)
                # Lξux 
                rl = _logical_vector_product(kl, jl)
                rl = _logical_vector_product(rl, il)
                r = rl[1] # r is the position of 1 in rl
                # let us compute the next state via logical operations
                for (idx, f) in enumerate(fs):
                    x_next[idx] = f(ib, jb, kb)
                x_next_l = _to_logical_vector(x_next)
                # assign the r-th column of L by x_next_l
                L[r - 1] = x_next_l[1]
    return L 




