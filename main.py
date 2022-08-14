yMAP = 140
xMAP = 130
nbReflexion = 2
precision = 1  # m^2
MAPstyle = 3  # 1(corner) or 2(MET) or 3 Grand Place
recv = [[125, 74]]  # [[90, 5]] eastern corner [[65,50]] center  # reception antennas for Impulse response and displaying rays
recvreal = [i for i in range(len(recv))]
for i in range(len(recv)):
    recvreal[i] = [recv[i][0] + precision / 2, recv[i][1] + precision / 2]
raysToPlot = []

import math
import Display
import Map
from Ray import *
from DiffRay import *
from ImageMethod import *
import multiprocessing as mp
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import special

B = 1e6  # bandwidth
noiseFigure = 12  # dB
k = 1.379 * 10 ** (-23)
T = 300  # K
factorSNR = noiseFigure + 10 * np.log10(k * T * B)

results = np.zeros((yMAP + 10, xMAP + 10))
delaySpread = np.zeros((yMAP + 10, xMAP + 10))
riceFactor = np.zeros((yMAP + 10, xMAP + 10))
SNRmap = np.zeros((yMAP + 10, xMAP + 10))
listForImpResp = []

a = 0
c = 299792458
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

def collect_results(result):
    """collecte les résultat et les place dans une matrice"""
    global results
    global a
    for i in range(precision):
        for j in range(precision):
            if result[1] + i < yMAP and result[0] + j < xMAP:
                results[result[1] + i + 5][result[0] + j + 5] += result[2]
                try:
                    riceFactor[result[1] + i + 5][result[0] + j + 5] += result[4]
                except:
                    donothing = 1
                        #print("tuple index out of range")
                delay = 0
                mindist = 1000
                maxdist = 0
                try:
                    if len(result[3]) > 1:
                        for elem in result[3]:
                            raylen = elem.getLength()
                            if raylen > maxdist:
                                maxdist = raylen
                            if raylen < mindist:
                                mindist = raylen
                        delay = (maxdist - mindist) / c
                except:
                    print("result3 is int")
                delaySpread[result[1] + i + 5][result[0] + j + 5] += delay

    # print(result[2])
    if result[0] // 2 != a:
        a = result[0] // 2
        # print(a, '%')
    if [result[0], result[1]] in recv:
        for thing in result[3]:
            raysToPlot.append(thing)
            print(thing.getLength())


def reflexionPower(dx, dy, nbHc, nbVc, nbHb, nbVb, nbHm, nbVm):
    """calcule les coefficients de réflexion et retourne le phaseur du champ électrique multiplié
    par ce coefficient
    nb for number of
    H for horizontal walls
    V for vertical walls
    c for concrete
    b for brick
    m for metal"""
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
        sinOi = abs(dx) / d
        Oi = math.asin(sinOi)
        cosOi = math.cos(Oi)
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        # print(GammaPerp)
        coef *= GammaPerp ** nbHc
    if nbVc != 0:
        sinOi = abs(dy) / d
        Oi = math.asin(sinOi)
        cosOi = math.cos(Oi)
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= GammaPerp ** nbVc
    if nbHb != 0:
        sinOi = abs(dx) / d
        Oi = math.asin(sinOi)
        cosOi = math.cos(Oi)
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        coef *= GammaPerp ** nbHb

    if nbVb != 0:
        sinOi = abs(dy) / d
        Oi = math.asin(sinOi)
        cosOi = math.cos(Oi)
        temp = math.sqrt(1 - (sinOi ** 2) / permRel) * math.sqrt(permRel)
        GammaPerp = (cosOi - temp) / (cosOi + temp)
        # print(GammaPerp)
        coef *= GammaPerp ** nbVb

    if nbHm != 0:
        GammaPerp = -1
        coef *= GammaPerp ** nbHm

    if nbVm != 0:
        GammaPerp = -1
        coef *= GammaPerp ** nbVm
    E = coef / d * cmath.exp(complex(0, -beta * d))  # En phaser for this ray
    return E


