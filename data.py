import numpy as np
import main
import Display

with open("saves/antenna0", 'rb') as f:
    a = np.load(f)
# Display.displayDPM(2, a)
f.close()

with open("saves/antenna1", 'rb') as f:
    b = np.load(f)
# Display.displayDPM(2, b)
f.close()

with open("saves/antenna2", 'rb') as f:
    c = np.load(f)
# Display.displayDPM(2, c)
f.close()

with open("saves/antenna7", 'rb') as f:
    d = np.load(f)
# Display.displayDPM(2, c)
f.close()

Display.displayDPM(2, a+b+c+d)
Display.displayDebit(2, a+b+c+d)
