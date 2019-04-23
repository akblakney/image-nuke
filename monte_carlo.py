import random
import cv2
import numpy as np

class Image:
    def __init__(self,img):
        self.img = img
        self.points = []
        self.defaultOrder()

    def incr(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][0] = (self.img[r,c][0] + amount) % 256  

    def incg(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][1] = (self.img[r,c][1] + amount) % 256  

    def incb(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][2] = (self.img[r,c][2] + amount) % 256
    
    
    # returns default ordering of points (as if they were
    # text on a page)
    def defaultOrder(self):
        points = []
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                points.append([r,c])
        self.points = points

    # returns outwards circle progression ordering of points
    # dradius is the width of the bands
    def circleOrder(self,dradius):
        points = []
        
        r_bar = self.img.shape[0] // 2
        c_bar = self.img.shape[1] // 2
        radius = dradius
        while radius < .5*(self.img.shape[0]**2+self.img.shape[1]**2)**.5:
            for r in range(self.img.shape[0]):
                for c in range(self.img.shape[1]):
                    point_rad = ((r - r_bar)**2 + (c - c_bar)**2)**.5 
                    if point_rad < radius and point_rad > radius - dradius:
                        points.append([r,c])
            radius += dradius

        self.points = points

    # set all points in image to black
    def black(self):
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                self.img[r,c][0] = 0
                self.img[r,c][1] = 0
                self.img[r,c][2] = 0

    # applies random walk filter over points
    # filter has mean mu and variance sigma^2
    # filter is applied over image; apply black() before for pure RW
    def randomWalk(self, mu, sigma):
        
        n = len(self.points)

        # generate init residuals
        rfilter = int(np.random.normal(mu,sigma)) % 256
        gfilter = int(np.random.normal(mu,sigma)) % 256
        bfilter = int(np.random.normal(mu,sigma)) % 256
        
        # generate rest of filters
        for i in range(n):
            self.incr(self.points[i][0], self.points[i][1], rfilter)
            self.incg(self.points[i][0], self.points[i][1], gfilter)
            self.incb(self.points[i][0], self.points[i][1], bfilter)
            rfilter = (rfilter + int(np.random.normal(0,sigma))) % 256
            gfilter = (gfilter + int(np.random.normal(0,sigma))) % 256
            bfilter = (bfilter + int(np.random.normal(0,sigma))) % 256

    # saturates image. I forget which values of s work well...
    def sat(self, s):
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                if self.img[r,c][0] < 128:
                    self.img[r,c][0] -= int((128 - self.img[r,c][0]) ** s)
                else:
                    self.img[r,c][0] += int((self.img[r,c][0] - 128) ** s)
                if self.img[r,c][1] < 128:
                    self.img[r,c][1] -= int((128 - self.img[r,c][1]) ** s)
                else:
                    self.img[r,c][1] += int((self.img[r,c][1] - 128) ** s)
                if self.img[r,c][2] < 128:
                    self.img[r,c][2] -= int((128 - self.img[r,c][2]) ** s)
                else:
                    self.img[r,c][2] += int((self.img[r,c][2] - 128) ** s)



image = cv2.imread('wp2try.jpg')
img = Image(image)

img.circleOrder(3)

#img.black()
img.randomWalk(150,.5)

#img.sat(.5)
cv2.imwrite('new.png', img.img)
    

