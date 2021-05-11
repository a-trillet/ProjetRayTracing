import Map
from datetime import datetime

init_time = datetime.now()
walls = Map.getWalls(2)
wallsH = Map.getWallsH(walls)
wallsV = Map.getWallsV(walls)
fin_time = datetime.now()
print("Execution time: ", (fin_time - init_time))