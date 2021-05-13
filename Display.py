import matplotlib.pyplot as plt
import numpy as np
import random
import Map


def displayDPM(MAPstyle, results, antennas):
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

    for antenna in antennas:
        plt.scatter(antenna[0], antenna[1], c="black")  # points émetteurs

    plt.title("Puissance en [dBm]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()


def displayDebit(MAPstyle, results, antennas):
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

    for antenna in antennas:
        plt.scatter(antenna[0], antenna[1], c="black")  # points émetteurs

    plt.title("Débit binaire en [Mb/s]")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()


def display(map_style, rays):
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
    Z = X * np.cos(Y / 5) * 0
    Z[60+5][60+5] = 200
    plt.pcolor(X, Y, Z, cmap=plt.cm.turbo)
    plt.colorbar()

    for i in Map.getWalls(map_style):  # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            plt.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            plt.plot(x1, y1, c="gray", lw=3)

    plt.scatter(100, 45, c="black")  # point émetteur initial

    plt.scatter(0, 0, c="black")
    plt.scatter(0, 5, c="black")
    for ray in rays:
        """try:
                    x1 = [ray.Ppoints[0], ray.receiverX]
                    y1 = [ray.Ppoints[1], ray.receiverY]
                    x2 = [ray.originX, ray.Ppoints[0]]
                    y2 = [ray.originY, ray.Ppoints[1]]
                except:
                    x1 = [ray.originX, ray.receiverX]
                    y1 = [ray.originY, ray.receiverY]
                    x2 = [0, 0]
                    y2 = [0, 0]"""
        if len(ray.walls) == 0:
            plt.scatter(ray.receiverX, ray.receiverY, c="red")
        """if ray.Ppoints:
            for p in range(len(ray.Ppoints)):
                plt.scatter(ray.Ppoints[p][0], ray.Ppoints[p][1], c='blue')
        if ray.Ppoints6:
            plt.scatter(ray.Ppoints6[0][0], ray.Ppoints6[0][1], c='red')
        if ray.Ppoints5:
            plt.scatter(ray.Ppoints5[0][0], ray.Ppoints5[0][1], c='green')
        if ray.Ppoints4:
            plt.scatter(ray.Ppoints4[0][0], ray.Ppoints4[0][1], c='yellow')"""



        # plt.plot(x1, y1, ls="--")
        # plt.plot(x2, y2, ls="--")

    plt.title("figure 1")
    plt.xlabel("axe x")
    plt.ylabel("axe y")
    plt.show()