def calculatePower(x, y, wallsh, wallsv, antenna):
    # next if for tests
    if [x, y] in recv:
        donothing = 1
    """calcule la puissance en un point"""
    global raysToPlot
    dx, dy = x + precision / 2 - antenna[0], y + precision / 2 - antenna[1]
    if math.sqrt(dx ** 2 + dy ** 2) < 10:
        return x, y, 0, precision  # only receivers further than 10 meters are computed

    ray = Ray(antenna[0], antenna[1], x + precision / 2, y + precision / 2)
    rays = getRayImage(antenna[0], antenna[1], wallsh, wallsv, ray)
    finalrays = []
    VocTot = 0
    PLos = 0
    PMulti = 0
    listImpResp = []

    dx = np.zeros(len(rays), dtype=np.float32)
    dy = np.zeros(len(rays), dtype=np.float32)
    nbWallsHc = np.zeros(len(rays), dtype=np.int8)
    nbWallsVc = np.zeros(len(rays), dtype=np.int8)
    nbWallsHb = np.zeros(len(rays), dtype=np.int8)
    nbWallsVb = np.zeros(len(rays), dtype=np.int8)
    nbWallsHm = np.zeros(len(rays), dtype=np.int8)
    nbWallsVm = np.zeros(len(rays), dtype=np.int8)
    # Z0 = 376.730313
    Ra = 73
    heXY = -lam / math.pi
    # Gtx = 1.6977
    # Ptx = 0.1471  # [W]
    # sqEIRP = math.sqrt(60 * Gtx * Ptx)  # 60 ~~ 2*Z0/4pi
    sqEIRP = 3.873

    for i in range(len(rays)):
        temp = 0
        r = rays[i]
        [blockingWall, wallsBlocking] = r.checkBlockingWall(wallsh, wallsv)
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
                    elif wall.mat == 4:
                        if wall.xDirection == 0:
                            nbWallsVm[i] += 1
                        else:
                            nbWallsHm[i] += 1
                temp = sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i], nbWallsVb[i], nbWallsHm[i], nbWallsVm[i])
                VocTot += temp  # reflexion Vov computation
                PMulti += abs(temp) ** 2
        else:
            if not blockingWall:  # add ground reflexion and compute En for LOS
                finalrays.append(r)
                dx[i], dy[i] = r.receiverX - r.originX, r.receiverY - r.originY
                temp = sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i], nbWallsVc[i], nbWallsHb[i],
                                                      nbWallsVb[i], nbWallsHm[i], nbWallsVm[i])  # computes LOS Voc
                VocTot += temp
                PLos = abs(temp) ** 2

                # add the ground reflexion
                temp1, lengthGND = r.getGroundReflexion(lam)
                VocTot += temp1
                PMulti += abs(temp1) ** 2
                # for GND need to add the ray manually as the real ray does not exist
                listImpResp.append([temp1 , lengthGND])

            else:
                listdiffrays = []
                usedCorner = []
                for wall in wallsBlocking:
                    diffraction1 = DiffRay(antenna[0], antenna[1], x + precision / 2, y + precision / 2, wall.origin[0],
                                           wall.origin[1])
                    diffraction2 = DiffRay(antenna[0], antenna[1], x + precision / 2, y + precision / 2,
                                           wall.origin[0] + wall.xDirection, wall.origin[1] + wall.yDirection)
                    if diffraction1.isacceptable(wallsh, wallsv) and [wall.origin[0], wall.origin[1]] not in usedCorner:
                        usedCorner.append([wall.origin[0], wall.origin[1]])
                        listdiffrays.append(diffraction1)
                    if diffraction2.isacceptable(wallsh, wallsv) and [wall.origin[0] + wall.xDirection, wall.origin[
                                                                                                            1] + wall.yDirection] not in usedCorner:
                        usedCorner.append([wall.origin[0] + wall.xDirection, wall.origin[1] + wall.yDirection])
                        listdiffrays.append(diffraction2)
                for elem in listdiffrays:
                    finalrays.append(elem)
                    dx[i], dy[i] = r.receiverX - r.originX, r.receiverY - r.originY
                    temp = elem.diffractionCoef(beta) * sqEIRP * heXY * reflexionPower(dx[i], dy[i], nbWallsHc[i],
                                                                                       nbWallsVc[i], nbWallsHb[i],
                                                                                       nbWallsVb[i], nbWallsHm[i], nbWallsVm[i])
                    VocTot += temp
                    PMulti += abs(temp) ** 2
        # list for impulse reponse
        listImpResp.append([temp, r.getLength()])
        # transmission not considered
        # En_carre[i] *= r.getTcoef(wallsh, wallsv)
    """for e in Voc:
        VocTot += e"""
    power = abs(VocTot) ** 2 / (8 * Ra)

    return x, y, power, finalrays, PLos / PMulti, listImpResp


