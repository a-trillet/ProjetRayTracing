import copy
import numpy as np

"""Implémentation de la méthode des images(fonction getRayImage) ainsi que le 
calcul du ou des point d'intersection entre le mur et le rayon (fonction findPoint)
Note: Un rayon n'es créé que si il est valable"""

def getRayImage(originX, originY, wallsh, wallsv, oldRay):
    rays = [oldRay]
    walls = [wallsv, wallsh]
    for e in range(3):
        for n in range(2):
            for wall in walls[n]:
                PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                if PsSN != 0:
                    imagePoints = [[originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY]]
                    if e == 0:
                        P1 = find_Point([wall], e, oldRay.receiverX, oldRay.receiverY, originX, originY, imagePoints)
                        if P1 is not None:
                            ray = copy.deepcopy(oldRay)
                            ray.walls.append(wall)
                            ray.imagePoints.extend(imagePoints)
                            ray.Ppoints.append(P1)
                            rays.append(ray)
                    elif e == 1 or e == 2:
                        for j in range(2):
                            for w in walls[j]:
                                if w != wall:
                                    if j == 0:
                                        PsSN2 = imagePoints[0][0] - w.getOriginX()
                                    else:
                                        PsSN2 = imagePoints[0][1] - w.getOriginY()
                                    if PsSN2 != 0:
                                        if j == 0:
                                            imagePoints.append([imagePoints[0][0] - 2 * PsSN2, imagePoints[0][1]])
                                        else:
                                            imagePoints.append(
                                                [imagePoints[0][0], imagePoints[0][1] - 2 * PsSN2])
                                        if e == 1:
                                            P2, P3 = find_Point([wall, w], e, oldRay.receiverX, oldRay.receiverY,
                                                                originX,
                                                                originY, imagePoints)
                                            if P2 is not None:
                                                ray = copy.deepcopy(oldRay)
                                                ray.walls.extend([wall, w])
                                                ray.imagePoints.extend(imagePoints)
                                                ray.Ppoints.extend([P2, P3])
                                                rays.append(ray)
                                        else:
                                            for jj in range(2):
                                                for m in walls[jj]:
                                                    if m != w:
                                                        if jj == 0:
                                                            PsSN3 = (imagePoints[1][0] - m.getOriginX())
                                                        else:
                                                            PsSN3 = (imagePoints[1][1] - m.getOriginY())
                                                        if PsSN3 != 0:
                                                            if jj == 0:
                                                                imagePoints.append([imagePoints[1][0] - 2 * PsSN3,
                                                                                     imagePoints[1][1]])
                                                            else:
                                                                imagePoints.append(
                                                                    [imagePoints[1][0],
                                                                     imagePoints[1][1] - 2 * PsSN3])
                                                            P4, P5, P6 = find_Point([wall, w, m], e, oldRay.receiverX,
                                                                                    oldRay.receiverY, originX,
                                                                                    originY, imagePoints)
                                                            if P4 is not None:
                                                                ray = copy.deepcopy(oldRay)
                                                                ray.walls.extend([wall, w, m])
                                                                ray.imagePoints.extend(imagePoints)
                                                                ray.Ppoints.extend([P4, P5, P6])
                                                                rays.append(ray)
                                                            imagePoints.remove(imagePoints[2])
                                        imagePoints.remove(imagePoints[1])
    for r in rays:
        print(r.Ppoints)
    return rays


