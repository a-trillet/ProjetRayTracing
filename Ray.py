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

    alphaMconcrete = omega * math.sqrt(mu0 * eps0 * 5) * math.sqrt(math.sqrt(1 + (0.014 / (omega * 5 * eps0)) ** 2) - 1)
    alphaMbrick = omega * math.sqrt(mu0 * eps0 * 4.6) * math.sqrt(math.sqrt(1 + (0.02 / (omega * 4.6 * eps0)) ** 2) - 1)
    betaMconcrete = omega * math.sqrt(mu0 * eps0 * 5) * math.sqrt(math.sqrt(1 + (0.014 / (omega * 5 * eps0)) ** 2) + 1)
    betaMbrick = omega * math.sqrt(mu0 * eps0 * 4.6) * math.sqrt(math.sqrt(1 + (0.02 / (omega * 4.6 * eps0)) ** 2) + 1)

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
        if len(self.imagePoints) != 0:
            dx = self.receiverX - self.imagePoints[-1][0]
            dy = self.receiverY - self.imagePoints[-1][1]
            d = math.sqrt(dx ** 2 + dy ** 2)
            a=1
        else:
            dx = self.receiverX - self.originX
            dy = self.receiverY - self.originY
            d = math.sqrt(dx ** 2 + dy ** 2)
        facEpsbrick = 0.4662524041201569
        facEpsconcrete = 0.4472135954999579
        Tcoef_carre = 1
        alphaMconcrete = 1.6678554713954776
        alphaMbrick = 2.484083522793021
        beta = 565.878155926954
        betaMconcrete = 1789.4646281205935
        betaMbrick = 1716.395226729443
        Z1 = 376.73031346177066
        Z2concrete = (168.47869848039613 + 0.15702915534584408j)
        Z2brick = (175.6508624825743 + 0.2542138351688341j)
        for i in range(len(self.Ppoints) + 1):
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
                if Py1 < wall.origin[1] < Py2 or Py1 > wall.origin[1] > Py2:
                    found = 1
                    proj = (wall.origin[1] - Py2) * sinOi / cosOi
                    if wall.origin[0] <= Px2 - proj <= wall.origin[0] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOtC) / (Z2concrete * abs(cosOi) + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,
                                                      (
                                                          facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtC)) / (
                                            1 - gammaPerp ** 2 * u))
                                Tcoef_carre *= TmC ** 2
                        elif wall.mat == 0:
                            if TmB == 0:
                                gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOtB) / (Z2brick * abs(cosOi) + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                      (
                                                          facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtB)) / (
                                            1 - gammaPerp ** 2 * u))
                                Tcoef_carre *= TmB ** 2
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
                if Px1 < wall.origin[0] < Px2 or Px1 > wall.origin[0] > Px2:
                    found = 1
                    proj = (Px2 - wall.origin[0]) * sinOi / cosOi
                    if wall.origin[0] <= Px2 - proj <= wall.origin[0] + wall.length:
                        if wall.mat == 1:
                            if TmC == 0:
                                gammaPerp = (Z2concrete * abs(cosOi) - Z1 * cosOtC) / (Z2concrete * abs(cosOi) + Z1 * cosOtC)
                                u = cmath.exp(complex(-alphaMconcrete,(facEpsconcrete) * sinOi ** 2 * beta - betaMconcrete) / cosOtC)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmC = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtC)) / (1 - gammaPerp ** 2 * u))
                                Tcoef_carre *= TmC ** 2
                        elif wall.mat == 0:
                            if TmB == 0:
                                gammaPerp = (Z2brick * abs(cosOi) - Z1 * cosOtB) / (Z2brick * abs(cosOi) + Z1 * cosOtB)
                                u = cmath.exp(complex(-alphaMbrick,
                                                      (
                                                          facEpsbrick) * sinOi ** 2 * beta - betaMbrick) / cosOtB)  # ATTENTION ici pas de thickness car 2*thickness(=0.5) =1
                                TmB = abs((1 - gammaPerp ** 2) * cmath.exp(complex(0, -betaMconcrete / 2 / cosOtB)) / (
                                        1 - gammaPerp ** 2 * u))
                                Tcoef_carre *= TmB ** 2
                elif found == 1:
                    break

        return Tcoef_carre  # NOTE: carré ou pas à voir
