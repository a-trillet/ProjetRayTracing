import numpy as np
import main
import Display

with open("antenna0", 'rb') as f:
    a = np.load(f)
#Display.displayDPM(1, a, [[100, 45]])
f.close()

with open("antenna1", 'rb') as f:
    b = np.load(f)
#Display.displayDPM(1, b)
f.close()

with open("antenna2", 'rb') as f:
    c = np.load(f)
#Display.displayDPM(1, c)
f.close()

Display.displayDPM(1, a+c)