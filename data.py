import numpy as np
import main
import Display

with open("saves/antenna3", 'rb') as f:
    a = np.load(f)
# Display.displayDPM(1, a, [[100, 45]])
f.close()

with open("saves/antenna4", 'rb') as f:
    b = np.load(f)
# Display.displayDPM(1, b)
f.close()

Display.displayDPM(2, a+b)
Display.displayDebit(2, a+b)
