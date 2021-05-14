from Wall import Wall


def sortWallsH(wall):
    return wall.origin[1]


def getWallsH(walls):
    wallsH = []
    for wall in walls:
        if wall.yDirection == 0:
            wallsH.append(wall)
    wallsH.sort(key=sortWallsH)
    return wallsH


def sortWallsV(wall):
    return wall.origin[0]


def getWallsV(walls):
    wallsV = []
    for wall in walls:
        if wall.xDirection == 0:
            wallsV.append(wall)
    wallsV.sort(key=sortWallsV)
    return wallsV


def getWalls(mapType):
    walls = []
    if mapType == 1:
        walls.append(Wall(130, 30, 0, 50, "concrete"))
        walls.append(Wall(50, 80, 70, 0, "concrete"))
        #walls.append(Wall(0, 10, 10, 0, "brick"))
        #walls.append(Wall(100, -5, 0, 100, 'brick'))
    """ 
        shéma du système de deux murs 
         
             .(10,10) 
    ----------     |.(15,10)
                   |
                   |
                   |
    . (0,0)        |              
    """

    if mapType == 2:
        # note, vecteurs choisis positif avec y vers le haut et x vers la droite (origine du plan MET en bas à doite)
        coordBrique = [[75, 10, 0, 5], [125, 10, 0, 5], [0, 30, 5, 0], [10, 30, 25, 0], [30, 15, 0, 15],
                       [35, 30, 0, 35], [37, 30, 31, 0], [70, 30, 25, 0], [75, 25, 0, 5], [95, 30, 0, 20],
                       [105, 30, 0, 20], [105, 30, 15, 0], [125, 25, 0, 5], [125, 30, 50, 0], [175, 30, 0, 35],
                       [165, 65, 20, 0], [187, 65, 3, 0], [165, 65, 0, 5], [10, 65, 3, 0], [15, 65, 20, 0],
                       [35, 50, 50, 0], [85, 40, 0, 10], [90, 50, 5, 0], [90, 50, 0, 15], [90, 70, 0, 10],
                       [90, 80, 20, 0], [110, 70, 0, 10], [110, 70, 30, 0], [140, 70, 0, 20], [105, 50, 35, 0],
                       [140, 40, 0, 10], [140, 40, 20, 0], [160, 40, 0, 20], [152, 60, 8, 0], [140, 60, 10, 0],
                       [140, 60, 0, 5], [110, 65, 30, 0], [110, 58, 0, 7], [110, 50, 0, 6], [10, 75, 3, 0],
                       [15, 75, 20, 0], [35, 75, 0, 15], [165, 80, 0, 10]]
        coordBeton = [[0, 0, 0, 65], [0, 65, 10, 0], [10, 65, 0, 35], [10, 100, 25, 0], [35, 90, 0, 10],
                      [35, 90, 55, 0], [90, 90, 0, 5], [85, 95, 5, 0], [85, 95, 0, 15], [85, 110, 30, 0],
                      [115, 95, 0, 15], [110, 95, 5, 0], [110, 90, 0, 5], [110, 90, 55, 0], [165, 90, 0, 10],
                      [165, 100, 25, 0], [190, 65, 0, 35], [190, 65, 10, 0], [200, 0, 0, 65], [165, 0, 35, 0],
                      [165, 0, 0, 10], [105, 10, 60, 0], [35, 10, 60, 0], [35, 0, 0, 10], [0, 0, 35, 0]]
        for i in range(len(coordBrique)):
            walls.append(Wall(coordBrique[i][0], coordBrique[i][1], coordBrique[i][2], coordBrique[i][3], "brick"))
        for i in range(len(coordBeton)):
            walls.append(Wall(coordBeton[i][0], coordBeton[i][1], coordBeton[i][2], coordBeton[i][3], "concrete"))

    return walls
