import matplotlib.pyplot as plt
import numpy as np
import random
import Map


def display():
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
    Z = X * np.cos(Y / 5)
    plt.pcolor(X, Y, Z, cmap=plt.cm.gnuplot)
    plt.colorbar()

    for i in Map.getWalls(2):                               # affichage des murs
        x1 = [i.getOriginX(), i.getOriginX() + i.xDirection]
        y1 = [i.getOriginY(), i.getOriginY() + i.yDirection]
        if i.mat == 0:
            plt.plot(x1, y1, c="red", lw=3)
        elif i.mat == 1:
            plt.plot(x1, y1, c="gray", lw=3)

    plt.scatter(100, 45, c="black")                         #point émetteur initial

    plt.title("figure 1")
    plt.xlabel("axe x")
    plt.ylabel("axe y")

    plt.show()
