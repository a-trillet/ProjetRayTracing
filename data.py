import numpy as np
import main
import Display
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
               22: [28, 28],
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
               38: [125, 55]
               }
nbAntenne = len(dicoAntenna)

allresult = []
for i in range(nbAntenne):
    with open("saves/antenna"+str(i), 'rb') as f:
        allresult.append(np.load(f))
    f.close()
Display.displayDPM(2, allresult, dicoAntenna)
Display.displayDebit(2, allresult, dicoAntenna)
