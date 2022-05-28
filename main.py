import math
yMAP = 140
xMAP = 130
nbReflexion = 2
precision = 1  # m^2
import Display
import Map
from Ray import *
from DiffRay import *
from ImageMethod import *
import multiprocessing as mp
import numpy as np
from datetime import datetime

results = np.zeros((yMAP + 10, xMAP + 10))
a = 0
recv = [[40, 60], [80, 80]]
recvreal = [[40+precision/2, 60+precision/2], [80+precision/2, 80+precision/2]]
raysToPlot = []


def collect_results(result):
    """collecte les résultat et les place dans une matrice"""
    global results
    global a
    for i in range(precision):
        for j in range(precision):
            if result[1] + i < yMAP and result[0] + j < xMAP:
                results[result[1] + i + 5][result[0] + j + 5] += result[2]
    # print(result[2])
    if result[0] // 2 != a:
        a = result[0] // 2
        #print(a, '%')
    if [result[0], result[1]] == recv[0] or [result[0], result[1]] == recv[1]:
        for thing in result[3]:
            raysToPlot.append(thing)


permRel = 4.5
freq = 26e9
omega = 2 * math.pi * freq
c = 299792458
lam = c / freq
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
    """calcule les coefficients de réflexion et retourne le phaseur du champ électrique multiplié
    par ce coefficient"""
    coef = 1
    cosOi = 0
    sinOi = 0
    # alphaMconcrete = 1.1793519138628281
    # alphaMbrick = 1.756512304000713
    # beta = 565.878155926954
    # betaMconcrete = 1265.3425732375354
    # betaMbrick = 1213.674704016611
    # Z1 = 376.73031346177066
    # Z2concrete = (168.47869848039613 + 0.15702915534584408j)
    # Z2brick = (175.6508624825743 + 0.2542138351688341j)
    d = math.sqrt(dx ** 2 + dy ** 2)
    if nbHc != 0:
        cosOi = -dy / d
        sinOi = dx / d
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= abs(GammaPerp) ** nbHc
    if nbVc != 0:
        cosOi = dx / d
        sinOi = dy / d
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= abs(GammaPerp) ** nbVc
    if nbHb != 0:
        cosOi = -dy / d
        sinOi = dx / d
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= abs(GammaPerp) ** nbHb

    if nbVb != 0:
        cosOi = dx / d
        sinOi = dy / d
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= abs(GammaPerp) ** nbVb
    E = coef / d * cmath.exp(complex(0, -beta * d))   #En phaser for this ray

    print("cosOi = ", cosOi, " and sinOi = ", sinOi)
    return E


