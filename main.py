import Map
from Ray import *
from ImageMethod import *
import Display as dp
import multiprocessing as mp
import numpy as np


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
    pool = mp.Pool(12)
    MAPstyle = 2  # 1(corner) or 2(MET)
    walls = Map.getWalls(MAPstyle)
    for x in range(5):
        for y in range(5):
            pool.apply_async(nb_of_rays, args=(x, y, walls), callback=collect_results)
    pool.close()
    pool.join()
    #dp.display(MAPstyle, rays)


MAPstyle = 1  # 1(corner) or 2(MET)
walls = Map.getWalls(MAPstyle)
ray = Ray(0, 0, 0, 5)
rays = getRayImages(0, 0, walls, ray)
print(len(rays))
for i in rays:
    i.find_Points()
dp.display(MAPstyle, rays)

    # print("Number of processors: ", mp.cpu_count())




if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    main()  # execute this only when run directly, not when imported!
