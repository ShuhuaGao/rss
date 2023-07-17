"""Boolean control network with disturbances
"""

import numpy as np
from collections.abc import Iterable


class BCN:
    def __init__(self, L: np.ndarray, q: int, m: int, n: int) -> None:
        """Create a BCN

        Args:
            L (np.ndarray): state transition matrix (a logical matrix in vector form)
            q (int): number of disturbance variables
            m (int): number of control variables    
            n (int): number of state variables
        """
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

    def step_set(self, i: int, j: int) -> set[int]:
        """Compute the one-step reachable set ``R_1``

        Args:
            i (int): state
            j (int): control

        Returns:
            set[int]: all possible succeeding states caused by random disturbances
        """
        ss = set()
        for k in range(1, self.Q + 1):
            s = self.step(i, j, k)
            ss.add(s)
        return ss
    
    def step_set_from_set(self, i_set: Iterable[int], j: int) -> set[int]:
        """Compute one-step reachable set for a set `i_set`

        Args:
            i_set (Iterable[int]): a set of source states
            j (int): control

        Returns:
            set[int]: all possible succeeding states from `i_set` caused by random disturbances
        """
        res = set()
        for i in i_set:
            ss = self.step_set(i, j)
            res |= ss  # union in place
        return res