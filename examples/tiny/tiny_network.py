# Examples of the tiny network in the paper
from rss import BCN, ESTG, compute_LRCIS, compute_min_time_control
from pprint import pp


# network definition
def f1(x, u, ξ):
    return x[1] or x[2]

def f2(x, u, ξ):
    return x[0] and u[0]

def f3(x, u, ξ):
    return u[0] or (ξ[0] and x[0])



# build ASSR
bcn = BCN.from_Boolean_functions([f1, f2, f3], 1, 1)
print(bcn.L)


Z = set([2, 4, 5, 7])

print("- Example 1: ESTG")
Gz = ESTG(bcn, Z)
print("Gz.P:")
pp(Gz.P)
print("Gz.S:")
pp(Gz.S)

print("- Example 2: LRCIS")
IcZ, Ds, U1 = compute_LRCIS(Gz)
print("IcZ:")
pp(IcZ)
print("Ds:")
pp(Ds)
print("U1:")
pp(U1)


print("- Example 3: RSS")
# construct an ESTG for all states in ΔN
G = ESTG(bcn, range(1, bcn.N + 1))
Fs, U2 = compute_min_time_control(G, IcZ)
print("Fs:")
pp(Fs)
print("U2:")
pp(U2)



