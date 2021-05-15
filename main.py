import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp
import numpy as np
from datetime import datetime
import numba
from numba import jit, njit, vectorize, cuda, float32, complex64, int8, guvectorize

results = np.zeros((120, 210))

a = 0


def collect_results(result):
    global results
    global a
    for i in range(result[3]):
        for j in range(result[3]):
            if result[1] + i < 110 and result[0] + j < 200:
                results[result[1] + i + 5][result[0] + j + 5] += result[2]
    # print(result[2])
    if result[0] // 2 != a:
        a = result[0] // 2
        print(a, '%')


omega = 2 * math.pi * 27e9
c = 299792458
lam = c / (27 * 10 ** 9)
beta = 2 * math.pi / lam
mu0 = 4e-7 * math.pi
eps0 = 1 / (mu0 * c ** 2)
facEpsbrick = math.sqrt(1 / 4.6)
facEpsconcrete = math.sqrt(1 / 5)
epsCconcrete = complex(5 * eps0, -(0.014 / omega))
epsCbrick = complex(4.6 * eps0, -(0.02 / omega))

alphaMconcrete = omega * math.sqrt(5 / 2 / c) * math.sqrt((math.sqrt(1 + (0.014 / omega / 5 / 8.854e-12) ** 2) - 1))
alphaMbrick = omega * math.sqrt(4.6 / c / 2) * math.sqrt((math.sqrt(1 + (0.02 / omega / 4.6 / 8.854e-12) ** 2) - 1))
betaMconcrete = omega * math.sqrt(5 / c / 2) * math.sqrt((1 + math.sqrt(1 + (0.014 / omega / 5 / 8.854e-12) ** 2) + 1))
betaMbrick = omega * math.sqrt(4.6 / c / 2) * math.sqrt((1 + math.sqrt(1 + (0.02 / omega / 4.6 / 8.854e-12) ** 2) + 1))
Z1 = mu0 * c
Z2concrete = cmath.sqrt(mu0 / epsCconcrete)
Z2brick = cmath.sqrt(mu0 / epsCbrick)


