import Map
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

"""init_time = datetime.now()
walls = Map.getWalls(2)
wallsH = Map.getWallsH(walls)
wallsV = Map.getWallsV(walls)
fin_time = datetime.now()
print("Execution time: ", (fin_time - init_time))"""

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

"""
def display(map_style, rays):
    a = 200
    b = 110
    x = np.linspace(-5, a + 4, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 4, b + 10)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(19, 9))

    Z = X * np.cos(Y / 5) * 0
    Z[60+5][60+5] = 200
    plt.pcolor(X, Y, Z, cmap=plt.cm.turbo)
    plt.colorbar()

    for i in Map.getWalls(map_style):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            plt.plot(x1, y1, c="blue", lw=1)
        elif i.mat == 1:
            plt.plot(x1, y1, c="gray", lw=1)

    plt.scatter(100, 45, c="black")  # point émetteur initial

    plt.scatter(0, 0, c="black")
    plt.scatter(0, 5, c="black")
    for ray in rays:
        try:
            x1 = [ray.Ppoints[0], ray.receiverX]
            y1 = [ray.Ppoints[1], ray.receiverY]
            x2 = [ray.originX, ray.Ppoints[0]]
            y2 = [ray.originY, ray.Ppoints[1]]
        except:
            x1 = [ray.originX, ray.receiverX]
            y1 = [ray.originY, ray.receiverY]
            x2 = [0, 0]
            y2 = [0, 0]
        if len(ray.walls) == 0:
            plt.scatter(ray.receiverX, ray.receiverY, c="red")
        if ray.Ppoints6:
            plt.scatter(ray.Ppoints6[0][0], ray.Ppoints6[0][1], c='red')
        if ray.Ppoints5:
            plt.scatter(ray.Ppoints5[0][0], ray.Ppoints5[0][1], c='green')
        if ray.Ppoints4:
            plt.scatter(ray.Ppoints4[0][0], ray.Ppoints4[0][1], c='yellow')



        # plt.plot(x1, y1, ls="--")
        # plt.plot(x2, y2, ls="--")

        plt.title("figure 1")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()
"""

"""# créer un ray de base Ray(originX, originY, receiverX, receiverY))
def getRayImages(originX, originY, walls, oldRay):
    rays = []
    e = len(oldRay.imagePoints)
    if True:
        # rays.append(oldRay)
        if e < 3:
            for wall in walls:
                try:
                    if wall != oldRay.walls[-1]:
                        PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                        if PsSN != 0:
                            ray = copy.deepcopy(oldRay)
                            if True:
                                ray.walls.append(wall)
                                ray.imagePoints.append([originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY])
                                rays.extend(getRayImages(ray.imagePoints[e][0], ray.imagePoints[e][1], walls, ray))
                    # else:
                    # print("rayon // à un mur")
                # else:
                # print(wall.origin[0])
                # else:
                # print("chaud")
                except:
                    if not oldRay.imagePoints:
                        PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                        if PsSN != 0:
                            ray = copy.deepcopy(oldRay)
                            if True:
                                ray.walls.append(wall)
                                ray.imagePoints.append([originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY])
                                rays.extend(getRayImages(ray.imagePoints[e][0], ray.imagePoints[e][1], walls, ray))
                    # else:
                    # print("rayon // à un mur")
                # else:
                # print(wall.origin[0])
                # else:
                # print("chaud")n
    if oldRay.find_Points():
        rays.append(oldRay)
    return rays
"""

"""def getPower(self):  # en fait pas vraiment power mais |E|**2
    coefficients = 1
    # coefficients de reflexion:
    e = len(self.imagePoints)
    for i in range(e):
        wall = self.walls[i]
        dx = self.Ppoints[i][0] - self.imagePoints[i][0]
        dy = self.Ppoints[i][1] - self.imagePoints[i][1]
        d = math.sqrt(dx ** 2 + dy ** 2)

        cosOi = (dx * wall.nX + dy * wall.nY) / d
        sinOi = (dx * wall.nY - dy * wall.nX) / d
        cosOt = math.sqrt(1 - sinOi ** 2 / wall.relativePermitivity)
        if wall.mat == 1:
            gammaPerp = (self.Z2concrete * cosOi - self.Z1 * cosOt) / (self.Z2concrete * cosOi + self.Z1 * cosOt)
            u = cmath.exp(complex(-self.alphaMconcrete,
                                  (
                                      self.facEpsconcrete) * sinOi ** 2 * self.beta - self.betaMconcrete) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
            gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
            coefficients *= abs(gammaM)
        elif wall.mat == 0:
            gammaPerp = (self.Z2brick * cosOi - self.Z1 * cosOt) / (self.Z2brick * cosOi + self.Z1 * cosOt)
            u = cmath.exp(complex(-self.alphaMbrick,
                                  (self.facEpsbrick) * sinOi ** 2 * self.beta - self.betaMbrick) / cosOt)
            gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
            coefficients *= abs(gammaM)

    if not self.imagePoints:
        dn_carre = (self.receiverX - self.originX) ** 2 + (self.receiverY - self.originY) ** 2
    else:
        dn_carre = (self.receiverX - self.imagePoints[-1][0]) ** 2 + (self.receiverY - self.imagePoints[-1][1]) ** 2

    power = coefficients ** 2 / dn_carre

    return power"""

