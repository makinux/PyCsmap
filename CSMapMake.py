# -*- coding: utf-8 -*
from PIL import Image
import os
import argparse
import requests
import math

from CSMap import CSMap

parser = argparse.ArgumentParser(description='MyScript')

parser.add_argument('images_x_start', type=int)
parser.add_argument('images_x_end', type=int)
parser.add_argument('images_y_start', type=int)
parser.add_argument('images_y_end', type=int)
parser.add_argument('zoom_level', type=int)
parser.add_argument('--outputPath', default="./")

args = parser.parse_args()

TILE_SIZE = 256

INPUT_URL = "http://cyberjapandata.gsi.go.jp/xyz/dem/"

OUTPUT_PATH = os.path.join(os.getcwd(),args.outputPath)
if not os.path.isdir(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

FILE_NAME = "CSMAP_%d-%d_%d-%d_%d.png" % (args.images_x_start, args.images_x_end, args.images_y_start, args.images_y_end, args.zoom_level)

def demtofloat(n):
    if n == 'e':
        return 0.0
    else:
        return float(n)

def csmap_make(images_x_start, images_x_end, images_y_start, images_y_end, zoom_level):
    size_x = TILE_SIZE * (images_x_end - images_x_start + 1)
    size_y = TILE_SIZE * (images_y_end - images_y_start + 1)
    cs_img = Image.new('RGBA', (size_x, size_y), (0, 0, 0, 0))

    for i in range(images_x_start, images_x_end + 1):
        for j in range(images_y_start, images_y_end + 1):
            input_image_url = INPUT_URL + str(zoom_level) + '/' +  str(i) + '/' + str(j) + '.txt'

            print 'input : ' + input_image_url
            res = requests.get(input_image_url, stream=True)
            if (res.status_code == 200):
                file = res.text
                file = file.split()
                dem_tmp = []
                for item in file:
                    dem_tmp.append(map(demtofloat, item.split(',')))

                dem = dem_tmp
                unit = 10 * math.pow(2, 14 - min(zoom_level, 14))
                cs_map = CSMap(dem, unit, image_size=[TILE_SIZE, TILE_SIZE])
                input_img_p = cs_map.cs_draw()

                print("Get tile : %d - %d - %d" % (zoom_level, i, j))
            else:
                input_img_p = Image.new('RGB', (TILE_SIZE, TILE_SIZE), (0, 0, 0))

                print("Can't get tile : %d - %d - %d" % (zoom_level, i, j))

            cs_img.paste(input_img_p, ((i - images_x_start) * TILE_SIZE, (j - images_y_start) * TILE_SIZE))

    return cs_img

cs_img = csmap_make(args.images_x_start, args.images_x_end, args.images_y_start, args.images_y_end, args.zoom_level)
cs_img.save(os.path.join(OUTPUT_PATH, FILE_NAME))
print "Image output : " + os.path.join(OUTPUT_PATH, FILE_NAME)






