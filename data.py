import numpy as np
import main
import Display
dicoAntenna = {0: [100, 45],
               1: [36, 49],
               2: [170, 34],
               3: [40, 20],
               4: [100, 90],
               5: [79, 31],
               6: [170, 20]}
nbAntenne = len(dicoAntenna)

allresult = []
for i in range(nbAntenne):
    with open("saves/antenna"+str(i), 'rb') as f:
        allresult.append(np.load(f))
    f.close()

Display.displayDPM(2, allresult, dicoAntenna)
Display.displayDebit(2, allresult, dicoAntenna)
