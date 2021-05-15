import matplotlib.pyplot as plt
import numpy as np
import random
import Map


def displayDPM(MAPstyle, results):
    a = 200
    b = 110
    x = np.linspace(-5, a + 4, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 4, b + 10)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(20, 10))

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
    x = np.linspace(-5, a + 4, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 4, b + 10)
    X, Y = np.meshgrid(x, y)
    plt.figure(figsize=(19, 9))
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

