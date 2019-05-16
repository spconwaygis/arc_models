# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# road_centerlines.py
# Created on: 2019-05-16 15:21:18.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: road_centerlines <Clip_Features> <Output_File_Location_Name> <Buffer_Distance> <Expression> 
# Description: 
# S1100-Primary Road
#  | S1200-Secondary Road
#  | S1400 -Local Neighborhood Road, Rural Road, City Street
#  | S1500-Vehicular Trail (4WD)
#  | S1630-Ramp
#  | S1640-Service Drive usually along a limited access highway
#  | S1710-Walkway/Pedestrian Trail
#  | S1720-Stairway
#  | S1730-Alley
#  | S1740-Private Road for service vehicles (logging, oil fields, ranches, etc.)
#  | S1750-Internal U.S. Census Bureau use
#  | S1780-Parking Lot Road
#  | S1820-Bike Path or Trail
#  | S1830-Bridle Path

# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
Clip_Features = arcpy.GetParameterAsText(0)

Output_File_Location_Name = arcpy.GetParameterAsText(1)
if Output_File_Location_Name == '#' or not Output_File_Location_Name:
    Output_File_Location_Name = "P:\\Projects\\Road_Centerlines\\Temp\\CENTERLINES_SELECT.shp" # provide a default value if unspecified

Buffer_Distance = arcpy.GetParameterAsText(2)
if Buffer_Distance == '#' or not Buffer_Distance:
    Buffer_Distance = "1 Meters" # provide a default value if unspecified

Expression = arcpy.GetParameterAsText(3)
if Expression == '#' or not Expression:
    Expression = "MTFCC IN ( 'S1100' , 'S1200' , 'S1400' , 'S1500' , 'S1630' , 'S1640' , 'S1710' , 'S1720' , 'S1730' , 'S1740' , 'S1750' , 'S1780' , 'S1820' , 'S1830' )" # provide a default value if unspecified

# Local variables:
Centerlines = "P:\\Projects\\Road_Centerlines\\Road_Centerlines.gdb\\Centerlines"
Output_Feature_Class = ""
File_Location_Name = "P:\\Projects\\Road_Centerlines\\Temp\\CENTERLINES_CLIP.shp"

# Process: Buffer
arcpy.Buffer_analysis(Clip_Features, Output_Feature_Class, Buffer_Distance, "FULL", "ROUND", "NONE", "", "PLANAR")

# Process: Clip
arcpy.Clip_analysis(Centerlines, Output_Feature_Class, File_Location_Name, "")

# Process: Select
arcpy.Select_analysis(File_Location_Name, Output_File_Location_Name, Expression)
