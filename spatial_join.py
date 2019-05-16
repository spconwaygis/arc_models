import arcpy  
  
# Manually specify the desired fieldnames here  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
outputFields = ("Name","Path","PID","Error_Path")  
  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
#Get input parameters from user/model   
targetFeature = arcpy.GetParameterAsText(0)  
joinFeature = arcpy.GetParameterAsText(1)  
outputFeature = arcpy.GetParameterAsText(2)  
  
#Create Fieldmappings and add tables from input  
tempMappings = arcpy.FieldMappings()  
tempMappings.addTable(targetFeature)  
tempMappings.addTable(joinFeature)  
  
#Create new fieldmappings using the listed fields, from the current(temp) fieldmappings.    
fieldMappings = arcpy.FieldMappings()  
for field in outputFields:  
    fieldMappings.addFieldMap(tempMappings.getFieldMap(tempMappings.findFieldMapIndex(field)))  
  
#Process: Spatial Join  
#(note: you can change how the join works on this line)  
arcpy.SpatialJoin_analysis(targetFeature, joinFeature, outputFeature, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldMappings, "HAVE_THEIR_CENTER_IN")  
