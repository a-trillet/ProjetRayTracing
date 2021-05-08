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

    def find_Points(self):
        for i in range(len(self.imagePoints)):
            try:
                if i+1 < len(self.imagePoints):
                    dx = self.imagePoints[i + 1][0] - self.imagePoints[i][0]
                    dy = self.imagePoints[i + 1][1] - self.imagePoints[i][1]
                    PsSN = (self.imagePoints[i][0] - self.walls[i].getOriginX()) * self.walls[i].nX + (
                                self.imagePoints[i][1] - self.walls[i].getOriginX()) * self.walls[i].nY

                    PsRN = (self.imagePoints[i + 1][0] - self.walls[i].getOriginX()) * self.walls[i].nX + (
                                self.imagePoints[i + 1][1] - self.walls[i].getOriginY()) * self.walls[i].nY

                    if np.sign(PsSN) == np.sign(PsRN):
                        w = dx * self.walls[i].nX + dy * self.walls[i].nY
                        if w != 0:
                            t = (dx * (self.walls[i].getOriginY() - self.imagePoints[i][1]) - dy * (
                                    self.walls[i].getOriginX() - self.imagePoints[i][0])) / w
                            if 0 <= t <= self.walls[i].length:
                                P = [self.walls[i].getOriginX() + t * self.walls[i].uX, self.walls[i].getOriginY() + t * self.walls[i].uY]
                                self.Ppoints.extend(P)
                                print(P)
                    else:
                        print("wooooow truc de ouf")
                elif i+1 == len(self.imagePoints):
                    dx = self.receiverX - self.imagePoints[i][0]
                    dy = self.receiverY - self.imagePoints[i][1]
                    PsSN = (self.originX - self.walls[i].getOriginX()) * self.walls[i].nX + (
                                self.originY - self.walls[i].getOriginY()) * self.walls[i].nY
                    PsRN = (self.receiverX - self.walls[i].getOriginX()) * self.walls[i].nX + (
                                self.receiverY - self.walls[i].getOriginY()) * self.walls[i].nY
                    if np.sign(PsSN) == np.sign(PsRN):
                        w = dx * self.walls[i].nX + dy * self.walls[i].nY
                        if w != 0:
                            t = (dx * (self.walls[i].getOriginY() - self.imagePoints[i][1]) - dy * (
                                    self.walls[i].getOriginX() - self.imagePoints[i][0])) / w
                            if 0 <= t <= self.walls[i].length:
                                P = [self.walls[i].getOriginX() + t * self.walls[i].uX,
                                     self.walls[i].getOriginY() + t * self.walls[i].uY]
                                self.Ppoints.extend(P)
                                print(P)
                    else:
                        print("wooooow truc de ouf")
            except:
                print("nope")
