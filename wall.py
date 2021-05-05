class wall:
    def __init__(self,xOrigin,yOrigin,xDirection, yDirection):
        self.n=[xDirection,yDirection]
        self.origin = [xOrigin,yOrigin]
    def getOriginX(self):
        return self.origin[0]
    def getOriginY(self):
        return self.origin[1]
    def getNx(self):
        return self.n[0]
    def getNy(self):
        return self.n[1]
