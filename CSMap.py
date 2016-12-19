from PIL import Image
import numpy as np
import math

class CSMap:
    def __init__(self, dem, unit, image_size=[256, 256]):
        self.dem = np.array(dem)
        self.unit = float(unit)
        self.image_size_x = image_size[0]
        self.image_size_y = image_size[1]

        self.ticker = []
        for i in range(0, 256):
            self.ticker.append(math.pow(math.tan((math.pi / 2.0) * (i / 256.0)), 2))

    def _slope(self, i, j):
        if (i == 0):
            return self._slope(i + 1, j)
        if (i == 255):
            return self._slope(i - 1, j)
        if (j == 0):
            return self._slope(i, j + 1)
        if (j == 255):
            return self._slope(i, j - 1)

        dem = self.dem / self.unit

        y = (dem[i + 1][j] * 2 + dem[i + 1][j + 1] + dem[i + 1][j - 1]) - (dem[i - 1][j] * 2 + dem[i - 1][j - 1] + dem[i - 1][j + 1])
        x = (dem[i][j + 1] * 2 + dem[i - 1][j + 1] + dem[i + 1][j + 1]) - (dem[i][j - 1] * 2 + dem[i - 1][j - 1] + dem[i + 1][j - 1])
        z = x * x + y * y

        for k, item in enumerate(self.ticker):
            if item >= z:
                return k
        return 0


    def _curvature(self, i, j):
        dem = self.dem * 255.0 / self.unit
        dem = np.r_[dem[0].reshape(1, len(dem[0])), dem]
        dem = np.r_[dem, dem[255].reshape(1, len(dem[255]))]
        dem = np.c_[dem[:,0].reshape(len(dem[:,0]), 1), dem]
        dem = np.c_[dem, dem[:,255].reshape(len(dem[:,255]))]

        i += 1
        j += 1
        c = 127
        c += dem[i][j] * 4
        c -= dem[i - 1][j]
        c -= dem[i + 1][j]
        c -= dem[i][j - 1]
        c -= dem[i][j + 1]

        return c


    def cs_draw(self):
        slope_img = Image.new('RGBA', (self.image_size_x, self.image_size_y), (0, 0, 0, 0))
        curvature_img = Image.new('RGBA', (self.image_size_x, self.image_size_y), (0, 0, 0, 0))

        for i in range(0, self.image_size_y):
            for j in range(0, self.image_size_x):
                c1 = self._slope(i, j)
                if (c1 < 160):
                    t = c1 / 160.0
                    r = int(255 + (255 - 255) * t)
                    g = int(255 + (51 - 255) * t)
                    b = int(255 + (0 - 255) * t)
                    a = int(255 * 0.5)
                    slope_img.putpixel((j,i),(r,g,b,a))
                else:
                    t = (c1 - 160.0) / (255.0 - 160.0)
                    r = int(255 + (51 - 255) * t)
                    g = int(51 + (0 - 51) * t)
                    b = int(0 + (0 - 0) * t)
                    a = int(255 * 0.5)
                    slope_img.putpixel((j,i),(r,g,b,a))

                c2 = self._curvature(i, j)
                if (c2 < 128):
                    t = c2 / 128.0
                    r = int(0 + (68 - 0) * t)
                    g = int(0 + (68 - 0) * t)
                    b = int(0 + (255 - 0) * t)
                    a = 255
                    curvature_img.putpixel((j,i),(r,g,b,a))
                else:
                    t = (c2 - 128.0) / (255.0 - 128.0)
                    r = int(68 + (255 - 68) * t)
                    g = int(68 + (255 - 68) * t)
                    b = int(255 + (255 - 255) * t)
                    a = 255
                    curvature_img.putpixel((j,i),(r,g,b,a))

        cs_img = Image.alpha_composite(curvature_img, slope_img)
        #slope_img.save('./slope_img.png')
        #curvature_img.save('./curvature_img.png')
        return cs_img


