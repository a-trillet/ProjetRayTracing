import copy
import Map
import numpy as np
# from main import walls
from Ray import Ray

wa = 0


# créer un ray de base Ray(originX, originY, receiverX, receiverY))
def getRayImages(originX, originY, walls, oldRay):
    rays = []
    e = len(oldRay.imagePoints)
    if e < 3:
        for wall in walls:
            try:
                if wall != oldRay.walls[-1]:
                    PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                    if PsSN != 0:
                        ray = copy.deepcopy(oldRay)
                        if True:
                            ray.walls.append(wall)
                            ray.imagePoints.append([originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY])
                            rays.extend(getRayImages(ray.imagePoints[e][0], ray.imagePoints[e][1], walls, ray))
                    # else:
                    # print("rayon // à un mur")
                # else:
                # print(wall.origin[0])
            # else:
            # print("chaud")
            except:
                if not oldRay.imagePoints:
                    PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                    if PsSN != 0:
                        ray = copy.deepcopy(oldRay)
                        if True:
                            ray.walls.append(wall)
                            ray.imagePoints.append([originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY])
                            rays.extend(getRayImages(ray.imagePoints[e][0], ray.imagePoints[e][1], walls, ray))
                    # else:
                    # print("rayon // à un mur")
                # else:
                # print(wall.origin[0])
                # else:
                # print("chaud")n
    if oldRay.find_Points():
        rays.append(oldRay)
    return rays
