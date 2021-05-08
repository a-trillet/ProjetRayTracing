import Map
from Ray import *
from ImageMethod import *
import Display as dp

MAPstyle = 1  # 1(corner) or 2(MET)
walls = Map.getWalls(1)
ray = Ray(0, 0, 0, 5)
rays = getRayImages(0, 0, walls, ray)
print(len(rays))
dp.display()
