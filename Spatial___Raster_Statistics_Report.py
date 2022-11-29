import arcpy
import xlwt
import os

raster_prop=['format','width','height','meanCellWidth','meanCellHeight','compressionType','pixelType','bandCount','noDataValue']
raster_title=['File','File Type','Width (px)','Height (px)','Width (GSD units)','Height (GSD units)','Pixel Width (GSD)','Pixel Height (GSD)', 'Compression','Bit Depth','# of Bands','No Data Value','Min X','Min Y','Max X','Max Y','MrSID Compression','MrSID Compression w/o Alpha']
spatref_prop_PCS=['name','projectionName','factoryCode','linearUnitName','metersPerUnit','falseEasting','falseNorthing','centralMeridian','standardParallel1','standardParallel2','latitudeOfOrigin']
spatref_prop_GCS=['name','factoryCode','angularUnitName','radiansPerUnit','primeMeridianName','datumName','spheroidName','semiMajorAxis','semiMinorAxis','flattening']
spatref_prop_VCS=['name','factoryCode','linearUnitName','direction','verticalShift','datumName']
PCS_title=['File','PCS','Projection','WKID','Linear Unit','Meters/Unit','False Easting','False Northing','Central Meridian','Standard Parallel 1','Standard Parallel 2','Latitude of Origin']
GCS_title=['File','GCS','WKID','Angular Units','Radians/Unit','Prime Meridian','Datum','Spheroid','Semimajor Axis','Semiminoraxis','Inverse Flattening']
VCS_title=['File','VCS','WKID','Linear Unit','Direction','Vertical Shift','Vertical Datum']
extent_title=['File','File Type','Min X','Min Y','Max X','Max Y']


directory=arcpy.GetParameterAsText(0)
ext=arcpy.GetParameterAsText(1)
recursive=arcpy.GetParameter(2)

wb=xlwt.Workbook()
if ext!='las' and ext!='LAS' and ext!='.las' and ext!='.LAS' and ext!='shp' and ext!='SHP' and ext!='.shp' and ext!='.SHP':
    sheet0=wb.add_sheet('File_Stats')
if ext=='las' or ext=='shp':
    sheet00=wb.add_sheet('File_Stats')
sheet1=wb.add_sheet(ext+'_PCS')
sheet2=wb.add_sheet(ext+'_GCS')
sheet3=wb.add_sheet(ext+'_VCS')
wbcol=0
wbrow=0

#Write excel headers
title_font=xlwt.Font()
title_font.bold=True
title_font.name='Consolas'
title_style=xlwt.XFStyle()
title_style.font=title_font
for i in range(len(PCS_title)):
    sheet1.write(wbrow,i,PCS_title[i],title_style)
for z in range(len(GCS_title)):
    sheet2.write(wbrow,z,GCS_title[z],title_style)
for o in range(len(VCS_title)):
    sheet3.write(wbrow,o,VCS_title[o],title_style)

if 'sheet0' in locals():
    for p in range(len(raster_title)):
        sheet0.write(wbrow,p,raster_title[p],title_style)
if 'sheet00' in locals():
    for aa in range(len(extent_title)):
        sheet00.write(wbrow,aa,extent_title[aa],title_style)

title_font=xlwt.Font()
title_font.bold=False
title_font.name='Consolas'
title_style=xlwt.XFStyle()
title_style.font=title_font

