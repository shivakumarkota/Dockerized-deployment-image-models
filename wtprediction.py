# import rasterio
from osgeo import gdal
from ultralytics import YOLO
# import csv
import shutil
import os
from tqdm import tqdm
from time import sleep
import uuid

model = YOLO("best.pt")  # load a pretrainesd YOLOv8n model
 
def splitraster(input_img, out_path, xsize=512, ysize=512, save_vrt=False):
    """
    :param input_img: Geographic raster data as input
    :param out_path: Output directory for tiles images
    :param xsize: Size of X dimension
    :param ysize: Size of Y dimension
    :param save_vrt: (optional) Save output tiles into VRT
    :return:
    """
    # data to be written row-wise in csv file
    data = []

    if xsize < 1 or ysize < 1:
        raise Exception(print("[ ERROR! ] width or height dimension should be more then 1px"))
    else:
        pass
    tile_size_x = xsize
    tile_size_y = ysize
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    ds = gdal.Open(input_img)
    output_raster=str(uuid.uuid4())+'.tif'
    warp = gdal.Warp(output_raster,ds,dstSRS='EPSG:4326')
    ds=gdal.Open(output_raster)
    band = ds.GetRasterBand(1)
    x_size = band.XSize
    y_size = band.YSize
    # get only filename without extension
    output_filename = os.path.splitext(os.path.basename(input_img))[0]
    count = 0
    for i in range(0, x_size, tile_size_x):
        for j in tqdm(range(0, y_size, tile_size_y), leave=False):
            count += 1
            translate_options = gdal.TranslateOptions(bandList=[1, 2, 3],
                                                      noData="none",
                                                      srcWin=[i, j,
                                                              tile_size_x,
                                                              tile_size_y])
            filename = os.path.join(out_path, str(output_filename) + "_" + str(count) + ".tif") #
            gdal.Translate(filename, ds, options=translate_options)
            sleep(0.005)
            dsF = gdal.Open(filename) 

            # # open the dataset and get the geo transform matrix
            prdict=model.predict(source=filename, conf=0.5, retina_masks=True)  # predict on an image
            for result in prdict:                                         # iterate results
                boxes = result.boxes.cpu().numpy()                         # get boxes on cpu in numpy
                for box in boxes:                                          # iterate boxes
                    xmin, ymin,ymax,xmax = box.xyxy[0].astype(int)                            # get corner points as int
                    detectX,detectY=int((xmax-xmin))/2, int((ymax-ymin))/2
                    xoffset, px_w, rot1, yoffset, px_h, rot2 = dsF.GetGeoTransform()
                    # supposing x and y are your pixel coordinate this 
                    # is how to get the coordinate in space.
                    posX = px_w * detectX + rot1 * detectY + xoffset
                    posY = rot2 * detectX + px_h * detectY + yoffset
                    # shift to the center of the pixel
                    posX += px_w / 2.0
                    posY += px_h / 2.0
                    data.append([posX,posY])
    return data

