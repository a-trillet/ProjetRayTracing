import Ray
import math
#constant variables :
Z0 = 376.730313
Ra = 73
c = 299792458
lam = c/(27 * 10**9)
he = -lam/math.pi
factor = he**2/8/Ra
print(factor)