#Iterate through files of specified extention
if recursive==True:
    for path,subdir,files in os.walk(directory):
        for name in files:
            if name.endswith(ext):
                #Get the spatial reference of file
                projection0=[]
                projection_PCS=[]
                projection_GCS=[]
                projection_VCS=[]
                spatial_ref=arcpy.Describe(os.path.join(path,name)).spatialReference
                projection_PCS.append(name)
                projection_GCS.append(name)
                projection_VCS.append(name)

                #Add raster properties to a list
                if 'sheet0' in locals():
                    raster_ref=arcpy.Raster(os.path.join(path,name))
                    raster_info_lst=[]
                    raster_info_lst.append(name)
                    for r in range(len(raster_prop)):
                        raster_info_lst.append(str(getattr(raster_ref,raster_prop[r])))
                    bitdepth=raster_info_lst[7]
                    raster_info_lst[7]=bitdepth[1:]
                    raster_info_lst.append(str(arcpy.GetRasterProperties_management(os.path.join(path,name), "LEFT")))
                    raster_info_lst.append(str(arcpy.GetRasterProperties_management(os.path.join(path,name), "BOTTOM")))
                    raster_info_lst.append(str(arcpy.GetRasterProperties_management(os.path.join(path,name), "RIGHT")))
                    raster_info_lst.append(str(arcpy.GetRasterProperties_management(os.path.join(path,name), "TOP")))
                    if ext=='sid' or ext=='.sid' or ext=='SID' or ext=='.SID':
                        #Get SID compression ratio
                        os.system('P:/Ortho/programs/batches/NEW_Batches/geoexpress_info/mrsidgeoinfo.exe '+os.path.join(path,name)+' -log '+os.path.join(path,name)+'_SIDlog.txt')
                        sidlog=open(os.path.join(path,name)+'_SIDlog.txt','r')
                        for line in sidlog.readlines():
                            if line[0:6]=='  comp':
                                raster_info_lst.append(line[21:])
                            if line[0:6]=='    CR':
                                raster_info_lst.append(line[21:])
                        sidlog.close()
                        os.remove(os.path.join(path,name)+'_SIDlog.txt')
                    else:
                        raster_info_lst.append('N/A')
                        raster_info_lst.append('N/A')
                    if len(raster_info_lst)==15:
                        raster_info_lst.append('N/A')
                    #if ext=='ecw' or ext=='.ecw' or ext=='ECW' or ext=='.ECW':
                    #    #Get ECW compression ratio
                    #    os.system('P:\Ortho\gdal\bin\gdal\apps\303\gdalinfo '+os.path.join(path,name)+'>'+os.path.join(path,name)+'_ECWlog.txt')
                    #    ecwlog=open(os.path.join(path,name)+'_ECWlog.txt','r')
                    #    for line in sidlog.readlines():
                    #        if line[0:6]=='    CR':
                    #            raster_info_lst.append(line[21:])
                    #    ecwlog.close()
                    #    os.remove(os.path.join(path,name)+'_SIDlog.txt')
                    #else:
                    #    raster_info_lst.append('N/A')
                if 'sheet00' in locals():
                    extent_lst=[]
                    extent_lst.append(name)
                    extent_lst.append(arcpy.Describe(os.path.join(path,name)).dataType)
                    extent_ref=str(arcpy.Describe(os.path.join(path,name)).extent)
                    extent_ref_lst=extent_ref.split()
                    for ee in range(len(extent_ref_lst)):
                        extent_lst.append(extent_ref_lst[ee])


                #Add spatial ref to a list
                for x in range(len(spatref_prop_PCS)):
                    try:
                        projection_PCS.append(str(getattr(spatial_ref,spatref_prop_PCS[x])))
                    except AttributeError:
                        projection_PCS.append('Unknown')
                for l in range(len(spatref_prop_GCS)):
                    try:
                        projection_GCS.append(str(getattr(spatial_ref.GCS,spatref_prop_GCS[l])))
                    except AttributeError:
                        projection_GCS.append('Unknown')
                for m in range(len(spatref_prop_VCS)):
                    try:
                        projection_VCS.append(str(getattr(spatial_ref.VCS,spatref_prop_VCS[m])))
                    except AttributeError:
                        projection_VCS.append('Unknown')
    
                if projection_VCS[4]=='1':
                    projection_VCS[4]='Up'
                if projection_VCS[4]=='0':
                    projection_VCS[4]='Down'
        
                wbrow+=1
                #Write file raster info to excel spreadsheet
                if 'sheet0' in locals():
                    sheet0.write(wbrow,0,raster_info_lst[0],title_style)
                    sheet0.write(wbrow,1,raster_info_lst[1],title_style)
                    sheet0.write(wbrow,2,raster_info_lst[2],title_style)
                    sheet0.write(wbrow,3,raster_info_lst[3],title_style)
                    sheet0.write(wbrow,4,str(float(raster_info_lst[2])*float(raster_info_lst[4])),title_style)
                    sheet0.write(wbrow,5,str(float(raster_info_lst[3])*float(raster_info_lst[5])),title_style)

                    for s in range(len(raster_info_lst)-4):
                        sheet0.write(wbrow,s+6,raster_info_lst[s+4],title_style)

                if 'sheet00' in locals():
                    for cc in range(len(extent_title)):
                        sheet00.write(wbrow,cc,extent_lst[cc],title_style)

                #Write file spatial ref to excel spreadsheet
                for j in range(len(projection_PCS)):
                    sheet1.write(wbrow,j,projection_PCS[j],title_style)
                for k in range(len(projection_GCS)):
                    sheet2.write(wbrow,k,projection_GCS[k],title_style)
                for n in range(len(projection_VCS)):
                    sheet3.write(wbrow,n,projection_VCS[n],title_style)
            else:
                continue
