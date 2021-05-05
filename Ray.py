class Ray:
    def __init__(self,originX,originY):
        self.originX = originX
        self.originY = originY
        self.receiver = [0, 0]
        self.imagePoints = []
        self.reflexionPoints = []
