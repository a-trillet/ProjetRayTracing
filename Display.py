import copy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import CheckButtons
import Map
from main import xMAP, yMAP, nbReflexion
somme = np.zeros((yMAP + 10, xMAP + 10))
displayAntenna = []
listAntenna = [0]

"""Affiche les résultat antenne par antenne
La fonction displayDBM affiche la puissance en dBm 
tandis que displayDebit affiche le débit"""

def displayRays(MAPstyle, rays, antennaTx, antennaRx):
    result = copy.deepcopy(somme)

    x = np.linspace(-4.5, xMAP + 4.5, xMAP + 10)  # initialisation des axes et points
    y = np.linspace(-4.5, yMAP + 4.5, yMAP + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe = fig.add_subplot()
    plt.title("Rays for validation")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    Z = result
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
    fig.colorbar(ax)

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)

    for ray in rays:  # affichage des murs
        if len(ray.Ppoints) == 0:
            x1 = [ray.originX, ray.receiverX]
            y1 = [ray.originY, ray.receiverY]
            graphe.plot(x1, y1, c="gray", lw=2)

        elif len(ray.Ppoints) == 1:
            x1 = [ray.originX, ray.Ppoints[0][0]]
            y1 = [ray.originY, ray.Ppoints[0][1]]
            graphe.plot(x1, y1, c="gray", lw=2)
            x1 = [ray.Ppoints[0][0], ray.receiverX]
            y1 = [ray.Ppoints[0][1], ray.receiverX]
            graphe.plot(x1, y1, c="gray", lw=2)
        elif len(ray.Ppoints) == 2:
            x1 = [ray.originX, ray.Ppoints[0][0]]
            y1 = [ray.originY, ray.Ppoints[0][1]]
            graphe.plot(x1, y1, c="gray", lw=2)
            x1 = [ray.Ppoints[0][0], ray.Ppoints[1][0]]
            y1 = [ray.Ppoints[0][1], ray.Ppoints[1][1]]
            graphe.plot(x1, y1, c="gray", lw=2)
            x1 = [ray.Ppoints[1][0], ray.receiverX]
            y1 = [ray.Ppoints[1][1], ray.receiverX]
            graphe.plot(x1, y1, c="gray", lw=2)

    graphe.scatter(antennaTx[0], antennaTx[1], c='b')
    graphe.scatter(antennaRx[0][0], antennaRx[0][1], c='b')
    graphe.scatter(antennaRx[1][0], antennaRx[1][1], c='b')

    plt.show()


