from shutil import copy
import arcpy


copy("P:/Projects/__ArcMap_Master_GDB_LYR/Master.mxd", arcpy.GetParameterAsText(0))