def calculatePower(x, y, wallsh, wallsv, antenna):
    """calcule la puissance en un point"""
    global raysToPlot
    dx, dy = x + precision / 2 - antenna[0], y + precision / 2 - antenna[1]
    if math.sqrt(dx ** 2 + dy ** 2) < 10:
        return x, y, 0, precision                      #only receivers further than 10 meters are computed

    ray = Ray(antenna[0], antenna[1], x + precision / 2, y + precision / 2)
    rays = getRayImage(antenna[0], antenna[1], wallsh, wallsv, ray)
    finalrays = []
    VocTot = 0

    dx = np.zeros(len(rays), dtype=np.float32)
    dy = np.zeros(len(rays), dtype=np.float32)
    nbWallsHc = np.zeros(len(rays), dtype=np.int8)
    nbWallsVc = np.zeros(len(rays), dtype=np.int8)
    nbWallsHb = np.zeros(len(rays), dtype=np.int8)
    nbWallsVb = np.zeros(len(rays), dtype=np.int8)
    # Z0 = 376.730313
    Ra = 73
    heXY = -lam / math.pi
    # Gtx = 1.6977
    # Ptx = 0.1471  # [W]
    # sqEIRP = math.sqrt(60 * Gtx * Ptx)  # 60 ~~ 2*Z0/4pi
    sqEIRP = 3.873

    for i in range(len(rays)):
        r = rays[i]
        [blockingWall, wallsBlocking] = r.checkBlockingWall(wallsh,wallsv)
        if len(r.imagePoints) != 0:  # only reflexions
            # if False:
            if not blockingWall:
                finalrays.append(r)
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
                VocTot += sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i]) # reflexion Vov computation

        else:
            if not blockingWall:  # add ground reflexion and compute En for LOS
                finalrays.append(r)
                dx[i], dy[i] = r.receiverX - r.originX, r.receiverY - r.originY
                VocTot += sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i])  # computes LOS Voc
                # add the ground reflexion
                VocTot += r.getGroundReflexion(lam)


            else:
                listdiffrays = []
                usedCorner = []
                for wall in wallsBlocking:
                    diffraction1 = DiffRay(antenna[0], antenna[1], x + precision / 2, y + precision / 2, wall.origin[0], wall.origin[1])
                    diffraction2 = DiffRay(antenna[0], antenna[1], x + precision / 2, y + precision / 2, wall.origin[0]+wall.xDirection, wall.origin[1]+ wall.yDirection)
                    if diffraction1.isacceptable(wallsh, wallsv) and [wall.origin[0], wall.origin[1]] not in usedCorner:
                        usedCorner.append([wall.origin[0], wall.origin[1]])
                        listdiffrays.append(diffraction1)
                    if diffraction2.isacceptable(wallsh, wallsv) and [wall.origin[0]+wall.xDirection, wall.origin[1] + wall.yDirection] not in usedCorner:
                        usedCorner.append([wall.origin[0]+wall.xDirection, wall.origin[1] + wall.yDirection])
                        listdiffrays.append(diffraction2)
                for elem in listdiffrays:
                    finalrays.append(elem)
                    dx[i], dy[i] = r.receiverX - r.originX, r.receiverY - r.originY
                    VocTot += elem.diffractionCoef(beta) * sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i])

        # transmission not considered
        # En_carre[i] *= r.getTcoef(wallsh, wallsv)
    """for e in Voc:
        VocTot += e"""
    power = abs(VocTot) ** 2 / (8 * Ra)
    return x, y, power, finalrays


def main(antenna, i):
    """calcule la puissance en tout point. Cette fonction utilise le multiprocessing"""

    init_time = datetime.now()
    pool = mp.Pool(8)
    global raysToPlot
    global results
    MAPstyle = 4  # 1(corner) or 2(MET) or 3 Grand Place
    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)
    difTest = DiffRay(45,90,85,120,80,100)
    print(difTest.isacceptable(wallsh,wallsv))
    print(difTest.diffractionCoef(beta))
    for x in range(xMAP // precision):
        for y in range(yMAP // precision):
            if [x * precision + precision // 2, y * precision + precision // 2] == antenna:
                a = 1
            else:
                pool.apply_async(calculatePower,
                                 args=(x * precision, y * precision, wallsh, wallsv, antenna),
                                 callback=collect_results)

    pool.close()
    pool.join()
    end_time = datetime.now()
    print("Execution time: ", (end_time - init_time))

    w = str(i+0)
    with open('GrandPlace' + w, 'wb') as f:
        np.save(f, results)
    f.close()
    print(len(raysToPlot))
    return raysToPlot


if __name__ == '__main__':
    # antennas = [[40, 20], [100, 90], [170, 20]]
    antennas = [[20, 80]]# [[45, 95]]

    # freeze_support() here if program needs to be frozen
    for i in range(len(antennas)):
        results = np.zeros((yMAP + 10, xMAP + 10))
        raysToPlot = main(antennas[i], i)  # execute this only when run directly, not when imported!
        print("nb of rays to plot: ", len(raysToPlot))
        Display.displayRays(4, raysToPlot, antennas[i], recvreal, results)
        results = np.zeros((yMAP + 10, xMAP + 10))



