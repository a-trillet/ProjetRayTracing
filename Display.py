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


def heatmapDisplay(MAPstyle, antenna, result, title):

    x = np.linspace(-4.5, xMAP + 4.5, xMAP + 10)  # initialisation des axes et points
    y = np.linspace(-4.5, yMAP + 4.5, yMAP + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe = fig.add_subplot()
    plt.title(title)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")

    ax = graphe.pcolor(X, Y, result, cmap=plt.cm.turbo, shading='nearest')
    fig.colorbar(ax)

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="gray", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)
    graphe.scatter(antenna[0], antenna[1], c='white', lw=3)
    plt.show()


def displayRays(MAPstyle, rays, antennaTx, antennaRx, result, title):

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
    plt.title(title)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    Z = 10 * np.log10(1000 * result)
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
    fig.colorbar(ax)

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="gray", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)

    for ray in rays:
        if len(ray.Ppoints) == 0:  # it is a LOS ray
            x1 = [ray.originX, ray.receiverX]
            y1 = [ray.originY, ray.receiverY]
            graphe.plot(x1, y1, c="yellow", lw=2)

        elif len(ray.Ppoints) == 1:
            if len(ray.imagePoints) == 0:  # it is a diffracted ray
                x1 = [ray.originX, ray.Ppoints[0][0]]
                y1 = [ray.originY, ray.Ppoints[0][1]]
                graphe.plot(x1, y1, c="white", lw=2)
                x1 = [ray.Ppoints[0][0], ray.receiverX]
                y1 = [ray.Ppoints[0][1], ray.receiverY]
                graphe.plot(x1, y1, c="white", lw=2)
            if len(ray.imagePoints) == 1:  # it is a reflected ray
                x1 = [ray.originX, ray.Ppoints[0][0]]
                y1 = [ray.originY, ray.Ppoints[0][1]]
                graphe.plot(x1, y1, c="blue", lw=2)
                x1 = [ray.Ppoints[0][0], ray.receiverX]
                y1 = [ray.Ppoints[0][1], ray.receiverY]
                graphe.plot(x1, y1, c="blue", lw=2)
        elif len(ray.Ppoints) == 2:   # it is a 2 times reflected ray
            x1 = [ray.originX, ray.Ppoints[0][0]]
            y1 = [ray.originY, ray.Ppoints[0][1]]
            graphe.plot(x1, y1, c="blue", lw=2)
            x1 = [ray.Ppoints[0][0], ray.Ppoints[1][0]]
            y1 = [ray.Ppoints[0][1], ray.Ppoints[1][1]]
            graphe.plot(x1, y1, c="blue", lw=2)
            x1 = [ray.Ppoints[1][0], ray.receiverX]
            y1 = [ray.Ppoints[1][1], ray.receiverY]
            graphe.plot(x1, y1, c="blue", lw=2)
    for i in range(len(antennaTx)):
        graphe.scatter(antennaTx[i][0], antennaTx[i][1], c='white', lw=3)
    for i in range(len(antennaRx)):
        graphe.scatter(antennaRx[i][0], antennaRx[i][1], c='white', lw = 3)

    plt.show()


def displayDPM(MAPstyle, results, dicoAntenna):
    somme = np.zeros((yMAP + 10, xMAP + 10))
    displayAntenna = []
    listAntenna = [0]

    def getDico():
        return dicoAntenna

    for antenna in listAntenna:
        for i in range(xMAP):
            for j in range(yMAP):
                if somme[i][j] < results[antenna][i][j]:
                    somme[i][j] = results[antenna][i][j]
        #somme += results[antenna]
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
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    Z = 10 * np.log10(1000 * result)
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
    fig.colorbar(ax)

    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="gray", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)
    for antenna in displayAntenna:
        graphe.scatter(antenna[0], antenna[1], c='white')

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
                for i in range(xMAP):
                    for j in range(yMAP):
                        if somme[i][j] < results[antenna][i][j]:
                            somme[i][j] = results[antenna][i][j]
                #somme += results[antenna]
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
        graphe.set_xlabel("x [m]")
        graphe.set_ylabel("y [m]")
        graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
        # fig.colorbar(ax)
        for i in Map.getWalls(MAPstyle):  # affichage des murs
            x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
            y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
            if i.mat == 0:
                graphe.plot(x1, y1, c="gray", lw=3)
            elif i.mat == 1:
                graphe.plot(x1, y1, c="gray", lw=3)
        for antenna in displayAntenna:
            graphe.scatter(antenna[0], antenna[1], c='white')
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
        for i in range(xMAP):
            for j in range(yMAP):
                if somme[i][j] < results[antenna][i][j]:
                    somme[i][j] = results[antenna][i][j]
        #somme += results[antenna]
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
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    Z = result
    ax = graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
    fig.colorbar(ax)
    for i in Map.getWalls(MAPstyle):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            graphe.plot(x1, y1, c="gray", lw=3)
        elif i.mat == 1:
            graphe.plot(x1, y1, c="gray", lw=3)
    for antenna in displayAntenna:
        graphe.scatter(antenna[0], antenna[1], c='white')

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
                for i in range(xMAP):
                    for j in range(yMAP):
                        if somme[i][j] < results[antenna][i][j]:
                            somme[i][j] = results[antenna][i][j]
                #somme += results[antenna]
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
        graphe.set_xlabel("x [m]")
        graphe.set_ylabel("y [m]")
        graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='auto')
        for i in Map.getWalls(MAPstyle):  # affichage des murs
            x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
            y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
            if i.mat == 0:
                graphe.plot(x1, y1, c="gray", lw=3)
            elif i.mat == 1:
                graphe.plot(x1, y1, c="gray", lw=3)
        for antenna in displayAntenna:
            graphe.scatter(antenna[0], antenna[1], c='white')
        plt.draw()

    chxbox.on_clicked(set_visible)
    plt.show()
