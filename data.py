import numpy as np
import main
import Display

with open("test.npy", 'rb') as f:
    a = np.load(f)
Display.displayDPM(2, a, [[100, 45]])
f.close()