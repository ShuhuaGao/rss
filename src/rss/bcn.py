"""Boolean control network with disturbances
"""

import numpy as np


class BCN:
    def __init__(self, L: np.ndarray, q: int, m: int, n: int) -> None:
        self.Q = 2 ** q
        self.M = 2 ** m
        self.N = 2 ** n
        assert len(L) == self.Q * self.M * self.N
        self.L = L

    def step(self, i: int, j: int, k: int) -> int:
        """Compute state transition in one step

        Args:
            i (int): state
            j (int): control
            k (int): disturbance

        Returns:
            int: new state
        """
        # see Eq. (4) in the paper
        M, N = self.M, self.N
        # note that i, j, k starts from 1, but indexing in Python begins from 0
        Blk_Q_k = self.L[(k - 1) * M * N: k * M * N]
        Blk_M_j = Blk_Q_k[(j - 1) * N: j * N]
        Col_i = Blk_M_j[i - 1]
        return Col_i