else:
    for files in os.listdir(directory):
    
        if files.endswith(ext):
            #Get the spatial reference of file
            projection0=[]
            projection_PCS=[]
            projection_GCS=[]
            projection_VCS=[]
            spatial_ref=arcpy.Describe(directory+'/'+files).spatialReference
            projection_PCS.append(files)
            projection_GCS.append(files)
            projection_VCS.append(files)

            #Add raster properties to a list
            if 'sheet0' in locals():
                raster_ref=arcpy.Raster(directory+'/'+files)
                raster_info_lst=[]
                raster_info_lst.append(files)
                for r in range(len(raster_prop)):
                    raster_info_lst.append(str(getattr(raster_ref,raster_prop[r])))
                bitdepth=raster_info_lst[7]
                raster_info_lst[7]=bitdepth[1:]
                raster_info_lst.append(str(arcpy.GetRasterProperties_management(directory+'/'+files, "LEFT")))
                raster_info_lst.append(str(arcpy.GetRasterProperties_management(directory+'/'+files, "BOTTOM")))
                raster_info_lst.append(str(arcpy.GetRasterProperties_management(directory+'/'+files, "RIGHT")))
                raster_info_lst.append(str(arcpy.GetRasterProperties_management(directory+'/'+files, "TOP")))
                if ext=='sid' or ext=='.sid' or ext=='SID' or ext=='.SID':
                    #Get SID compression ratio
                    os.system('P:/Ortho/programs/batches/NEW_Batches/geoexpress_info/mrsidgeoinfo.exe '+directory+'/'+files+' -log '+directory+'/'+files+'_SIDlog.txt')
                    sidlog=open(directory+'/'+files+'_SIDlog.txt','r')
                    for line in sidlog.readlines():
                        if line[0:6]=='    CR':
                            raster_info_lst.append(line[21:])
                        if line[0:6]=='  comp':
                            raster_info_lst.append(line[21:])
                    sidlog.close()
                    os.remove(directory+'/'+files+'_SIDlog.txt')
                else:
                    raster_info_lst.append('N/A')
                    raster_info_lst.append('N/A')
                if len(raster_info_lst)==15:
                    raster_info_lst.append('N/A')
            if 'sheet00' in locals():
                extent_lst=[]
                extent_lst.append(files)
                extent_lst.append(arcpy.Describe(directory+'/'+files).dataType)
                extent_ref=str(arcpy.Describe(directory+'/'+files).extent)
                extent_ref_lst=extent_ref.split()
                for ff in range(len(extent_ref_lst)):
                    extent_lst.append(extent_ref_lst[ff])

            #Add spatial ref to a list
            for x in range(len(spatref_prop_PCS)):
                try:
                    projection_PCS.append(str(getattr(spatial_ref,spatref_prop_PCS[x])))
                except AttributeError:
                    projection_PCS.append('Unknown')
            for l in range(len(spatref_prop_GCS)):
                try:
                    projection_GCS.append(str(getattr(spatial_ref.GCS,spatref_prop_GCS[l])))
                except AttributeError:
                    projection_GCS.append('Unknown')
            for m in range(len(spatref_prop_VCS)):
                try:
                    projection_VCS.append(str(getattr(spatial_ref.VCS,spatref_prop_VCS[m])))
                except AttributeError:
                    projection_VCS.append('Unknown')
    
            if projection_VCS[4]=='1':
                projection_VCS[4]='Up'
            if projection_VCS[4]=='0':
                projection_VCS[4]='Down'
        
            wbrow+=1
            #Write file raster info to excel spreadsheet
            if 'sheet0' in locals():
                sheet0.write(wbrow,0,raster_info_lst[0],title_style)
                sheet0.write(wbrow,1,raster_info_lst[1],title_style)
                sheet0.write(wbrow,2,raster_info_lst[2],title_style)
                sheet0.write(wbrow,3,raster_info_lst[3],title_style)
                sheet0.write(wbrow,4,str(float(raster_info_lst[2])*float(raster_info_lst[4])),title_style)
                sheet0.write(wbrow,5,str(float(raster_info_lst[3])*float(raster_info_lst[5])),title_style)

                for s in range(len(raster_info_lst)-4):
                    sheet0.write(wbrow,s+6,raster_info_lst[s+4],title_style)

            if 'sheet00' in locals():
                for cc in range(len(extent_title)):
                    sheet00.write(wbrow,cc,extent_lst[cc],title_style)

            #Write file spatial ref to excel spreadsheet
            for j in range(len(projection_PCS)):
                sheet1.write(wbrow,j,projection_PCS[j],title_style)
            for k in range(len(projection_GCS)):
                sheet2.write(wbrow,k,projection_GCS[k],title_style)
            for n in range(len(projection_VCS)):
                sheet3.write(wbrow,n,projection_VCS[n],title_style)
        else:
            continue

