# Test the algorithm with the T-LGL network

import numpy as np 
from rss import BCN, ESTG, compute_LRCIS
from pathlib import Path
import time 


## Load data
data_dir = Path(__file__).resolve().parent / "data"
Z = np.load(data_dir / "Z.npy")
print(len(Z))
net = np.load(data_dir / "net.npz")
N = net["N"]
bcn = BCN(net["L"], int(np.log2(net["Q"])), int(np.log2(net["M"])), int(np.log2(N)))

## build ESTG
start = time.time()
print(bcn.M, bcn.N, bcn.Q)
estg = ESTG(bcn, Z)
print(len(estg.S), len(estg.P))
LRCIS = compute_LRCIS(estg)
print(len(Z), len(LRCIS))

end = time.time()
print("Time (ESTG + LRCIS) (s): ", end - start)

# validate results with Julia


