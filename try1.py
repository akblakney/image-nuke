import random
import cv2
import numpy as numpy

def makeLs():
    for i in range(80):
        line_len = 40
        pt = [random.randint(0, int(img.shape[0] / 2)),\
            random.randint(0, img.shape[1] - 1)]
        if pt[0] > line_len and pt[1] > line_len:
            for j in range(line_len):
                img[pt[0] - j, pt[1]] = img[pt[0], pt[1]]
                img[pt[0], pt[1] - j] = img[pt[0], pt[1]]



class Image:
    def __init__(self, img):
        self.img = img
        self.blocks = None

    # sets blocks field according to params xlen and ylen
    def get_blocks(self, xlen, ylen):
        
        blocks = []
        xmin = 0
        ymin = 0

        while ymin < self.img.shape[0]:
            ymax = ymin + ylen
            while xmin < self.img.shape[1]:
                xmax = xmin + xlen
                if xmin + xlen > self.img.shape[1]:
                    xmax = self.img.shape[1]
                if ymin + ylen > self.img.shape[0]:
                    ymax = self.img.shape[0]
                
                blocks.append(Block(xmin, xmax, ymin, ymax, self.img))
                
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

    # apply a color gradient over the iamge
    def color_grad(self, p_change):
        count = 0
        for r in range(self.img.shape[0]):
            for c in range(self.img.shape[1]):
                if random.random() < p_change:
                    self.inc_pixel(r, c, count)
                    count += 1

    def inc_pixel(self, r, c, amount):
        if r >= self.img.shape[0] or c >= img.shape[1] \
            or r < 0 or c < 0:
            return
        self.img[r,c][0] = self.img[r,c][0] + amount
        self.img[r,c][1] = self.img[r,c][1] + amount
        self.img[r,c][2] = self.img[r,c][2] + amount

    def quadratic(self, width):
        ystart = random.randint(0, self.img.shape[0])
        xstart = random.randint(0, self.img.shape[1])
        a = random.random() * 6 - 3
        b = random.random() * 6 - 3

        for c in range(self.img.shape[1]):
            r = int(a * c ** 2 + b * c + ystart)
            for c_offset in range(width):
                for r_offset in range(width):
                    self.inc_pixel(r + r_offset, c + c_offset + xstart, 100)



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

        

img = cv2.imread('carl.png')
print(img.shape)

i = Image(img)
i.get_blocks(5,10)

for _ in range(1000):
    i.swap_blocks(i.blocks[random.randint(0,len(i.blocks) - 1)], \
        i.blocks[random.randint(0,len(i.blocks) - 1)])
 
i.color_grad(0.3)
for _ in range(10):
    i.quadratic(40)

cv2.imwrite('carlfixed.png', img)
