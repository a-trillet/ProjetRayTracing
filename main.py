import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp

MAPstyle = 1  # 1(corner) or 2(MET)
walls = Map.getWalls(2)
ray = Ray(100, 65, 100, 40)
#rays = getRayImages(0, 0, walls, ray)
#print(len(rays))
dp.display()

print("Number of processors: ", mp.cpu_count())