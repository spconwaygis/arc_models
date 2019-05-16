# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# shapes_folder_creation.py
# Created on: 2019-05-16 15:22:18.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: shapes_folder_creation <Project_QC_Folder> <Seamline_File> <Tile_Layout_File> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Script arguments
Project_QC_Folder = arcpy.GetParameterAsText(0)

Seamline_File = arcpy.GetParameterAsText(1)

Tile_Layout_File = arcpy.GetParameterAsText(2)

# Local variables:
Output_Folder = Project_QC_Folder
Folder_Name = "Shapes"
Output_Folder__2_ = Output_Folder
Output_Feature_Class__6_ = "Seamlines"
Output_Feature_Class__5_ = ""
Output_Feature_Class__8_ = "Tile_Layout"
Output_Feature_Class__7_ = ""

# Process: Create Folder
arcpy.CreateFolder_management(Project_QC_Folder, Folder_Name)

# Process: Create Folder (2)
arcpy.CreateFolder_management(Output_Folder, "Seams")

# Process: Copy Seamlines
arcpy.FeatureClassToFeatureClass_conversion(Seamline_File, Output_Folder__2_, Output_Feature_Class__6_, "", "", "")

# Process: Copy Tile_Layout
arcpy.FeatureClassToFeatureClass_conversion(Tile_Layout_File, Output_Folder, Output_Feature_Class__8_, "", "", "")
