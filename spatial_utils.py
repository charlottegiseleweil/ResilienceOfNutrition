import numpy as np

def area_of_pixel(pixel_size, center_lat):
    """Calculate m^2 area of a wgs84 square pixel.

    Adapted from: https://gis.stackexchange.com/a/127327/2397

    Parameters:
        pixel_size (float): length of side of pixel in degrees.
        center_lat (float): latitude of the center of the pixel. Note this
            value +/- half the `pixel-size` must not exceed 90/-90 degrees
            latitude or an invalid area will be calculated.

    Returns:
        Area of square pixel of side length `pixel_size` centered at
        `center_lat` in m^2.

    """
    a = 6378137  # meters
    b = 6356752.3142  # meters
    e = np.sqrt(1-(b/a)**2)
    area_list = []
    for f in [center_lat+pixel_size/2, center_lat-pixel_size/2]:
        zm = 1 - e*np.sin(np.radians(f))
        zp = 1 + e*np.sin(np.radians(f))
        area_list.append(
            np.pi * b**2 * (
                np.log(zp/zm) / (2*e) +
                np.sin(np.radians(f)) / (zp*zm)))
    return pixel_size / 360. * (area_list[0]-area_list[1])

def resample_raster(inputfile_path, referencefile_path, outputfile_path,band_num=1):
             
    input_raster = gdal.Open(inputfile_path, gdalconst.GA_ReadOnly)
    input_band = input_raster.GetRasterBand(band_num)
    inputProj = input_raster.GetProjection()
    inputTrans = input_raster.GetGeoTransform()

    reference = gdal.Open(referencefile_path, gdalconst.GA_ReadOnly)
    referenceProj = reference.GetProjection()
    referenceTrans = reference.GetGeoTransform()
    bandreference = reference.GetRasterBand(1)    
    x = reference.RasterXSize 
    y = reference.RasterYSize

    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(outputfile_path,x,y,1,bandreference.DataType)
    output.SetGeoTransform(referenceTrans)
    output.SetProjection(referenceProj)

    gdal.ReprojectImage(input_raster,output,inputProj,referenceProj,gdalconst.GRA_Bilinear)

    del output