def displayDPM(MAPstyle, results, dicoAntenna):
    somme = np.zeros((yMAP + 10, xMAP + 10))
    displayAntenna = []
    listAntenna = [0]

    def getDico():
        return dicoAntenna

    for antenna in listAntenna:
        somme += results[antenna]
        displayAntenna.append(dicoAntenna[0])
    result = copy.deepcopy(somme)

    for i in range(len(result)):
        for j in range(len(result[0])):
            if result[i][j] < 10 ** (-14):
                result[i][j] = 10 ** (-14)
            if result[i][j] > 10 ** (-6):
                result[i][j] = 10 ** (-6)

    x = np.linspace(-4.5, xMAP + 4.5, xMAP + 10)  # initialisation des axes et points
    y = np.linspace(-4.5, yMAP + 4.5, yMAP + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe = fig.add_subplot()
    plt.title("Puissance en  [dBm]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    Z = 10 * np.log10(1000 * result)
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
    fig.colorbar(ax)

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)
    for antenna in displayAntenna:
        graphe.scatter(antenna[0], antenna[1], c='b')

    # Make checkbuttons with all plotted lines with correct visibility
    # checkbuton widget
    labels = []
    activated = [True]
    for i in range(len(dicoAntenna)):
        labels.append("Antenne " + str(i) + " : " + str(dicoAntenna[i]))
        if i != 0:
            activated.append(False)
    axCheckButton = plt.axes([0.83, 0, 0.15, 0.95])
    chxbox = CheckButtons(axCheckButton, labels, activated)
    for r in chxbox.rectangles:
        r.set_width(0.05)
    [ll.set_markeredgewidth(0.5) for l in chxbox.lines for ll in l]

    def set_visible(label):
        index = int(label.split(" ")[1])
        somme = np.zeros((yMAP + 10, xMAP + 10))
        if index not in listAntenna:
            listAntenna.append(index)
            displayAntenna.append(getDico()[index])
        else:
            listAntenna.remove(index)
            displayAntenna.remove(getDico()[index])
        if listAntenna:
            for antenna in listAntenna:
                somme += results[antenna]
        result = somme
        for i in range(len(result)):
            for j in range(len(result[0])):
                if result[i][j] < 10 ** (-14):
                    result[i][j] = 10 ** (-14)
                if result[i][j] > 10 ** (-6):
                    result[i][j] = 10 ** (-6)
        Z = 10 * np.log10(1000 * somme)
        graphe.clear()
        graphe.set_title("Puissance en  [dBm]")
        graphe.set_xlabel("axe x")
        graphe.set_ylabel("axe y")
        graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
        # fig.colorbar(ax)
        for i in Map.getWalls(MAPstyle):  # affichage des murs
            x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
            y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
            if i.mat == 0:
                graphe.plot(x1, y1, c="red", lw=3)
            elif i.mat == 1:
                graphe.plot(x1, y1, c="gray", lw=3)
        for antenna in displayAntenna:
            graphe.scatter(antenna[0], antenna[1], c='b')
        plt.draw()

    chxbox.on_clicked(set_visible)
    plt.show()


def displayDebit(MAPstyle, results, dicoAntenna):
    somme = np.zeros((yMAP + 10, xMAP + 10))
    displayAntenna = []
    listAntenna = [0]

    def getDico():
        return dicoAntenna
    for antenna in listAntenna:
        somme += results[antenna]
        displayAntenna.append(dicoAntenna[0])
    result = copy.deepcopy(somme)
    for i in range(len(result)):
        for j in range(len(result[0])):
            dbm = -90
            if result[i][j] != 0:
                dbm = 10 * np.log10(result[i][j] * 1000)
            if dbm < -82:
                result[i][j] = 0
            elif dbm > -73:
                result[i][j] = 320
            else:
                result[i][j] = 280 / 9 * dbm + 23320 / 9

    x = np.linspace(-4.5, xMAP + 3.5, xMAP + 10)  # initialisation des axes et points
    y = np.linspace(-4.5, yMAP + 3.5, yMAP + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe = fig.add_subplot()
    plt.title("Débit binaire en [Mb/s]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    Z = result
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
    fig.colorbar(ax)
    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)
    for antenna in displayAntenna:
        graphe.scatter(antenna[0], antenna[1], c='b')

    # Make checkbuttons with all plotted lines with correct visibility
    # checkbuton widget
    labels = []
    activated = [True]
    for i in range(len(dicoAntenna)):
        labels.append("Antenne " + str(i) + " : " + str(dicoAntenna[i]))
        if i != 0:
            activated.append(False)
    axCheckButton = plt.axes([0.83, 0.05, 0.15, 0.9])
    chxbox = CheckButtons(axCheckButton, labels, activated)
    for r in chxbox.rectangles:
        r.set_width(0.05)
    [ll.set_markeredgewidth(0.5) for l in chxbox.lines for ll in l]

    def set_visible(label):
        index = labels.index(label)
        somme = np.zeros((yMAP + 10, xMAP + 10))
        if index not in listAntenna:
            listAntenna.append(index)
            displayAntenna.append(getDico()[index])
        else:
            listAntenna.remove(index)
            displayAntenna.remove(getDico()[index])
        if listAntenna:
            for antenna in listAntenna:
                somme += results[antenna]
        result = somme
        for i in range(len(result)):
            for j in range(len(result[0])):
                dbm = -90
                if result[i][j] > 0:
                    dbm = 10 * np.log10(result[i][j] * 1000)
                if dbm < -82:
                    result[i][j] = 0
                elif dbm > -73:
                    result[i][j] = 320
                else:
                    result[i][j] = 280 / 9 * dbm + 23320 / 9
        Z = somme
        graphe.clear()
        graphe.set_title("Débit binaire en [Mb/s]")
        graphe.set_xlabel("axe x")
        graphe.set_ylabel("axe y")
        graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
        for i in Map.getWalls(MAPstyle):  # affichage des murs
            x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
            y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
            if i.mat == 0:
                graphe.plot(x1, y1, c="red", lw=3)
            elif i.mat == 1:
                graphe.plot(x1, y1, c="gray", lw=3)
        for antenna in displayAntenna:
            graphe.scatter(antenna[0], antenna[1], c='b')
        plt.draw()

    chxbox.on_clicked(set_visible)
    plt.show()
