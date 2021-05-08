import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp

MAPstyle = 2  # 1(corner) or 2(MET)
walls = Map.getWalls(MAPstyle)
ray = Ray(100, 65, 100, 40)
rays = getRayImages(100, 65, walls, ray)
print(len(rays))
dp.display(MAPstyle, rays)

# print("Number of processors: ", mp.cpu_count())