def main(antenna, i):
    """calcule la puissance en tout point. Cette fonction utilise le multiprocessing"""

    init_time = datetime.now()
    pool = mp.Pool(1)
    global raysToPlot
    global results

    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)

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

    w = str(i + 0)
    with open('GrandPlace' + w, 'wb') as f:
        np.save(f, results)
    f.close()
    with open('DelaySpread' + w, 'wb') as f:
        np.save(f, delaySpread)
    f.close()
    print(len(raysToPlot))
    return raysToPlot


def main1D(antenna):
    taps = 500
    results1D = np.zeros(taps)
    delaySpread1D = np.zeros(taps)
    riceFactor1D = np.zeros(taps)
    SNR1D = np.zeros(taps)

    antennas1Dx = np.linspace(50, 90, taps)  #grand place
    antennas1Dy = np.linspace(90, 0, taps)
   # antennas1Dx = np.linspace(35, -56, taps)  # tete d'or
   # antennas1Dy = np.linspace(95, 95, taps)
    distance = np.sqrt((antennas1Dx - 45) ** 2 + (antennas1Dy - 95) ** 2)

    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)

    for i in range(taps):
        res = calculatePower(antennas1Dx[i], antennas1Dy[i], wallsh, wallsv, antenna)
        results1D[i] = res[2]
        try:
            riceFactor1D[i] = res[4]
        except:
            print("tuple index out of range")
        delay = 0
        mindist = 1000
        maxdist = 0
        try:
            if len(res[3]) > 1:
                for elem in res[3]:
                    raylen = elem.getLength()
                    if raylen > maxdist:
                        maxdist = raylen
                    if raylen < mindist:
                        mindist = raylen
                delay = (maxdist - mindist) / c
        except:
            donothing = 1
                # print("result3 is int")
        delaySpread1D[i] = delay
        if res[2] < 10 ** (-14):
            SNR1D[i] = 10 * np.log10(10 ** (-14)) - factorSNR
        elif res[2] > 10 ** (-6):
            SNR1D[i] = 10 * np.log10(10 ** (-6)) - factorSNR
        else:
            SNR1D[i] = 10 * np.log10(res[2]) - factorSNR

    # plots
    Power1D = 10 * np.log10(1000 * results1D)
    # removing first 5 element that are infinite
    #distanceCorr = distance
    indexArray = [t for t in range(math.ceil(len(Power1D)/30), len(Power1D))]
    Power1D = Power1D[indexArray]
    distanceCorr = distance[indexArray]
    SNR1D = SNR1D[indexArray]
    delaySpread1D = delaySpread1D[indexArray]
    riceFactor1D = 10*np.log10(riceFactor1D[indexArray])

    logDist = np.log10(distanceCorr)
    coeffs = np.polyfit(logDist, Power1D, deg=1)
    poly = np.poly1d(coeffs)
    powerFit = poly(logDist)
    plt.semilogx(distanceCorr, Power1D)
    plt.semilogx(distanceCorr, powerFit)
    plt.xlabel('distance[m]')
    plt.ylabel('power received [dBm]')
    plt.title('BS to eastern corner 1D plot - Path Loss model')
    #plt.title("Rue de la Tête d'OR - Path Loss model")
    plt.legend(['Prx : data', '<Prx> : 1st order fitting curve(in log)'])
    plt.show()
    variance = np.var(Power1D-powerFit)
    print("std dev: ", math.sqrt(variance), '<Prx(10m)> ', poly(math.log10(10)), "n = ", -(poly(2)-poly(1))/10)
    plt.semilogx(distanceCorr, Power1D-powerFit)
    plt.semilogx(distanceCorr, powerFit-powerFit)
    plt.xlabel('distance[m]')
    plt.ylabel('power received - mean received power [dBm]')
    plt.title('BS to eastern corner 1D plot - Fading variability')
    plt.show()
    plt.plot(distanceCorr, Power1D)
    plt.xlabel('distance[m]')
    plt.ylabel('power received [dBm]')
    plt.title('BS to eastern corner 1D plot - Power received [dBm]')
    plt.show()
    plt.plot(distanceCorr, SNR1D)
    plt.xlabel('distance[m]')
    plt.ylabel('SNR [dB]')
    plt.title('BS to eastern corner 1D plot - SNR [dB]')
    plt.show()
    plt.plot(distanceCorr, delaySpread1D)
    plt.xlabel('distance[m]')
    plt.ylabel('delay spread [s]')
    plt.title('BS to eastern corner 1D plot - Delay spread [s]')
    plt.show()
    plt.plot(distanceCorr, riceFactor1D)
    plt.xlabel('distance[m]')
    plt.ylabel('rice factor')
    plt.title('BS to eastern corner 1D plot - Rice Factor[dB]')
    plt.show()
    return math.sqrt(variance), poly(math.log10(10)), -(poly(2)-poly(1))/10 # std dev, Prx(10m), n