if 'sheet0' in locals():
    sheet0.col(0).width=400*len(raster_info_lst[0])
    sheet0.col(1).width=280*len(raster_title[1])
    if len(raster_title[2])<len(raster_info_lst[2]):
        sheet0.col(2).width=280*len(raster_info_lst[2])
    else:
        sheet0.col(2).width=280*len(raster_title[2])
    if len(raster_title[3])<len(raster_info_lst[3]):
        sheet0.col(3).width=280*len(raster_info_lst[3])
    else:
        sheet0.col(3).width=280*len(raster_title[3])
    if len(raster_title[4])<len(str(float(raster_info_lst[2])*float(raster_info_lst[4]))):
        sheet0.col(4).width=280*len(str(float(raster_info_lst[2])*float(raster_info_lst[4])))
    else:
        sheet0.col(4).width=280*len(raster_title[4])
    if len(raster_title[5])<len(str(float(raster_info_lst[3])*float(raster_info_lst[5]))):
        sheet0.col(5).width=280*len(str(float(raster_info_lst[3])*float(raster_info_lst[5])))
    else:
        sheet0.col(5).width=280*len(raster_title[5])

    
    for t in range(len(raster_title)-6):
        if len(raster_title[t+6])<len(raster_info_lst[t+4]):
            sheet0.col(t+6).width=280*len(raster_info_lst[t+4])
        else:
            sheet0.col(t+6).width=280*len(raster_title[t+6])
if 'sheet00'in locals():
    for dd in range(len(extent_title)):
        if len(extent_title[dd])<len(extent_lst[dd]):
            sheet00.col(dd).width=280*len(extent_lst[dd])
        else:
            sheet00.col(dd).width=280*len(extent_title[dd])   
for v in range(len(PCS_title)):
    if len(PCS_title[v])<len(projection_PCS[v]):
        sheet1.col(v).width=280*len(projection_PCS[v])
    else:
        sheet1.col(v).width=280*len(PCS_title[v])   
for w in range(len(GCS_title)):
    if len(GCS_title[w])<len(projection_GCS[w]):
        sheet2.col(w).width=280*len(projection_GCS[w])
    else:
        sheet2.col(w).width=280*len(GCS_title[w]) 
for y in range(len(VCS_title)):
    if len(VCS_title[y])<len(projection_VCS[y]):
        sheet3.col(y).width=280*len(projection_VCS[y])
    else:
        sheet3.col(y).width=280*len(VCS_title[y]) 

if 'sheet0' in locals():
    wb.save(directory+'/ArcPro_'+ext+'_Raster_Info_Spatial_Stats_'+time.strftime('%Y%m%d')+'_'+time.strftime('%H%M%S')+'.xls')
else:
    wb.save(directory+'/ArcPro_'+ext+'_Spatial_Stats_'+time.strftime('%Y%m%d')+'_'+time.strftime('%H%M%S')+'.xls')

#if 'sheet0' in locals():
#    os.startfile(directory+'/ArcPro_'+ext+'_Raster_Info_Spatial_Stats_'+time.strftime('%Y%m%d')+'_'+time.strftime('%H%M%S')+'.xls')
#else:
#    os.startfile(directory+'/ArcPro_'+ext+'_Spatial_Stats_'+time.strftime('%Y%m%d')+'_'+time.strftime('%H%M%S')+'.xls')