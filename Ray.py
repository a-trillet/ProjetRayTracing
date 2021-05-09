from Wall import *
import numpy as np


class Ray:
    def __init__(self, originX, originY, receiverX, receiverY):
        self.originX = originX
        self.originY = originY
        self.receiverX = receiverX
        self.receiverY = receiverY
        self.imagePoints = []
        self.walls = []
        self.reflexionPoints = []
        self.Ppoints = []
        self.Ppoints2 = []
        self.Ppoints3 = []

    def find_Points(self):

        for i in range(1):
            if i == 0:
                try:
                    RX = [self.receiverX, self.receiverY]
                    TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                    TX = [self.originX, self.originY]
                    d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                    x0 = [self.walls[i].origin[0], self.walls[i].origin[1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    n = [self.walls[i].nX, self.walls[i].nY]
                    u = [self.walls[i].uX, self.walls[i].uY]

                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn):
                        if 0 <= t <= self.walls[i].length:
                            P = [x0[0] + t * u[0], x0[1] + t * u[1]]
                            self.Ppoints.extend(P)
                except:
                    print("pas de point image")
            else:
                RX = [self.imagePoints[i + 1][0], self.imagePoints[i + 1][1]]
                TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                TX = 0
        print(self.Ppoints)