"""def getPowerCoef(self):  # en fait pas vraiment power mais |E|**2
    coefficients = 1
    # coefficients de reflexion:
    e = len(self.imagePoints)
    for i in range(e):
        wall = self.walls[i]
        dx = self.Ppoints[i][0] - self.imagePoints[i][0]
        dy = self.Ppoints[i][1] - self.imagePoints[i][1]
        d = math.sqrt(dx ** 2 + dy ** 2)

        cosOi = (dx * wall.nX + dy * wall.nY) / d
        sinOi = (dx * wall.nY - dy * wall.nX) / d
        cosOt = math.sqrt(1 - sinOi ** 2 / wall.relativePermitivity)
        if wall.mat == 1:
            gammaPerp = (self.Z2concrete * cosOi - self.Z1 * cosOt) / (self.Z2concrete * cosOi + self.Z1 * cosOt)
            u = cmath.exp(complex(-self.alphaMconcrete,
                                  (
                                      self.facEpsconcrete) * sinOi ** 2 * self.beta - self.betaMconcrete) / cosOt)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
            gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
            coefficients *= abs(gammaM)
        elif wall.mat == 0:
            gammaPerp = (self.Z2brick * cosOi - self.Z1 * cosOt) / (self.Z2brick * cosOi + self.Z1 * cosOt)
            u = cmath.exp(complex(-self.alphaMbrick,
                                  (self.facEpsbrick) * sinOi ** 2 * self.beta - self.betaMbrick) / cosOt)
            gammaM = gammaPerp * (1 - u) / (1 - gammaPerp ** 2 * u)
            coefficients *= abs(gammaM)

    if not self.imagePoints:
        dn_carre = (self.receiverX - self.originX) ** 2 + (self.receiverY - self.originY) ** 2
    else:
        dn_carre = (self.receiverX - self.imagePoints[-1][0]) ** 2 + (self.receiverY - self.imagePoints[-1][1]) ** 2

    power = coefficients ** 2 / dn_carre

    return power"""

import Map


def displayDPM(MAPstyle, results):
    """
        plt.plot(x, y, label="quadratique")
        plt.plot(x, x ** 3, label="cubique")
        plt.legend()
        #plt.savefig("figure.png")
        """
    a = 200
    b = 110
    x = np.linspace(-5, a + 1 + 5, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 1 + 5, b + 10)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(19, 9))

    # Z = np.random.randint(40, 320, (b+10, a+10))  # il y a plus q'a mettre un tableau de données pour z et c'est plié

    for i in range(len(results)):
        for j in range(len(results[0])):
            if results[i][j] == 0:
                results[i][j] = 1e-12
    Z = 10 * np.log10(1000*results)
    plt.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
    plt.colorbar()

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            plt.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            plt.plot(x1, y1, c="gray", lw=3)


    plt.title("Puissance en [dBm]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()


def displayDebit(MAPstyle, results):
    """
            plt.plot(x, y, label="quadratique")
            plt.plot(x, x ** 3, label="cubique")
            plt.legend()
            #plt.savefig("figure.png")
            """
    for i in range(len(results)):
        for j in range(len(results[0])):
            dbm = -90
            if results[i][j] != 0:
                dbm = 10 * np.log10(results[i][j]*1000)
            if dbm < -82:
                results[i][j] = 0
            elif dbm > -73:
                results[i][j] = 320
            else:
                results[i][j] = 280/9*dbm+23320/9




    a = 200
    b = 110
    x = np.linspace(-5, a + 1 + 5, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 1 + 5, b + 10)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(19, 9))

    # Z = np.random.randint(40, 320, (b+10, a+10))  # il y a plus q'a mettre un tableau de données pour z et c'est plié
    Z = results
    plt.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
    plt.colorbar()

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            plt.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            plt.plot(x1, y1, c="gray", lw=3)

    plt.title("Débit binaire en [Mb/s]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()