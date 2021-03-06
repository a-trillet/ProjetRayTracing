import math

import Display
import Map
from Ray import *
import temporaire as dp
from ImageMethod import *
import multiprocessing as mp
import numpy as np
from datetime import datetime


results = np.zeros((120, 210))

a = 0


def collect_results(result):
    """collecte les résultat et les place dans une matrice"""
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

alphaMconcrete = omega * math.sqrt(5 / 2) * math.sqrt(math.sqrt(1 + (0.014 / (omega * 5 * eps0)) ** 2) - 1) / c
alphaMbrick = omega * math.sqrt(4.6 / 2) * math.sqrt(math.sqrt(1 + (0.02 / (omega * 4.6 * eps0)) ** 2) - 1) / c
betaMconcrete = omega * math.sqrt(5 / 2) * math.sqrt(math.sqrt(1 + (0.014 / (omega * 5 * eps0)) ** 2) + 1) / c
betaMbrick = omega * math.sqrt(4.6 / 2) * math.sqrt(math.sqrt(1 + (0.02 / (omega * 4.6 * eps0)) ** 2) + 1) / c

Z1 = mu0 * c
Z2concrete = cmath.sqrt(mu0 / epsCconcrete)
Z2brick = cmath.sqrt(mu0 / epsCbrick)


# @guvectorize('complex64(float32, float32, int8, int8, int8, int8)', target='cuda')
# @numba.cuda.jit('void(float32, float32, int8, int8, int8, int8)')
def reflexionPower(dx, dy, nbHc, nbVc, nbHb, nbVb):
    """calcule les coefficients de réflexion et retourne le champ électrique multiplié
    par ce coefficient"""
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
        print("Gamma m béton", gammaM)
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
        print("Gamma m brick:", gammaM)
        coef *= abs(gammaM) ** (2 * nbVb)
    E = coef / d ** 2
    #E=1
    return E


def calculatePower(x, y, wallsh, wallsv, precision, antenna):
    """calcule la puissance en un point"""
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
        En_carre[i] = reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i])
        En_carre[i] *= r.getTcoef(wallsh, wallsv)
    for e in En_carre:
        power += e
    print(En_carre)
    power *= factor * 60 * Gtx * Ptx
    return x, y, power, precision


def main(antenna, i):
    """calcule la puissance en tout point. Cette fonction utilise le multiprocessing"""
    init_time = datetime.now()
    pool = mp.Pool(8)
    global results
    MAPstyle = 1  # 1(corner) or 2(MET)
    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)
    precision = 1  # m^2
    for x in range(200 // precision):
        for y in range(110 // precision):
            if [x * precision + precision // 2, y * precision + precision // 2] == antenna:
                a = 1
            else:
                pool.apply_async(calculatePower,
                                 args=(x * precision, y * precision, wallsh, wallsv, precision, antenna),
                                 callback=collect_results)
    pool.close()
    pool.join()

    end_time = datetime.now()
    print("Execution time: ", (end_time - init_time))

    w = str(i+39)
    with open('antenna' + w, 'wb') as f:
        np.save(f, results)
    f.close()


if __name__ == '__main__':
    # antennas = [[40, 20], [100, 90], [170, 20]]
    antennas = [[100, 45]]
    # freeze_support() here if program needs to be frozen
    for i in range(len(antennas)):
        results = np.zeros((120, 210))
        main(antennas[i], i)  # execute this only when run directly, not when imported!
        results = np.zeros((120, 210))
