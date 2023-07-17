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
        self.P = defaultdict(set) # a dictionary whose each value is a set
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
            
    def compute_LRCIS(self) -> set[int]:
        """Calculate the LRCIS for a target set `Z`, which has been used to construct the ESTG.

        Returns:
            set[int]: the LRCIS, i.e., a set of states
        
        Warning: this method will change the ESTG `self` by deleting edges
        """  # noqa: E501
        if isinstance(self.Z, set):
            Z = self.Z
        else:
            Z = set(self.Z)
        R1Z = set()
        for j in range(1, self.bcn.M + 1):
            # union update in place
            R1Z |= self.bcn.step_set_from_set(Z, j)
        D0 = R1Z - Z
        D = set()
        while not D0:   # D0: D_k, D1: D_{k+1}
            D1 = set()  # the next set
            for x̄ in D0:  # x̄ represents x′ here because Python does not allow \prime 
                for (i, j) in self.P[x̄]:
                    if i not in D:
                        # delete the edge in both S and P
                        self.S[i].discard((i, j))
                        self.P[(i, j)].discard(i)
                        if not self.S[i]:  # empty 
                            D1.add(i)
            D |= D1
            D0 = D1
        return Z - D
    




    