def find_Point(walls, i, receiverX, receiverY, originX, originY, imagePoints):
    if True:
        if walls:
            RX = [receiverX, receiverY]
            x0 = [walls[i].origin[0], walls[i].origin[1]]
            n = [walls[i].nX, walls[i].nY]
            u = [walls[i].uX, walls[i].uY]
            if i == 0 and len(imagePoints) == 1:
                TXp = [imagePoints[i][0], imagePoints[i][1]]  # point TX'

                d = [RX[0] - TXp[0], RX[1] - TXp[1]]

                dnt = u[0] * d[1] - u[1] * d[0]
                if dnt != 0:
                    TX = [originX, originY]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i].length:
                        P1 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                        return P1
                    else:
                        return None
                else:
                    return None
            elif i == 1 and len(imagePoints) == 2:
                TXp = [imagePoints[i][0], imagePoints[i][1]]  # point TX'
                d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                dnt = (u[0] * d[1] - u[1] * d[0])
                if dnt != 0:
                    TX = [imagePoints[i - 1][0], imagePoints[i - 1][1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i].length:
                        P3 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                        RX = P3
                        TXp = [imagePoints[i - 1][0], imagePoints[i - 1][1]]  # point TX'
                        u = [walls[i - 1].uX, walls[i - 1].uY]

                        d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                        dnt = (u[0] * d[1] - u[1] * d[0])
                        if dnt != 0:
                            TX = [originX, originY]
                            x0 = [walls[i - 1].origin[0], walls[i - 1].origin[1]]
                            n = [walls[i - 1].nX, walls[i - 1].nY]
                            s = [TX[0] - x0[0], TX[1] - x0[1]]
                            t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt
                            PSsn = s[0] * n[0] + s[1] * n[1]
                            PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                            if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i - 1].length:
                                P2 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                                return P2, P3
                            else:
                                return None, None
                        else:
                            return None, None
                    else:
                        return None, None
                else:
                    return None, None
            elif i == 2 and len(imagePoints) == 3:
                TXp = [imagePoints[i][0], imagePoints[i][1]]  # point TX'
                d = [RX[0] - TXp[0], RX[1] - TXp[1]]
                dnt = u[0] * d[1] - u[1] * d[0]

                if dnt != 0:
                    TX = [imagePoints[i - 1][0], imagePoints[i - 1][1]]
                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt

                    PSsn = s[0] * n[0] + s[1] * n[1]
                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                    if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i].length:
                        P6 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                        RX = P6
                        TXp = [imagePoints[i - 1][0], imagePoints[i - 1][1]]  # point TX'
                        u = [walls[i - 1].uX, walls[i - 1].uY]
                        d = [RX[0] - TXp[0], RX[1] - TXp[1]]

                        dnt = u[0] * d[1] - u[1] * d[0]
                        if dnt != 0:
                            TX = [imagePoints[i - 2][0], imagePoints[i - 2][1]]
                            x0 = [walls[i - 1].origin[0], walls[i - 1].origin[1]]
                            n = [walls[i - 1].nX, walls[i - 1].nY]
                            s = [TX[0] - x0[0], TX[1] - x0[1]]
                            t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt

                            PSsn = s[0] * n[0] + s[1] * n[1]
                            PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                            if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i - 1].length:
                                P5 = [x0[0] + t * u[0], x0[1] + t * u[1]]

                                RX = P5
                                TXp = [imagePoints[i - 2][0], imagePoints[i - 2][1]]  # point TX'
                                u = [walls[i - 2].uX, walls[i - 2].uY]
                                d = [RX[0] - TXp[0], RX[1] - TXp[1]]

                                dnt = u[0] * d[1] - u[1] * d[0]
                                if dnt != 0:
                                    TX = [originX, originY]
                                    x0 = [walls[i - 2].origin[0], walls[i - 2].origin[1]]
                                    n = [walls[i - 2].nX, walls[i - 2].nY]
                                    s = [TX[0] - x0[0], TX[1] - x0[1]]
                                    t = (d[1] * (TXp[0] - x0[0]) - d[0] * (TXp[1] - x0[1])) / dnt

                                    PSsn = s[0] * n[0] + s[1] * n[1]
                                    PSRXn = (RX[0] - x0[0]) * n[0] + (RX[1] - x0[1]) * n[1]
                                    if np.sign(PSsn) == np.sign(PSRXn) and 0 < t < walls[i - 2].length:
                                        P4 = [x0[0] + t * u[0], x0[1] + t * u[1]]
                                        return P4, P5, P6
                                    else:
                                        return None, None, None
                                else:
                                    return None, None, None
                            else:
                                return None, None, None
                        else:
                            return None, None, None
                    else:
                        return None, None, None
                else:
                    return None, None, None
