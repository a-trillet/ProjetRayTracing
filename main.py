import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp
import numpy as np
from datetime import datetime

results = np.zeros((110, 200))


def collect_results(result):
    global results
    results[result[0]][result[1]] = result[2]
    print(result[2])


def nb_of_rays(i, j, walls):
    ray = Ray(100, 65, 10*i, 10*j)
    rays = getRayImages(100, 65, walls, ray)
    return i, j, len(rays)


def main():
    init_time = datetime.now()
    pool = mp.Pool(12)
    MAPstyle = 2  # 1(corner) or 2(MET)
    walls = Map.getWalls(MAPstyle)
    for x in range(5):
        for y in range(5):
            pool.apply_async(nb_of_rays, args=(x, y, walls), callback=collect_results)
    pool.close()
    pool.join()
    #dp.display(MAPstyle, rays)
    fin_time = datetime.now()
    print("Execution time: ", (fin_time - init_time))


MAPstyle = 2  # 1(corner) or 2(MET)
walls = Map.getWalls(MAPstyle)
if MAPstyle == 1:
    ray = Ray(0, 0, 0, 5)
    rays = getRayImages(0, 0, walls, ray)
else:
    ray = Ray(100, 45, 100, 40)
    rays = getRayImages(100, 45, walls, ray)
print(len(rays))
power = 0
Z0 = 376.730313
Ra = 73
c = 299792458
lam = c/(27 * 10**9)
he = -lam/math.pi
factor = he**2/8/Ra
Gtx = 1.6977
Ptx = 0.1   # [W]
"""for i in rays:
    if i.find_Points():
        power += i.getPower
power *= factor * 60*Gtx*Ptx"""
dp.display(MAPstyle, rays)

    # print("Number of processors: ", mp.cpu_count())




"""if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    main()  # execute this only when run directly, not when imported!"""
