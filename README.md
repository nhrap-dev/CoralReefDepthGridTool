## To Do
- clean up readme
- test output in coastal flood hazard in hazus
- run all return periods for all locations
- Enhance with elevation (add depth to DEM 10m to equal water surface; create IDW from water surface; subtract DEM from water surface IDW (positve points are flooded))

# Coral Reef Depth Grid Tool
description goes here

## Requirements

The Coral Reef Depth Grid Tool requires ArcGIS 10.5.1 and python 2.7

## To Use

1. Download zip folder of tool from GitHub, unzip

2. Open the .py file with IDLE or a text editor and then modify the following variables to match your machine:
	- arcpy.env.workspace = r"C:\temp\ScratchCoral" #set to where you want the output depthgrids (.tif) to be saved at
	- Folder = r"C:\Users\Clindeman\OneDrive - niyamit.com\CoralReef\Data\USGS" #change this to your directory
	- LocationList =['AmericanSamoa','CNMI','Florida','Guam','HawaiianIslands','PuertoRico','USVI'] #full list
	- ReturnPeriodList = ['rp10','rp50','rp100','rp500'] #full list
3. Run the script within IDLE to see the output statements and if there are any issues with the data

## Documentation
	USGS Data
		https://www.sciencebase.gov/catalog/item/5bd77b33e4b0b3fc5ce825d8
		Shapefiles for seven areas:
			USVI 		WGS_1984_UTM_Zone_20N
			Puerto Rico 	WGS_1984_UTM_Zone_20N
			Guam 		WGS_1984_UTM_Zone_55n
			CNMI		WGS_1984_UTM_Zone_55n
			Am Samoa	WGS_1984_UTM_Zone_2S
			Florida		WGS_1984_UTM_Zone_17N
			Hawaii		WGS_1984_UTM_Zone_4N
			
Issues with the source USGS data (downloaded on 2020-12-03):
* "HawaiianIslands_floodpoints.shp" has scenario "Molokai_rp100_wrfcsv_floodpoints", it should not have the 'csv' in it
* "USVI_floodmasks.shp" has field 'ShpName', it should be 'MaskName'

## Contact

Issues can be reported through the repository on Github (https://github.com/nhrap-dev/CoralReefDepthGridTool)

For questions contact hazus-support@riskmapcds.com