# @guvectorize('complex64(float32, float32, int8, int8, int8, int8)', target='cuda')
# @numba.cuda.jit('void(float32, float32, int8, int8, int8, int8)')
def reflexionPower(dx, dy, nbHc, nbVc, nbHb, nbVb, ray):
    coef = 1
    alphaMconcrete = 1.1793519138628281
    alphaMbrick = 1.756512304000713
    beta = 565.878155926954
    betaMconcrete = 1265.3425732375354
    betaMbrick = 1213.674704016611
    Z1 = 376.73031346177066
    Z2concrete = (168.47869848039613 + 0.15702915534584408j)
    Z2brick = (175.6508624825743 + 0.2542138351688341j)
    d = math.sqrt(dx ** 2 + dy ** 2)
    if nbHc != 0:
        cosOi = -dy / d
        sinOi = dx / d
        cosOt = math.sqrt(1 - sinOi ** 2 / 5)
        gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOt) / (Z2concrete * abs(cosOi) + Z1 * cosOt)
        u = cmath.exp(complex(-alphaMconcrete,
                              (
                                  facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
        gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
        coef *= abs(gammaM) ** (2 * nbHc)
    if nbVc != 0:
        cosOi = dx / d
        sinOi = dy / d
        cosOt = math.sqrt(1 - sinOi ** 2 / 5)
        gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOt) / (Z2concrete * abs(cosOi) + Z1 * cosOt)
        u = cmath.exp(complex(-alphaMconcrete,
                              (
                                  facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
        gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
        coef *= abs(gammaM) ** (2 * nbVc)
    if nbHb != 0:
        cosOi = -dy / d
        sinOi = dx / d
        cosOt = math.sqrt(1 - sinOi ** 2 / 4.6)
        gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOt) / (Z2brick * abs(cosOi) + Z1 * cosOt)
        u = cmath.exp(complex(-alphaMbrick,
                              (
                                  facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
        gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
        coef *= abs(gammaM) ** (2 * nbHb)

    if nbVb != 0:
        cosOi = dx / d
        sinOi = dy / d
        cosOt = math.sqrt(1 - sinOi ** 2 / 4.6)
        gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOt) / (Z2brick * abs(cosOi) + Z1 * cosOt)
        u = cmath.exp(complex(-alphaMbrick,
                              (
                                  facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
        gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
        coef *= abs(gammaM) ** (2 * nbVb)
    # print(nbVb, nbHc, nbVc, nbHb, coef, dx, dy)
    E = coef / d ** 2
    # E=1
    return E


def calculatePower(x, y, wallsh, wallsv, precision, antenna):
    ray = Ray(antenna[0], antenna[1], x + precision // 2, y + precision // 2)
    rays = getRayImage(antenna[0], antenna[1], wallsh, wallsv, ray)
    power = 0

    dx = np.zeros(len(rays), dtype=np.float32)
    dy = np.zeros(len(rays), dtype=np.float32)
    nbWallsHc = np.zeros(len(rays), dtype=np.int8)
    nbWallsVc = np.zeros(len(rays), dtype=np.int8)
    nbWallsHb = np.zeros(len(rays), dtype=np.int8)
    nbWallsVb = np.zeros(len(rays), dtype=np.int8)
    En_carre = np.zeros(len(rays), dtype=np.float32)
    Z0 = 376.730313
    Ra = 73
    c = 299792458
    lam = c / (27 * 10 ** 9)
    he = -lam / math.pi
    factor = he ** 2 / 8 / Ra
    Gtx = 1.6977
    Ptx = 0.1  # [W]
    for i in range(len(rays)):
        r = rays[i]
        if len(r.imagePoints) != 0:
            dx[i], dy[i] = r.receiverX - r.imagePoints[-1][0], r.receiverY - r.imagePoints[-1][1]
            for wall in r.walls:
                if wall.mat == 1:
                    if wall.xDirection == 0:
                        nbWallsVc[i] += 1
                    else:
                        nbWallsHc[i] += 1
                elif wall.mat == 0:
                    if wall.xDirection == 0:
                        nbWallsVb[i] += 1
                    else:
                        nbWallsHb[i] += 1
        else:
            dx[i], dy[i] = r.receiverX - r.originX, r.receiverY - r.originY
            # print('okok')

        En_carre[i] = reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i], r)
        En_carre[i] *= r.getTcoef(wallsh, wallsv)
        a = 1
    for e in En_carre:
        power += e
    power *= factor * 60 * Gtx * Ptx
    return x, y, power, precision


def main(antenna, i):
    init_time = datetime.now()
    pool = mp.Pool(12)
    global results
    MAPstyle = 2  # 1(corner) or 2(MET)
    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)
    precision = 1  # m^2
    for x in range(200 // precision):
        for y in range(110 // precision):
            if [x * precision + precision // 2, y * precision + precision // 2] == antenna:
                # results[x * precision + precision // 2, y * precision + precision // 2] += 0.1
                a = 1
            else:
                pool.apply_async(calculatePower,
                                 args=(x * precision, y * precision, wallsh, wallsv, precision, antenna),
                                 callback=collect_results)
    print("c'est : ", calculatePower(190, 90, wallsh, wallsv, precision, antenna))
    pool.close()
    pool.join()
    end_time = datetime.now()
    print("Execution time: ", (end_time - init_time))
    #dp.displayDPM(MAPstyle, results, antennas)
    #dp.displayDebit(MAPstyle, results, antennas)
    w = str(i)
    with open('antenna' + w, 'wb') as f:
        np.save(f, results)
    f.close()


"""MAPstyle = 2  # 1(corner) or 2(MET)
walls = Map.getWalls(MAPstyle)
wallsh = Map.getWallsH(walls)
wallsv = Map.getWallsV(walls)
if MAPstyle == 1:
    ray = Ray(0, 0, 0, 5)
    rays = getRayImages(0, 0, walls, ray)
else:
    ray = Ray(100, 45, 100, 40)
    init_time = datetime.now()
    rays = getRayImage(100, 45, wallsh, wallsv, ray)
    fin_time = datetime.now()
    print("Execution time image: ", (fin_time - init_time))
print(len(rays))
power = 0
E = np.zeros(len(rays), dtype=np.float32)
dx = np.zeros(len(rays), dtype=np.float32)
dy = np.zeros(len(rays), dtype=np.float32)
nbWallsHc = np.zeros(len(rays), dtype=np.int8)
nbWallsVc = np.zeros(len(rays), dtype=np.int8)
nbWallsHb = np.zeros(len(rays), dtype=np.int8)
nbWallsVb = np.zeros(len(rays), dtype=np.int8)
Z0 = 376.730313
Ra = 73
c = 299792458
lam = c/(27 * 10**9)
he = -lam/math.pi
factor = he**2/8/Ra
Gtx = 1.6977
Ptx = 0.1   # [W]
En_carre = np.zeros(len(rays), dtype=np.float32)
init_time = datetime.now()
for i in range(len(rays)):
    r = rays[i]
    try:
        dx[i], dy[i] = r.receiverX-r.imagePoints[-1][0] , r.receiverY-r.imagePoints[-1][1]
        for wall in r.walls:
            if wall.mat == 1:
                if wall.Xdirection == 0:
                    nbWallsVc[i] += 1
                else:
                    nbWallsHc[i] += 1
            if wall.mat == 0:
                if wall.Xdirection == 0:
                    nbWallsVb[i] += 1
                else:
                    nbWallsHb[i] += 1
    except:
        dx[i], dy[i] = r.receiverX-r.originX , r.receiverY-r.originY

    En_carre[i] = reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i], E[i])
    En_carre[i] *= r.getTcoef(wallsh, wallsv)
for e in En_carre:
    power += e
power *= factor * 60*Gtx*Ptx
print(power)
fin_time = datetime.now()
print("Execution time: ", (fin_time - init_time))
dp.display(MAPstyle, rays)"""

# print("Number of processors: ", mp.cpu_count())


if __name__ == '__main__':
    antennas = [[79, 31]]
    # freeze_support() here if program needs to be frozen
    for i in range(len(antennas)):
        results = np.zeros((120, 210))
        main(antennas[i], i)  # execute this only when run directly, not when imported!
        results = np.zeros((120, 210))


"""7.288447357455732e-09
7.288447357455732e-09
9.899063005576875e-09
2.457860267550925e-08
9.899063005576875e-09
2.457860267550925e-08
7.076678956532395e-08
7.076678956532395e-08
2.6830825231432408e-08
2.6830825231432408e-08
3.820327510784149e-08
3.820327510784149e-08
3.1374440275840464e-07
3.1374440275840464e-07
4.345622543516969e-08
4.345622543516969e-08
7.784682071154845e-09
7.784682071154845e-09
1.0260822783189319e-08
1.0260822783189319e-08
Execution time:  0:00:16.849826

Process finished with exit code 0"""
