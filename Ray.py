class Ray:
    def __init__(self,originX,originY, receiverX, receiverY):
        self.originX = originX
        self.originY = originY
        self.receiverX = receiverX
        self.receiverY = receiverY
        self.imagePoints = []
        self.walls = []
        self.reflexionPoints = []
