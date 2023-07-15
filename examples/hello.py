from rss.bcn import BCN 
import numpy as np 
import time


L = np.array([1, 2, 3, 4, 2, 1, 2, 4, 1, 1, 4, 3, 2, 3, 3, 2])

bcn = BCN(L, 1, 1, 2)

print(bcn.M, bcn.N)
print(bcn.step(3, 2, 1))

