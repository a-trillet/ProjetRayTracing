
class wall:
    def __init__(self, xOrigin, yOrigin, xDirection, yDirection, material):
        self.n=[xDirection,yDirection]
        self.origin = [xOrigin,yOrigin]
        self.material = material
        self.relativePermitivity = 0
        self.condctivity = 0

    def getOriginX(self):
        return self.origin[0]
    def getOriginY(self):
        return self.origin[1]
    def getNx(self):
        return self.n[0]
    def getNy(self):
        return self.n[1]

    def set(self, material):
        if material == "brick":
            self.condctivity = 0.02
            self.relativePermitivity = 4.6
        elif material == "concrete":
            self.condctivity = 0.014
            self.relativePermitivity = 5
        elif material == "partition":
            self.condctivity = 0.04
            self.relativePermitivity = 2.25
        else:
            print("matériau inconnu")
