import rasterio
import openeo
import xarray as xr
import math
import csv
from scipy.ndimage import zoom
connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
connection.authenticate_oidc()
# reference square of area 50 000 to get a reference side length
a = [[117.745972,-34.189086],[114.89502,-34.189086],[114.89502,-32.472695],[117.745972,-32.472695],[117.745972,-34.189086]]
side =( abs(a[2][1]-a[0][1]) + abs(a[2][0]-a[0][0])) /2
def get_square_plot(x, y, side):
    return [[x-(side/2), y+(side/2)], [x+(side/2), y+(side/2)], [x+(side/2), y-(side/2)], [x-(side/2), y-(side/2)]]
f = open('Coordinates_FossilFuelPowerPlants.csv')
csvf = csv.reader(f)
aois = []
for row in csvf:
    if row[2] != 'latitude':
        i = [float(row[3]),float(row[2])]
        square = get_square_plot(i[0],i[1],side)
        square.append(i)
        rect = [square]
        aois.append(rect)
indices = [] # some squares are going over the limits. We omit those rectangles.
for k in range(len(aois)):
    aoi = aois[k]
    for coord in aoi[0]:
        if coord[0] < -180 or coord[0] > 180 or coord[1] < -90 or coord[1] > 90:
            indices.append(k)
            break
aois.remove(aois[indices[0]])
aois.remove(aois[indices[1]-1])
i = 33
n = 100
for rect in aois[i:i+n]:
    aoi = {"type":"Polygon","coordinates":rect}
    NO2_cube = connection.load_collection(
    "SENTINEL_5P_L2",
    bands=["NO2"],
    temporal_extent= ("2022-07-01", "2022-07-30"),
    spatial_extent=aoi
    )
    NO2_cube = NO2_cube.max_time()
    name = 'ImagesPowerPlants/PowerPlantspp'+ str(i)+'.tiff'
    NO2_cube.download(name)
    i = i+1