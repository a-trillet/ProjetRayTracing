from Ray import Ray


# créer un ray de base Ray(originX, originY, receiverX, receiverY))
def getRayImages(originX, originY, walls, oldRay):
    rays = [oldRay]
    e = len(oldRay.imagePoints)
    if e <3:
        for wall in walls:
            if oldRay.walls == [] or wall != oldRay.walls[-1]:
                PsSN = (originX - wall.getOriginX()) * wall.nX + (originY - wall.getOriginY()) * wall.nY
                if PsSN != 0:
                    ray = oldRay
                    ray.walls.append(wall)
                    ray.imagePoints.append([originX - 2 * PsSN * wall.nX, originY - 2 * PsSN * wall.nY])
                    rays.extend(getRayImages(ray.imagePoints[e][0], ray.imagePoints[e][1], walls, ray))
                else:
                    print("rayon // à un mur")
            else:
                print(wall.origin[0])
    else:
        print("chaud")
    return rays
