# Medial-Axis-Transform

It will include script and dataset to find river width and centerline from Sentinal 1A image using deep learning model DeepLabV3.
The repository contains a notebook to extract river centerline and width with sample data and results.

## Installation of required packages
For Jupyter notebook, ArcGIS Pro and Google Colab notebook use this command: install required libraries if not installed by uncommenting it:

#!pip install geopandas

#!pip install numpy

#!pip install pandas

#!pip install rasterio

#!pip install skimage

#!pip install shapely

Other options, installing it by using the package manager in ArcGIS Pro, to add necessary packages to operate this program such as rasterio, geopandas, numpy, pandas, and skiimage.

## Usage Guide
The easiest and quickest way to use the Medial Axis Transform is to run it from Jupyter notebook or Google Colab, where the functions can be directly loaded without setup. The tutorial for using the tool is shared on my YouTube channel (learnsomethingtoday): [https://youtu.be/J0KKxBf-vLI](https://youtu.be/POs02W3LgS8)

### Explanation
The code performs the following tasks:

1. **Importing Libraries**:
   - The code imports several libraries necessary for image processing, geometric operations, and data handling, including `numpy`, `pandas`, `rasterio`, `skimage`, `shapely`, and `geopandas`.

2. **Loading the Image**:
   - The image is loaded using `rasterio.open`, which reads the image file (`images/Extract_P1.tif`) and extracts the first band of the image into the variable `img`. The transformation matrix of the image is also stored.

3. **Labeling the Image**:
   - The `label` function from `skimage.measure` is used to label connected regions in the image. Each connected region is assigned a unique label.

4. **Preparing Data Structures**:
   - Several lists are initialized to store the results: `centerline_data` for centerline geometries, `width_data` for widths, and `centerlines` for geometries to be rasterized.

5. **Processing Each Region**:
   - The code iterates over each labeled region using `regionprops`.
   - For each region, the medial axis (skeleton) is computed using `medial_axis`, which also returns the distance transform.
   - The centerline of the region is computed as a `LineString` using `shapely.geometry.LineString`.
   - The maximum width along the centerline is calculated from the distance transform.
   - The centerline and width data are appended to their respective lists.
   - The centerline geometry is also added to the list for rasterization.

6. **Creating DataFrames**:
   - Two DataFrames are created from the lists: `df_centerline` for centerlines and `df_width` for widths.

7. **Converting to GeoDataFrame**:
   - The `df_centerline` DataFrame is converted to a GeoDataFrame `gdf_centerline` using `geopandas.GeoDataFrame`, with the centerline geometries.
   - The coordinate reference system (CRS) is set to EPSG:4326 (WGS 84), which can be replaced with the appropriate EPSG code if known.

8. **Saving to CSV**:
   - The GeoDataFrame and DataFrame are saved to CSV files (`centerlines.csv` and `widths.csv`).

9. **Rasterizing Centerlines**:
   - The centerlines are rasterized using `rasterio.features.rasterize`, creating a raster image of the centerlines with the same shape and transformation as the original image.

This code effectively processes an image to extract and analyze the centerlines and widths of labeled regions, saving the results in both vector (CSV) and raster formats. 

## Acknowledgement
I want to express our gratitude to the developers and contributors of the Medial Axis Transform and our script, dataset, tutorial, and example, which are hosted on GitHub at https://github.com/thapawan/Medial-Axis-Transform/tree/main. Additionally, we acknowledge the provision of the HYDRoSWOT data, accessible via https://www.arcgis.com/apps/dashboards/4b8f2ba307684cf597617bf1b6d2f85d. Finally, we are thankful to the GitHub repository https://github.com/briannapagan/get_river_width for its code and resources, which have significantly contributed to our research.

## Cite
THAPA P., Davis, L., Amanambu, A., LaFevor, M., Frame, J. (2025). Enhanced river planform analysis using deep learning and medial axis transform with Sentinel 1A imagery. Earth Surface Processes & Landforms 50: e7015B, https://doi.org/10.1002/esp.70158

## Contact
Open for collaboration and welcome any valuable feedback or suggestions for improvement. If you have any queries about the algorithm, open for discussion and contact:
pthapa2@crimson.ua.edu.

## Future work
Currently, it provides CSVs and raster (.tif) files. A further extension is available in the GitHub repository with the folder name of Modified Medial Axis Transform (MMAT).