def mainImpulseResponse(antenna):
    # antennaRX = [65, 50]
    antennaRX = [90, 0.5]
    antennaTX = antenna

    walls = Map.getWalls(MAPstyle)
    wallsh = Map.getWallsH(walls)
    wallsv = Map.getWallsV(walls)
    res = calculatePower(antennaRX[0], antennaRX[1], wallsh, wallsv, antennaTX)
    distMax = 300
    timeaxis = np.arange(0, distMax / c, 1 / (2 * B))
    taps = np.arange(0, distMax/c, 1/B)
    impPhys = np.zeros(len(timeaxis), dtype=np.complex_)
    impTDL = np.zeros(len(taps), dtype=np.complex_)

    for impulse in res[5]:
        index = 0
        #index = round(impulse[1] / distMax * len(timeaxis))
        impPhys[index] += impulse[0]
        impTDL += impulse[0] * np.sinc(B * (impulse[1] / c - taps))

    plt.stem(timeaxis, abs(impPhys))
    plt.xlabel('time[s]')
    plt.ylabel('|h(t)|')
    plt.title('Eastern corner - Physical impulse response')
    plt.show()
    plt.stem(taps, abs(impTDL))
    plt.xlabel('time[s]')
    plt.ylabel('|h_tdl(t,τ)|')
    plt.title('Eastern corner - Tapped delay line impusle response (B =' + str(round(B/1000000)) + ' MHz)')
    plt.show()


def calculateSNR():
    for i in range(len(results)):
        for j in range(len(results[0])):
            if results[i][j] < 10 ** (-14):
                SNRmap[i][j] = 10 * np.log10(10 ** (-14)) - factorSNR
            elif results[i][j] > 10 ** (-6):
                SNRmap[i][j] = 10 * np.log10(10 ** (-6)) - factorSNR
            else:
                SNRmap[i][j] = 10 * np.log10(results[i][j]) - factorSNR


def computeCellRange(Prx10m, n, sygmaL):
    proba = np.arange(0, 0.501, 0.001)
    sensitivity = -73.84
    # computing the fade margin for a certain proba of connection at cell edge
    fademargin = math.sqrt(2) * sygmaL * special.erfinv(2 * proba)
    cellRange = 10 * np.power(10, (Prx10m-sensitivity-fademargin) / (10*n))

    plt.plot(proba + 0.5, cellRange)
    plt.xlabel('probability of connection')
    plt.ylabel('cell range [m]')
    plt.title('Cell range in function of the probability of connection at cell edge')
    plt.show()
    return 0


if __name__ == '__main__':

    # antennas = [[60, 100 - (2/4*lam + 0.1)], [60, 100 - (4/4*lam + 0.1)], [60, 100 - (5/4*lam + 0.1)], [60, 100 - (6/4*lam + 0.1)]]  # [[45, 95]]
    # antennas = [[65, 0 + (0.97 * lam + 0.1)]]  # [[45, 95]]
    antennas = [[45, 95]]
    mainImpulseResponse(antennas[0])

    symgaL, PRX10, n = main1D(antennas[0])
    computeCellRange(PRX10, n, symgaL)
    # freeze_support() here if program needs to be frozen
    for i in range(len(antennas)):
        results = np.zeros((yMAP + 10, xMAP + 10))
        raysToPlot = main(antennas[i], i)  # execute this only when run directly, not when imported!
        print("nb of rays to plot: ", len(raysToPlot))
        Display.displayRays(MAPstyle, raysToPlot, antennas, recvreal, results, 'Received power [dBm]')
        Display.heatmapDisplay(MAPstyle, antennas[i], delaySpread, 'Delay spread [s]')
        Display.heatmapDisplay(MAPstyle, antennas[i], 10*np.log10(riceFactor), 'RiceFactor[dB]')
        calculateSNR()
        Display.heatmapDisplay(MAPstyle, antennas[i], SNRmap, 'SNR (B= 200MHz)')
        riceFactor = np.zeros((yMAP + 10, xMAP + 10))
        delaySpread = np.zeros((yMAP + 10, xMAP + 10))

        results = np.zeros((yMAP + 10, xMAP + 10))
