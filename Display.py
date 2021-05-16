import copy

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib.figure import Figure
from matplotlib.widgets import CheckButtons

import Map

somme = np.zeros((120, 210))
displayAntenna = []
listAntenna = [0]



def displayDPM(MAPstyle, results,dicoAntenna):
    somme = np.zeros((120, 210))
    displayAntenna = []
    listAntenna = [0]

    def getDico():
        return dicoAntenna

    for antenna in listAntenna:
        somme += results[antenna]
        displayAntenna.append(dicoAntenna[0])
    result = copy.deepcopy(somme)
    a = 200
    b = 110
    x = np.linspace(-5, a + 4, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 4, b + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe = fig.add_subplot()
    plt.title("Puissance en  [dBm]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")

    for i in range(len(result)):
        for j in range(len(result[0])):
            if result[i][j] < 10**(-14):
                result[i][j] = 10 ** (-14)
            if result[i][j] > 10 ** (-6):
                result[i][j] = 10 ** (-6)

    Z = 10 * np.log10(1000*result)
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
            labels.append("Antenne " + str(i) + ": " + str(dicoAntenna[i]))
            if i != 0:
                activated.append(False)
        axCheckButton = plt.axes([0.83, 0.2, 0.15, 0.7])
        chxbox = CheckButtons(axCheckButton, labels, activated)

        def set_visible(label):
            index = labels.index(label)
            somme = np.zeros((120, 210))
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
            Z = 10 * np.log10(1000 * result)
            graphe.clear()
            graphe.set_title("Puissance en  [dBm]")
            graphe.set_xlabel("axe x")
            graphe.set_ylabel("axe y")
            graphe.pcolor(X, Y, Z, cmap=plt.cm.turbo, shading='nearest')
            #fig.colorbar(ax)
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
    somme = np.zeros((120, 210))
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
                dbm = 10 * np.log10(result[i][j]*1000)
            if dbm < -82:
                result[i][j] = 0
            elif dbm > -73:
                result[i][j] = 320
            else:
                result[i][j] = 280/9*dbm+23320/9
    a = 200
    b = 110
    x = np.linspace(-5, a + 4, a + 10)  # initialisation des axes et points
    y = np.linspace(-5, b + 4, b + 10)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(19, 9))
    graphe= fig.add_subplot()
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
        labels.append("Antenne "+str(i)+ ": " +str(dicoAntenna[i]))
        if i != 0:
            activated .append(False)
    axCheckButton = plt.axes([0.83, 0.2, 0.15, 0.7])
    chxbox = CheckButtons(axCheckButton, labels, activated)

    def set_visible(label):
        index = labels.index(label)
        somme = np.zeros((120, 210))
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
        #plt.colorbar()
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