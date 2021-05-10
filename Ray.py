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
        res = False
        for i in range(2):
            try:
                RX = [self.receiverX, self.receiverY]
                x0 = [self.walls[i].origin[0], self.walls[i].origin[1]]
                n = [self.walls[i].nX, self.walls[i].nY]
                u = [self.walls[i].uX, self.walls[i].uY]
                if i == 0:
                    TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                    TX = [self.originX, self.originY]
                    d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]

                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i].length:
                        P1 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                        self.Ppoints.extend(P1)
                        res = True
                elif i == 1:
                    try:
                        TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                        TX = [self.imagePoints[i - 1][0], self.imagePoints[i - 1][1]]
                        d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                        s = [TX[0] - x0[0], TX[1] - x0[1]]
                        t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                        PSsn = s[0] * n[0] + s[1] * n[1]
                        PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                        print("avant")
                        if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i].length:
                            print("après")
                            P3 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                            RX = P3
                            TXp = [self.imagePoints[i - 1][0], self.imagePoints[i - 1][1]]  # point TX'
                            TX = [self.originX, self.originY]
                            x0 = [self.walls[i - 1].origin[0], self.walls[i - 1].origin[1]]
                            n = [self.walls[i - 1].nX, self.walls[i - 1].nY]
                            u = [self.walls[i - 1].uX, self.walls[i - 1].uY]
                            d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                            s = [TX[0] - x0[0], TX[1] - x0[1]]
                            t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                            PSsn = s[0] * n[0] + s[1] * n[1]
                            PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                            if np.sign(PSsn) == np.sign(PSRXn):
                                if 0 <= t <= self.walls[i - 1].length:
                                    P2 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                                    self.Ppoints3.extend(P2)
                                    self.Ppoints2.extend(P3)
                                    res = True
                    except:
                        dhj = 5
            except:
                print("pas de point image")

        print("P1 : ", self.Ppoints, "rayon : ", self)
        print("P3 : ", self.Ppoints2)
        print("P2 : ", self.Ppoints3)
        return res
