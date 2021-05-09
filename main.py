import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp

MAPstyle = 2  # 1(corner) or 2(MET)
walls = Map.getWalls(MAPstyle)
if MAPstyle == 1:
    ray = Ray(0, 0, 0, 5)
    rays = getRayImages(0, 0, walls, ray)
else:
    ray = Ray(100, 45, 100, 40)
    rays = getRayImages(100, 45, walls, ray)
print(len(rays))
for i in rays:
    i.find_Points()
dp.display(MAPstyle, rays)

# print("Number of processors: ", mp.cpu_count())