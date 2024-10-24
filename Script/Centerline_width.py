# Import necessary libraries
import numpy as np
import pandas as pd
import rasterio
from skimage.measure import label, regionprops
from skimage.morphology import medial_axis
from shapely.geometry import LineString, mapping
import geopandas as gpd
from rasterio.features import rasterize

# Load the image
with rasterio.open('images/Extract_P1.tif') as ds:
    img = ds.read(1)
    transform = ds.transform

# Label the image
labels = label(img)

# Prepare lists to store the results
centerline_data = []
width_data = []

# Prepare an empty list to store the centerline geometries for rasterization
centerlines = []

for region in regionprops(labels):
    # Compute the medial axis (skeleton) of the region
    skeleton, distances = medial_axis(region.image, return_distance=True)

    # Compute the centerline as a LineString
    centerline = LineString(np.column_stack(np.where(skeleton)))

    # Compute the width along the centerline
    width = distances[skeleton].max()

    # Append the results to the lists
    centerline_data.append({'Label': region.label, 'Centerline': centerline})
    width_data.append({'Label': region.label, 'Width': width})

    # Append the centerline geometry to the list for rasterization
    centerlines.append(mapping(centerline))

# Create DataFrames from the lists
df_centerline = pd.DataFrame(centerline_data)
df_width = pd.DataFrame(width_data)

# Convert the centerline DataFrame to a GeoDataFrame
gdf_centerline = gpd.GeoDataFrame(df_centerline, geometry='Centerline')

# Set the CRS for the GeoDataFrame
gdf_centerline.set_crs(epsg=4326, inplace=True) # Replace 4326 with the appropriate EPSG code if known

# Save the DataFrames to CSV files
gdf_centerline.to_csv('centerlines.csv', index=False)
df_width.to_csv('widths.csv', index=False)

# Rasterize the centerlines
centerline_raster = rasterize(centerlines, out_shape=img.shape, transform=transform)

# Create a width raster by filling in the labeled regions with the corresponding widths
width_raster = np.zeros_like(img, dtype=np.float32)
for index, row in df_width.iterrows():
    width_raster[labels == row['Label']] = row['Width']

# Save the centerline and width rasters to GeoTIFF files
with rasterio.open('centerlines.tif', 'w', driver='GTiff', height=centerline_raster.shape[0], width=centerline_raster.shape[1], count=1, dtype=str(centerline_raster.dtype), crs=ds.crs, transform=transform) as dst:
    dst.write(centerline_raster, 1)

with rasterio.open('widths.tif', 'w', driver='GTiff', height=width_raster.shape[0], width=width_raster.shape[1], count=1, dtype=width_raster.dtype, crs=ds.crs, transform=transform) as dst:
    dst.write(width_raster, 1)

# Print a success message
print("Centerlines and widths have been saved to 'centerlines.csv', 'widths.csv', 'centerlines.tif', and 'widths.tif'.")
