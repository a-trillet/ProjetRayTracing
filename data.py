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
               19: [],
               20: [],
               21: [],
               22: [],
               23: [],
               24: [],
               25: [],
               26: [],
               27: [],
               28: [],
               29: [],
               30: [],
               31: [],
               32: [],
               33: [],
               34: [],
               35: [],
               }
nbAntenne = len(dicoAntenna)

allresult = []
for i in range(nbAntenne):
    with open("saves/antenna"+str(i), 'rb') as f:
        allresult.append(np.load(f))
    f.close()
Display.displayDPM(2, allresult, dicoAntenna)
Display.displayDebit(2, allresult, dicoAntenna)
