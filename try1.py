import random
import cv2
import numpy as np

class Block:
    
    # min values are invlusive, max values are exclusive
    def __init__(self, min_x, max_x, min_y, max_y, img):
        self.img = img
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.xlen = self.max_x - self.min_x
        self.ylen = self.max_y - self.min_y
        self.pixels = []
        for r in range(self.min_y, self.max_y):
            for c in range(self.min_x, self.max_x):
                self.pixels.append(img[r, c])
        self.avg_color = 0
        for px in self.pixels:
            self.avg_color += px[2]
        self.avg_color /= len(self.pixels)
    
    # make entire block the average block color
    def avg(self):
        for r in range(self.min_y, self.max_y):
            for c in range(self.min_x, self.max_x):
                img[r, c] = self.avg_color



class Image:
    def __init__(self, img):
        self.img = img
        self.blocks = None

    # sets blocks field according to params xlen and ylen
    def get_blocks(self, xlen, ylen, xmin, ymin, xmax, ymax):
        
        blocks = []

        while ymin < ymax:
            ymax_ = ymin + ylen
            while xmin < xmax:
                xmax_ = xmin + xlen
                if xmin + xlen > xmax:
                    xmax_ = xmax
                if ymin + ylen > ymax:
                    ymax_ = ymax
                
                blocks.append(Block(xmin, xmax_, ymin, ymax_, self.img))
                
                xmin += xlen
            xmin = 0
            ymin += ylen 

        self.blocks = blocks

    # swaps the contents of b1 and b2 in image
    # blocks must be the same dimension
    def swap_blocks(self, b1, b2):
        x1len = b1.max_x - b1.min_x
        x2len = b2.max_x - b2.min_x
        y1len = b1.max_y - b1.min_y
        y2len = b2.max_y - b2.min_y

        if x1len != x2len or y1len != y2len or b1 == b2:
            return
        
        # set pixels in b1 location
        for r in range(y1len):
            for c in range(x1len):
                p1 = list(self.img[r + b1.min_y, c + b1.min_x])
                self.img[r + b1.min_y, c + b1.min_x] = \
                    self.img[r + b2.min_y, c + b2.min_x]
                self.img[r + b2.min_y, c + b2.min_x] = p1
                #print(self.img[r + b1.min_y, c + b1.min_x] == p1)

    # apply a color gradient over the iamge; each pixel incremented
    # with probability p_change
    def color_grad(self, p_change):
        count = 0
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                if random.random() < p_change:
                    self.inc_pixel(r, c, count)
                    count += 1

    def inc_r(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][0] = (self.img[r,c][0] + amount) % 256  

    def inc_g(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][1] = (self.img[r,c][1] + amount) % 256  

    def inc_b(self,r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return

        self.img[r,c][2] = (self.img[r,c][2] + amount) % 256  

    # increments RGB values of pixel with coords r and c by amount
    def inc_pixel(self, r, c, amount):
        if r >= self.img.shape[0] or c >= self.img.shape[1] \
            or r < 0 or c < 0:
            return
        self.inc_r(r, c, amount)
        self.inc_g(r, c, amount)
        self.inc_b(r, c, amount)

    def quadratic(self, width):
        ystart = random.randint(0, self.img.shape[0])
        xstart = random.randint(0, self.img.shape[1])
        a = random.random() * 3 - 1.5
        b = random.random() * 3 - 1.5

        for c in range(self.img.shape[1]):
            r = int(a * c ** 2 + b * c + ystart)
            for c_offset in range(width):
                for r_offset in range(width):
                    self.inc_pixel(r + r_offset, c + c_offset + xstart, 100)


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

    # as rchance is increased, get horseshoe-type distortion
    # decreasing rchange to approx .5 yields more homogeneous discoloration
    # of the image
    # increasing pat 1.0 gives horseshoe stripes 
    def horseshoe(self, rchange, cchange, red, green, blue):
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                if random.random() < red:
                    self.inc_r(r, c, int(r ** rchange * c ** cchange) % 256)
                if random.random() < green:
                    self.inc_g(r, c, int(r ** rchange * c ** cchange) % 256)
                if random.random() < blue:
                    self.inc_b(r, c, int(r ** rchange * c ** cchange) % 256)
    
    # returns list of points in img that are in the given circle
    def circle(self, rcenter, ccenter, radius):
        circ = [self.img[rcenter,ccenter]]
        for r in range(rcenter - radius, rcenter + radius):
            for c in range(ccenter - radius, ccenter + radius):
                if ((r - rcenter) ** 2 + (c - ccenter) ** 2) ** .5 <= radius:
                    circ.append(self.img[r,c])
        return circ

    def block(self, rcenter, ccenter, radius):
        circ = [self.img[rcenter, ccenter]]
        for r in range(rcenter - radius, rcenter + radius):
            for c in range(ccenter - radius, ccenter + radius):
                circ.append(self.img[r,c])
        return circ

    # returns average R value for the given points
    def avg_color(self,points, identifier):
        if identifier < 0 or identifier > 2 or len(points) < 1:
            return
        color = 0
        for point in points:
            color += point[identifier]
        return color / len(points)

    # smooths circle centered at r, c with radius rad
    def smooth(self, r, c, rad, iter, size):
        
        # smooth points in circ by smoothing many small circles in circ
        for _ in range(iter):
            rtemp = random.randint(r - rad, r + rad)
            ctemp = random.randint(c - rad, c + rad)
            if ((rtemp - r) ** 2 + (ctemp - c) ** 2) ** .5 > rad:
                continue
            circtemp = self.circle(rtemp, ctemp, size)
            #circtemp = self.block(rtemp, ctemp, size)
            for j in range(3):
                avg = self.avg_color(circtemp, j)
                for point in circtemp:
                    point[j] = avg

    def shuffle(self):
        self. get_blocks(5, 5, 170, 160, 513, 210)
        for _ in range(10000):
            self.swap_blocks(self.blocks[random.randint(0, len(self.blocks) - 1)], \
                self.blocks[random.randint(0, len(self.blocks) - 1)])

    def randomWalk(self, sigma):
        xr = random.randint(0,255)
        xg = random.randint(0,255)
        xb = random.randint(0,255)
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                self.img[r,c][0] = xr
                self.img[r,c][1] = xg
                self.img[r,c][2] = xb
                
                xr += int(np.random.normal(0,sigma)) % 256
                xg += int(np.random.normal(0,sigma)) % 256
                xb += int(np.random.normal(0,sigma)) % 256

    def whiteNoise(self):
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                self.img[r,c][0] = random.randint(0,255)
                self.img[r,c][1] = random.randint(0,255)
                self.img[r,c][2] = random.randint(0,255)

    def randomWalk2(self, sigma, points):
        xr = random.randint(0,255)
        xg = random.randint(0,255)
        xb = random.randint(0,255)
        for point in points:
            self.img[point[0],point[1]][0] = xr
            self.img[point[0],point[1]][1] = xg
            self.img[point[0],point[1]][2] = xb

            xr += int(np.random.normal(0,sigma)) % 256
            xg += int(np.random.normal(0,sigma)) % 256
            xb += int(np.random.normal(0,sigma)) % 256

    # returns ordered list of points [[r1,c1],...,[rn,cn]]
    # progressing outwards from the center
    # dradius is the width of the bands, or increment of the radius
    # in a polar coordinate system
    def circleOrder(self,dradius):
        points = []
        
        r_bar = self.img.shape[0] // 2
        c_bar = self.img.shape[1] // 2
        radius = dradius
        while radius < max(r_bar, c_bar):
            for r in range(self.img.shape[0]):
                for c in range(self.img.shape[1]):
                    point_rad = ((r - r_bar)**2 + (c - c_bar)**2)**.5 
                    if point_rad < radius and point_rad > radius - dradius:
                        points.append([r,c])
            radius += dradius

        return points




image = cv2.imread('wp2try.jpg')
img = Image(image)
'''
index = 10
for rchange in np.linspace(.10,.2,25):
    img = Image(image)
    img.horseshoe(rchange,.25, 1,1,.2)
    img.horseshoe(rchange,.25, 1,1,.2)
    cv2.imwrite('i' + str(index) + '.png', img.img)
    index += 1

curr_img = img

for cchange in np.linspace(.25,.15,25):
    img = curr_img    
    img.horseshoe(.2,cchange,1,1,.2)
    img.horseshoe(.2,cchange,1,1,.2)
    cv2.imwrite('i' + str(index) + '.png', img.img)
    index += 1

#img.shuffle()

#img.smooth(image.shape[0] // 2, image.shape[1] // 2, 200,15000, 2)
'''
index = 10
points = img.circleOrder(3)
for sigma in np.linspace(0,3,6):
    img.randomWalk2(sigma, points)
    cv2.imwrite('rw' + str(index) + '.png',img.img)
    index += 1
#cv2.imwrite('randomwalk.png',img.img)