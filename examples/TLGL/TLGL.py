# Test the algorithm with the T-LGL network

import numpy as np 
from rss import BCN, ESTG, compute_LRCIS, compute_min_time_control, get_Tstar
from pathlib import Path
import time 


## Load data
data_dir = Path(__file__).resolve().parent / "data"
Z = np.load(data_dir / "Z.npy")
net = np.load(data_dir / "net.npz")
print("N = ", net["N"], "M = ", net["M"], "Q = ", net["Q"])
bcn = BCN(net["L"], int(np.log2(net["Q"])), int(np.log2(net["M"])), int(np.log2(net["N"])))

## build ESTG
print("Solving LRCIS...")
start = time.time()
estg = ESTG(bcn, Z)
LRCIS = compute_LRCIS(estg)
end = time.time()
t1 = end - start
print("Time (ESTG + LRCIS) (s): ", t1)
print("size of Z and LRCIS: ", len(Z), len(LRCIS))

# validate results with Julia
# IcZ_sorted = sorted(list(LRCIS))
# print(IcZ_sorted[0],  IcZ_sorted[44], IcZ_sorted[88], IcZ_sorted[-1], IcZ_sorted[-2])

print("Solving min-time rss...")
start = time.time()
# construct an ESTG for all states in ΔN
G = ESTG(bcn, range(1, bcn.N + 1))
Fs, U = compute_min_time_control(G, LRCIS)
print("Time (ESTG + LRCIS + min-time RSS) (s): ", time.time() - start + t1)
print("Size of Ω: ", sum(len(Fk) for Fk in Fs))
print("Largest T* except ∞: ", len(Fs) - 1)
print("T* for state 1: ", get_Tstar(1, Fs))
print("T* for state 1234: ", get_Tstar(1234, Fs))
print("T* for state 7680: ", get_Tstar(7680, Fs))  # in IcZ


