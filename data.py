import numpy as np
import Display
import math
from main import xMAP, yMAP, nbReflexion
"""Ce fichier permet d'afficher les résultats calculé précédemment en choisissant plusieurs antennes
à la fois
"""

dicoAntenna = {0: [100, 45],
               1: [36, 49],
               2: [170, 34],
               3: [40, 20],
               4: [100, 90],
               5: [79, 31],
               6: [170, 20],
               7: [33, 77],
               8: [100, 82],
               9: [100, 78],
               10: [100, 67],
               11: [38, 70],
               12: [14, 70],
               13: [164, 75],
               14: [151, 67],
               15: [138, 72],
               16: [151, 60],
               17: [180, 60],
               18: [28, 28],
               19: [15, 35],
               20: [33, 40],
               21: [151, 50],
               22: [100, 20],
               23: [10, 20],
               24: [123, 40],
               25: [25, 70],
               26: [32, 28],
               27: [60, 70],
               28: [88, 50],
               29: [25, 62],
               30: [37, 52],
               31: [80, 45],
               32: [90, 35],
               33: [36, 32],
               34: [69, 28],
               35: [69, 41],
               36: [72, 13],
               37: [170, 50],
               38: [125, 55],
               39: [125, 67],
               40: [100, 20]
               }
dicoAntennaGP = {0: [45, 100-0.2],
                 1: [45, 100-0.2],
                 2: [45, 100-0.2],
                 3: [65, 0 + 0.2],  # d = 0.97 lam
                 4: [45, 100-0.2],  # d = 5/4  lam
                 5: [60, 100-0.2],  # d = 1/4 lam
                 6: [60, 100-0.2],  # d = 3/4 lam
                 7: [60, 100-0.2],  # d = 2/4 lam
                 8: [60, 100-0.2],  # d = 4/4 lam
                 9: [60, 100-0.2],  # d = 5/4 lam
                 10: [60, 100-0.2],  # d = 6/4 lam
                 }
dicoTest = {0: [20, 80]}
nbAntenne = len(dicoAntennaGP)

allresult = []
for i in range(nbAntenne):
    with open("saves/GrandPlace"+str(i), 'rb') as f:
        allresult.append(np.load(f))
    f.close()

# print(10 * math.log10(allresult[10][5][90]*1000), " dBm in (90, 5)")
Display.displayDPM(3, allresult, dicoAntennaGP)
Display.displayDebit(3, allresult, dicoAntennaGP)
