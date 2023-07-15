"""Build ESTG
"""

from collections import defaultdict
from .bcn import BCN


class ESTG:
    def __init__(self, bcn: BCN, Z: set | range) -> None:
        """Initialize an ESTG for `bcn` with a given set of states in `Z`

        Args:
            bcn (BCN): a BCN
            Z (set): a set of states

        See Algorithm 1 in the paper.
        An ESTG is defined with its successors `S` and predecessors `P`.
        """
        self.bcn = bcn
        self.Z = Z
        self.P = defaultdict(set)
        self.S = defaultdict(set)
        self._build()

    def _build(self):
        for i in self.Z:
            for j in range(1, self.bcn.M + 1): # control is indexed from 1
                self.S[i].add((i, j))  # denote b_i^j by (i, j)
                self.P[(i, j)].add(i)
                for k in range(1, self.bcn.Q + 1):
                    x_new = self.bcn.step(i, j, k)
                    self.S[(i, j)].add(x_new)
                    self.P[x_new] .add((i, j))
            


    

