'''20201130 Colin Lindeman Niyamit
ArcGIS 10.5.1, Python 2.7

Change the following lines to be specific to your machine and file location:
1) arcpy.env.workspace = r"C:\temp\ScratchCoral"
2) Folder = r"C:\Users\Clindeman\OneDrive - niyamit.com\CoralReef\Data\USGS"
3) inFloodPoints = os.path.join(Folder, r'Florida_floodpoints\Florida_floodpoints.shp')
4) inFloodMask = os.path.join(Folder, r'Florida_floodmasks\Florida_floodmasks.shp')
5) RPList = ['rp100'] #define your list

Known issues with the data circa 20201203:
-"Molokai_rp100_wrfcsv_floodpoints" should have the 'csv' removed after 'wrf'.
'''

print("Start")

#IMPORTS
import arcpy
from arcpy import env
from arcpy.sa import *
import os


#SETTINGS
arcpy.CheckOutExtension("Spatial")
arcpy.env.scratchWorkspace = r"in_memory"
arcpy.env.workspace = r"C:\temp\ScratchCoral" #set to where you want the output depthgrids (.tif) to be saved at
arcpy.env.overwriteOutput = True


#FUNCTIONS
def unique_values(table, field):  ##uses list comprehension
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

    
#INPUTS
#Input for arctoolbox operation
##inFloodPoints = arcpy.GetParameterAsText(1)
##inFloodPointsScenarioField = arcpy.GetParameterAsText(2)
##inFloodMask = arcpy.GetParameterAsText(3)
##inFloodMaskScenarioField = arcpy.GetParameterAsText(4)
##outGrid = arcpy.GetParameterAsText(5)

#Input for manual operation
Folder = r"C:\Users\Clindeman\OneDrive - niyamit.com\CoralReef\Data\USGS"

#inFloodPoints = os.path.join(Folder, r'HawaiianIslands_floodpoints\HawaiianIslands_floodpoints.shp')
inFloodPoints = os.path.join(Folder, r'Florida_floodpoints\Florida_floodpoints.shp')
inFloodPointsScenarioField = 'Scenario'

#inFloodPoints = os.path.join(Folder, r'HawaiianIslands_floodmasks\HawaiianIslands_floodmasks.shp')
inFloodMask = os.path.join(Folder, r'Florida_floodmasks\Florida_floodmasks.shp')
inFloodMaskScenarioField = 'MaskName'

#Return Periods to create depth grids (IDW raster)
#RPList = ['rp10','rp50','rp100','rp500'] #full list
RPList = ['rp100'] #define your list


#PROCESS
#generate a list of scenarios...
scenariosPoints = unique_values(inFloodPoints,inFloodPointsScenarioField)
scenariosMask = unique_values(inFloodMask,inFloodMaskScenarioField)
#Check if scenarios match and if they do create an IDW raster...
mergedList = tuple(zip(sorted(scenariosPoints), sorted(scenariosMask)))
for x in mergedList:
        y = x[0].split("_")#check if return period is in RPList
        if y[1] in RPList:
            x0 = x[0].replace("_floodpoints","")
            x1 = x[1].replace("_floodmask","")
            '''Maui_rp100_wrf_floodmask != Maui_rp100_wrf_floodpoints
               Maui_rp100_wrf == Maui_rp100_wrf'''
            
            if x0 <> x1:
                print("NO Match",x0,x1)
                
            elif x0 == x1:
                print("Match",x0,x1)
                PointsLayer = x0 + "PLayer"
                MaskLayer = x1 + "MLayer"
                IDWGrid = x0 + ".tif" #grid format is failing, error 010240
                
                #iterate over each scenario, filtering the data and generating a depth grid with IDW...
                print("Make PointsLayer", x[0], PointsLayer)
                inFloodPointsWhereClause = '"' + inFloodPointsScenarioField + '"' + "= '" + x[0] + "'"
                arcpy.MakeFeatureLayer_management(inFloodPoints, PointsLayer, inFloodPointsWhereClause)

                print("Make MaskLayer", x[1], MaskLayer)
                inFloodMaskWhereClause = '"' + inFloodMaskScenarioField + '"' + "= '" + x[1] + "'"
                arcpy.MakeFeatureLayer_management(inFloodMask, MaskLayer, inFloodMaskWhereClause)    

                try:
                    arcpy.env.mask = MaskLayer
                    zField = "F_Depth" #Sould check that this exists/matches first
                    cellSize = 30
                    power = 2
                    searchRadius = RadiusVariable(10, 150000)
                    print("IDW", IDWGrid)
                    outIDW = Idw(PointsLayer, zField, cellSize, power, searchRadius)
                    
                    print("Save IDW")
                    outIDW.save(IDWGrid) #should build pyramids, stats
                except Exception as (e):
                    print(e)
                arcpy.management.Delete(PointsLayer)
                arcpy.management.Delete(MaskLayer)
                
            else:
                pass
            print("")

print("Done")
