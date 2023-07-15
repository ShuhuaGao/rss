# Test the algorithm with the T-LGL network

import numpy as np 
from rss.estg import ESTG
from rss.bcn import BCN
from pathlib import Path
import time 


## Load data
data_dir = Path(__file__).resolve().parent / "data"
Z = np.load(data_dir / "Z.npy")
net = np.load(data_dir / "net.npz")
N = net["N"]
bcn = BCN(net["L"], int(np.log2(net["Q"])), int(np.log2(net["M"])), int(np.log2(N)))

## build ESTG
start = time.time()
print(bcn.M, bcn.N, bcn.Q)
estg = ESTG(bcn, range(1, N + 1))
print(len(estg.S), len(estg.P))
end = time.time()
print("Time (s): ", end - start)

