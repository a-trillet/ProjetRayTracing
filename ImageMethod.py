from Ray import Ray


def getRayImages(originX, originY, walls):
    rays = []
    for wall in walls:
        PsSN = (originX - wall.getOriginX())*wall.nX + (originY - wall.getOriginY())*wall.nY
        if PsSN != 0:
            ray = Ray(originX, originY)
            ray.imagePoints.append()
            rays.append(ray)
    return rays
