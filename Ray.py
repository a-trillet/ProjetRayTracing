import cmath

import inline as inline
import pylab

from Wall import *
import numpy as np
import pylab
import inline

class Ray:
    def __init__(self, originX, originY, receiverX, receiverY):
        self.originX = originX
        self.originY = originY
        self.receiverX = receiverX
        self.receiverY = receiverY
        self.imagePoints = []
        self.walls = []
        self.reflexionPoints = []
        self.cosOiV = 0
        self.sinOiV = 0

        self.Ppoints = []

        self.Ppoints2 = []
        self.Ppoints3 = []

        self.Ppoints4 = []
        self.Ppoints5 = []
        self.Ppoints6 = []

    def find_Points(self):
        if self.walls:
            for i in range(len(self.walls)):
                RX = [self.receiverX, self.receiverY]
                x0 = [self.walls[i].origin[0], self.walls[i].origin[1]]
                n = [self.walls[i].nX, self.walls[i].nY]
                u = [self.walls[i].uX, self.walls[i].uY]
                if i == 0 and len(self.imagePoints) == 1:
                    TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                    TX = [self.originX, self.originY]
                    d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]

                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i].length:
                        P1 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                        self.Ppoints.append(P1)
                        return True
                    else:
                        return False

                elif i == 1 and len(self.imagePoints) == 2:
                    RX = [self.receiverX, self.receiverY]
                    TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                    TX = [self.imagePoints[i - 1][0], self.imagePoints[i - 1][1]]
                    d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i].length:
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
                        if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i - 1].length:
                            P2 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                            self.Ppoints.append(P2)
                            self.Ppoints.append(P3)
                            return True
                        else:
                            return False
                    else:
                        return False

                elif i == 2 and len(self.imagePoints) == 3:
                    RX = [self.receiverX, self.receiverY]
                    TXp = [self.imagePoints[i][0], self.imagePoints[i][1]]  # point TX'
                    TX = [self.imagePoints[i - 1][0], self.imagePoints[i - 1][1]]
                    d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i].length:
                        P6 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                        RX = P6
                        TXp = [self.imagePoints[i - 1][0], self.imagePoints[i - 1][1]]  # point TX'
                        TX = [self.imagePoints[i - 2][0], self.imagePoints[i - 2][1]]
                        x0 = [self.walls[i - 1].origin[0], self.walls[i - 1].origin[1]]
                        n = [self.walls[i - 1].nX, self.walls[i - 1].nY]
                        u = [self.walls[i - 1].uX, self.walls[i - 1].uY]
                        d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                        s = [TX[0] - x0[0], TX[1] - x0[1]]
                        t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                        PSsn = s[0] * n[0] + s[1] * n[1]
                        PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                        if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i - 1].length:
                            P5 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                            RX = P5
                            TXp = [self.imagePoints[i - 2][0], self.imagePoints[i - 2][1]]  # point TX'
                            TX = [self.originX, self.originY]
                            x0 = [self.walls[i - 2].origin[0], self.walls[i - 2].origin[1]]
                            n = [self.walls[i - 2].nX, self.walls[i - 2].nY]
                            u = [self.walls[i - 2].uX, self.walls[i - 2].uY]
                            d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                            s = [TX[0] - x0[0], TX[1] - x0[1]]
                            t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / (u[0] * d[1] - u[1] * d[0])

                            PSsn = s[0] * n[0] + s[1] * n[1]
                            PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                            if np.sign(PSsn) == np.sign(PSRXn) and 0 <= t <= self.walls[i - 2].length:
                                P4 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                                self.Ppoints6.append(P6)
                                self.Ppoints5.append(P5)
                                self.Ppoints4.append(P4)
                                """print("P4 : ", self.Ppoints4, "rayon : ", self)
                                print("P5 : ", self.Ppoints5)
                                print("P6 : ", self.Ppoints6)"""
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False

        else:
            return True

    """#constant variables :
    Z0 = 376.730313
    Ra = 73
    c = 299792458
    lam = c/(27 * 10**9)
    he = -lam/math.pi
    factor = he**2/8/Ra
    Gtx = 1.6977
    Ptx = 0.1   # [W]"""
    omega = 2 * math.pi * 27e9
    c = 299792458
    lam = c / (27 * 10 ** 9)
    beta = 2 * math.pi / lam
    mu0 = 4e-7 * math.pi
    eps0 = 1 / (mu0 * c ** 2)
    facEpsbrick = math.sqrt(1 / 4.6)
    facEpsconcrete = math.sqrt(1 / 5)
    epsCconcrete = complex(5 * eps0, -(0.014 / omega))
    epsCbrick = complex(4.6 * eps0, -(0.02 / omega))

    alphaMconcrete = omega * math.sqrt(5 * c / 2 * (math.sqrt(1 + (0.014 / omega / 5 / 8.854e-12) ** 2)-1))
    alphaMbrick = omega * math.sqrt(4.6 * c / 2 * (1 + math.sqrt(1 + (0.02 / omega / 4.6 / 8.854e-12) ** 2) -1))
    betaMconcrete = omega * math.sqrt(5 * c /2*(1+math.sqrt(1+(0.014/omega/5/8.854e-12)**2)+1))
    betaMbrick = omega * math.sqrt(4.6 * c /2*(1+math.sqrt(1+(0.02/omega/4.6/8.854e-12)**2)+1))
    Z1 = mu0 * c
    Z2concrete = cmath.sqrt(mu0 / epsCconcrete)
    Z2brick = cmath.sqrt(mu0 / epsCbrick)

    def getPowerCoef(self):  # en fait pas vraiment power mais |E|**2
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

        return power
    def getPower(self):  # en fait pas vraiment power mais |E|**2
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

        return power

    def getTcoef(self, wallsH, wallsV):
        try:
            dx = self.receiverX - self.imagePoints[-1][0]
            dy = self.receiverY - self.imagePoints[-1][1]
            d = math.sqrt(dx**2 + dy**2)
        except:
            dx = self.receiverX-self.originX
            dy = self.receiverY - self.originY
            d = math.sqrt(dx**2 + dy**2)
        facEpsbrick = 0.4662524041201569
        facEpsconcrete = 0.4472135954999579
        Tcoef_carre = 1
        alphaMconcrete = 6121864080547.301
        alphaMbrick = 4454703587257557.0
        beta = 565.878155926954
        betaMconcrete = 8044234853336171.0
        betaMbrick = 7715762171124073.0
        Z1 = 376.73031346177066
        Z2concrete = (168.47869848039613 + 0.15702915534584408j)
        Z2brick = (175.6508624825743 + 0.2542138351688341j)
        for i in range(len(self.Ppoints)+1):
            if i == 0 and len(self.Ppoints) != 0:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.Ppoints[0][0]
                Py2 = self.Ppoints[0][1]
            elif len(self.Ppoints) == 0:
                Px1 = self.originX
                Py1 = self.originY
                Px2 = self.receiverX
                Py2 = self.receiverY
            elif i == len(self.Ppoints):
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.receiverX
                Py2 = self.receiverY
            else:
                Px1 = self.Ppoints[i - 1][0]
                Py1 = self.Ppoints[i - 1][1]
                Px2 = self.Ppoints[i][0]
                Py2 = self.Ppoints[i][1]

            # Walls H
            found = 0
            TmB = 0
            TmC = 0
            cosOi = -dy / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dx / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            cosOtC = math.sqrt(1 - sinOi ** 2 / 5)
            cosOtB = math.sqrt(1 - sinOi ** 2 / 4.6)
            for wall in wallsH:  # n= (0,-1)
                if Py1 <= wall.origin[1] <= Py2 or Py1 >= wall.origin[1] >= Py2:
                    found = 1
                    proj = (wall.origin[1] - Py2) * sinOi / cosOi
                    if wall.origin[0] <= Px2 - proj <= wall.origin[0] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                gammaPerp = (Z2concrete * cosOi - Z1 * cosOtC) / (Z2concrete * cosOi + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,
                                                  (
                                                      facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1-gammaPerp**2)*cmath.exp(complex(0, -betaMconcrete/2/cosOtC)) / (1 - gammaPerp ** 2 * u))
                            Tcoef_carre * TmC**2
                        elif wall.mat == 0:
                            if TmB == 0:
                                gammaPerp = (Z2brick * cosOi - Z1 * cosOtB) / (Z2brick * cosOi + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                  (
                                                      facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1-gammaPerp**2)*cmath.exp(complex(0, -betaMconcrete/2/cosOtB)) / (1 - gammaPerp ** 2 * u))
                            Tcoef_carre * TmB**2
                elif found == 1:
                    break
            # Walls V
            found = 0
            TmB = 0
            TmC = 0
            cosOi = dx / d  # NOTE : valeurs plus ou moins calculées dans # getPower
            sinOi = dy / d  # faute expres pour simplifier, cos, sin  corrigés par la suite
            cosOtC = math.sqrt(1 - sinOi ** 2 / 5)
            cosOtB = math.sqrt(1 - sinOi ** 2 / 4.6)
            for wall in wallsV:  # n= (1,0)
                if Px1 <= wall.origin[0] <= Px2 or Px1 >= wall.origin[0] >= Px2:
                    found = 1
                    proj = (Px2 - wall.origin[0]) * sinOi / cosOi
                    if wall.origin[0] <= Px2 - proj <= wall.origin[0] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                gammaPerp = (Z2concrete * cosOi - Z1 * cosOtC) / (Z2concrete * cosOi + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,
                                                      (
                                                          facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtC)) / (
                                            1 - gammaPerp ** 2 * u))
                            Tcoef_carre * TmC ** 2
                        elif wall.mat == 0:
                            if TmB == 0:
                                gammaPerp = (Z2brick * cosOi - Z1 * cosOtB) / (Z2brick * cosOi + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                      (
                                                          facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtB)) / (
                                            1 - gammaPerp ** 2 * u))
                            Tcoef_carre * TmB ** 2
                elif found == 1:
                    break

        return Tcoef_carre  # NOTE: carré ou pas à voir
