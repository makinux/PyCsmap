from PIL import Image
import numpy as np
import math
import time

class CSMap:
    def __init__(self, dem, unit, image_size=[256, 256]):
        self.unit = float(unit)
        self.image_size_x = image_size[0]
        self.image_size_y = image_size[1]
        if not isinstance(dem, np.ndarray):
            dem = np.array(dem)
        dem = np.r_[dem[0].reshape(1, len(dem[0])), dem]
        dem = np.r_[dem, dem[self.image_size_y].reshape(1, len(dem[self.image_size_y]))]
        dem = np.c_[dem[:,0].reshape(len(dem[:,0]), 1), dem]
        dem = np.c_[dem, dem[:,self.image_size_x].reshape(len(dem[:,self.image_size_x]), 1)]
        self.dem = dem

    def _slope(self):

        dem = self.dem / self.unit

        y = (dem[2:, 1:-1] * 2.0 + dem[2:, 2:] + dem[2:, :-2]) - (dem[:-2, 1:-1] * 2.0 + dem[:-2, :-2] + dem[:-2, 2:])
        x = (dem[1:-1, 2:] * 2.0 + dem[:-2, 2:] + dem[2:, 2:]) - (dem[1:-1, :-2] * 2.0 + dem[:-2, :-2] + dem[2:, :-2])

        z = x * x + y * y

        re_slope = (np.arctan(np.sqrt(z)) / math.pi) * 2.0 * 256.0
        return re_slope

    def _curvature(self):
        dem = self.dem * 255.0 / self.unit

        c = np.zeros((self.image_size_y, self.image_size_x)) + 127
        c += dem[1:-1, 1:-1] * 4
        c -= dem[:-2, 1:-1]
        c -= dem[2:, 1:-1]
        c -= dem[1:-1, :-2]
        c -= dem[1:-1, 2:]

        return c


    def cs_draw(self):
        startall_time = time.time()
        slope_img = Image.new('RGBA', (self.image_size_x, self.image_size_y), (0, 0, 0, 0))
        curvature_img = Image.new('RGBA', (self.image_size_x, self.image_size_y), (0, 0, 0, 0))
        start_time = time.time()
        c1_list = self._slope()
        #print 'Slope : ' + str(time.time() - start_time) + 'sec'
        start_time = time.time()
        c2_list = self._curvature()
        #print 'Curvature : ' + str(time.time() - start_time) + 'sec'
        start_time = time.time()

        slope_array = np.zeros((self.image_size_y, self.image_size_x, 4))
        curvature_array = np.zeros((self.image_size_y, self.image_size_x, 4))

        slope_array[:, :, 0] = np.where(c1_list < 160.0, (255 + (255 - 255) * (c1_list / 160.0)), (255 + (51 - 255) * ((c1_list - 160.0) / (255.0 - 160.0))))
        slope_array[:, :, 1] = np.where(c1_list < 160.0, (255 + (51 - 255) * (c1_list / 160.0)), (51 + (0 - 51) * ((c1_list - 160.0) / (255.0 - 160.0))))
        slope_array[:, :, 2] = np.where(c1_list < 160.0, (255 + (0 - 255) * (c1_list / 160.0)), (0 + (0 - 0) * ((c1_list - 160.0) / (255.0 - 160.0))))
        slope_array[:, :, 3] = 255 * 0.5
        slope_array = np.where(slope_array < 0, 0, slope_array)
        slope_array = np.where(slope_array > 255, 255, slope_array)

        curvature_array[:, :, 0] = np.where(c2_list < 128.0, (0 + (68 - 0) * (c2_list / 128.0)), (68 + (255 - 68) * ((c2_list - 128.0) / (255.0 - 128.0))))
        curvature_array[:, :, 1] = np.where(c2_list < 128.0, (0 + (68 - 0) * (c2_list / 128.0)), (68 + (255 - 68) * ((c2_list - 128.0) / (255.0 - 128.0))))
        curvature_array[:, :, 2] = np.where(c2_list < 128.0, (0 + (255 - 0) * (c2_list / 128.0)), (255 + (255 - 255) * ((c2_list - 128.0) / (255.0 - 128.0))))
        curvature_array[:, :, 3] = 255
        curvature_array = np.where(curvature_array < 0, 0, curvature_array)
        curvature_array = np.where(curvature_array > 255, 255, curvature_array)

        slope_img = Image.fromarray(np.uint8(slope_array))
        curvature_img = Image.fromarray(np.uint8(curvature_array))

        cs_img = Image.alpha_composite(curvature_img, slope_img)
        return cs_img


