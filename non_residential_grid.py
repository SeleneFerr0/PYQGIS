#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Input - fin_grid.shp
Output  - fin_base.shp

carved out:

1, big rivers
2, grid_ids that have been marked as non-residential

'''
import itertools as iter
import pandas as pd
import numpy as np
import re
import string
import processing
import os
import shutil
import shapely
import json
import urllib
import math
from qgis.core import *
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QColor
from qgis.core import QgsMapLayerRegistry, QgsVectorJoinInfo
from qgis.core import QgsMessageLog

def count_unique_poi2(filename, polygon,  points, alg="qgis:countuniquepointsinpolygon", save=False):
    
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == False:
        count_unique =  processing.runalg(alg, polygon, points, 'POI_ID', 'Resident',  None)
        return processing.getObject(count_unique['OUTPUT'])
    else:
        processing.runalg(alg, polygon, points, 'POI_ID', 'Resident',  save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name,  provider_name)

def union_load(filename, layer1, layer2, alg="qgis:union", save=False):
    '''
    #This is a warpper-function for "union"
    '''
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save == False:
        union = processing.runalg(alg, layer1, layer2, None)
        return processing.getObject(union['OUTPUT'])
    else:
        processing.runalg(alg, layer1, layer2, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

def count_unique_poi(filename, polygon,  points, alg="qgis:countuniquepointsinpolygon", save=False):
    
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == False:
        count_unique =  processing.runalg(alg, polygon, points, 'POIID', 'NUMPOINTS',  None)
        return processing.getObject(count_unique['OUTPUT'])
    else:
        processing.runalg(alg, polygon, points, 'POIID', 'NUMPOINTS',  save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name,  provider_name)

def clip_load(filename, layer1, layer2, alg="qgis:clip", save=False) :
    '''
    #This is a warpper-function for "clip"
    #if save =False， the output will be kept only in memory
    #if save =True，  the output will be saved to OutputFile and added to the current panel
    '''
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == True:
        processing.runalg(alg, layer1, layer2, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)        
        
    else:
        clip = processing.runalg(alg, layer1, layer2, None)
        return processing.getObject(clip['OUTPUT'])

def clip_saga(filename, layer1, layer2, alg="saga:polygonclipping", save=False) :
    '''
    #This is a warpper-function for "clip"
    #if save =False， the output will be kept only in memory
    #if save =True，  the output will be saved to OutputFile and added to the current panel
    '''
    global OutputFile2
    save_name = OutputFile2 + filename + ".shp"
    
    if save == True:
        processing.runalg(alg, layer1, layer2, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)        
        
    else:
        clip = processing.runalg("qgis:clip", layer2, layer1, None)
        return processing.getObject(clip['OUTPUT'])

def remove_null_load(filename, layer1, alg="qgis:removenullgeometries", save=False):
    '''
    #This is a warpper-function for "remove_null_geometries"
    '''
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save == False:
        remove = processing.runalg(alg, layer1, None)
        return processing.getObject(remove['OUTPUT_LAYER'])
    else:
        processing.runalg(alg, layer1, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)
        

def dsv_load(filename, layer, field="new_id",alg="qgis:dissolve", save=False) :
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == True:
        processing.runalg(alg, layer, 0, field, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)        
        
    else:
        clip = processing.runalg(alg, layer, 0, field, None)
        return processing.getObject(clip['OUTPUT'])

def area_cal(filename, layer, alg="qgis:fieldcalculator", save=False):
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save == True:
        processing.runalg(alg, layer,"area",0,10,2,True,"$area/1000000",save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)        
        
    else:
        area = processing.runalg(alg, layer,"area",0,10,2,True,"$area/1000000", None)
        return processing.getObject(area['OUTPUT'])
    

def difference_load(filename, layer1, layer2, alg="qgis:difference", save=False) :
    '''
    #This is a warpper-function for "difference"
    '''
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == True:
        if int(layer2.featureCount())>0:
             processing.runalg(alg, layer1, layer2, True, save_name)
             data_source = save_name
             layer_name = filename
             provider_name = "ogr"
             return iface.addVectorLayer(data_source, layer_name, provider_name)
        else:
             processing.runalg('qgis:clip', layer1, layer1, save_name)
             data_source = save_name
             layer_name = filename
             provider_name = "ogr"
             return iface.addVectorLayer(data_source, layer_name, provider_name)    
    else:
        if int(layer2.featureCount())>0:
            diff = processing.runalg(alg, layer1, layer2, True, None)
        else:
            diff = processing.runalg('qgis:clip', layer1, layer1, None)
        return processing.getObject(diff['OUTPUT'])

def difference_saga(filename, layer1, layer2, alg="saga:difference", save=False) :
    '''
    #This is a warpper-function for "difference"
    '''
    global OutputFile2
    save_name = OutputFile2 + filename + ".shp"
    
    if save == True:
        if int(layer2.featureCount())>0:
             processing.runalg(alg, layer1, layer2, 1, save_name)
             data_source = save_name
             layer_name = filename
             provider_name = "ogr"
             return iface.addVectorLayer(data_source, layer_name, provider_name)
        else:
             processing.runalg('saga:polygonclipping', layer1, layer1, save_name)
             data_source = save_name
             layer_name = filename
             provider_name = "ogr"
             return iface.addVectorLayer(data_source, layer_name, provider_name)    
    else:
        if int(layer2.featureCount())>0:
            diff = processing.runalg('qgis:difference', layer1, layer2, True, None)
        else:
            diff = processing.runalg('qgis:clip', layer1, layer1, None)
        return processing.getObject(diff['OUTPUT'])

def multi_single(filename, layer, alg="qgis:multiparttosingleparts", save=False):
    global OutputFile2
    save_name = OutputFile + filename + ".shp"
    if save == False:
        result = processing.runalg(alg, layer, None)
        return processing.getObject(result['OUTPUT'])
    else:
        processing.runalg(alg, layer, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

def join_load(filename, layer1, layer2,  predicate, alg='qgis:joinattributesbylocation', save=False):
    '''
    #This is a warpper-function for "join"
    '''
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == False:
        join = processing.runalg(alg, layer1, layer2, predicate, 0, 0, 'sum', 0, None)
        return processing.getObject(join['OUTPUT'])
    else:
        processing.runalg(alg, layer1, layer2, predicate, 0, 0, 'sum', 0, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

def find_neighbor(layer):
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        index.insertFeature(f)
    layer.startEditing()
    for f in feature_dict.values():
        geom = f.geometry()
        intersecting_ids = index.intersects(geom.boundingBox())
        neighbors = []
        north =[]
        south =[]
        east =[]
        west =[]
        neighbors_sum = 0
        a = f['id2']
        for intersecting_id in intersecting_ids:
            intersecting_f = feature_dict[intersecting_id]
            # For our purpose we consider a feature as 'neighbor' if it touches or intersects a feature. We use the 'disjoint' predicate to satisfy
            if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
                neighbors.append(intersecting_f[_NAME_FIELD])
                if(intersecting_f["xmin"]==f["xmin"] and intersecting_f["ymin"]==f["ymax"]):
                    north.append(intersecting_f[_NAME_FIELD])
                elif(intersecting_f["xmin"]==f["xmin"] and intersecting_f["ymax"]==f["ymin"]):
                    south.append(intersecting_f[_NAME_FIELD])
                elif(intersecting_f["ymin"]==f["ymin"] and intersecting_f["xmin"]==f["xmax"]):
                    west.append(intersecting_f[_NAME_FIELD])
                elif(intersecting_f["ymin"]==f["ymin"] and intersecting_f["xmax"]==f["xmin"]):
                    east.append(intersecting_f[_NAME_FIELD])
        f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
        f[_NEW_NORTH] = ','.join(north)
        f[_NEW_SOUTH] = ','.join(south)
        f[_NEW_SUM_FIELD] = len(neighbors)
        f[_NEW_LEFT] = ','.join(east)
        f[_NEW_RIGHT] = ','.join(west)
        f[_NEW_ID] =f["id2"]
        # Update the layer with new attribute values.
        layer.updateFeature(f)
    layer.commitChanges()


def merge_grid(filename, layer, exp =u'"left_grid"is null', id="right_grid", thresh=0.33, save=False):
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save==False:
        processing.runalg("qgis:selectbyattribute", layer, u'area', 4, thresh)
        processing.runalg("qgis:selectbyexpression", layer, exp, 3)
        feature_dict = {f.id(): f for f in layer.selectedFeatures()}
        layer.startEditing()
        for f in feature_dict.values():
            geom = f.geometry()
            new = f[id]
            f[_NEW_ID] = new
            layer.updateFeature(f)
        layer.commitChanges()
        layer.removeSelection()
        layer2 = dsv_load(filename, layer)
        layer3= area_cal(filename, layer2)
        layer.removeSelection()
        return processing.getObject(layer3['OUTPUT'])
    else:
        processing.runalg("qgis:selectbyattribute", layer, u'area', 4, thresh)
        processing.runalg("qgis:selectbyexpression", layer, exp, 3)
        feature_dict = {f.id(): f for f in layer.selectedFeatures()}
        layer.startEditing()
        for f in feature_dict.values():
            geom = f.geometry()
            new = f[id]
            layer.updateFeature(f)
        layer.commitChanges()
        layer.removeSelection()
        layer2 = dsv_load(filename, layer)
        processing.runalg("qgis:fieldcalculator", layer2,"area",0,10,2,True,"$area/1000000",save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)  

def convert_polygon(filename, layer, alg="qgis:convertgeometrytype", save=False):
    global OutputFile2
    save_name = OutputFile2 + filename + ".shp"
    if save == False:
        remove = processing.runalg(alg, layer, 4, None)
        return processing.getObject(remove['OUTPUT_LAYER'])
    else:
        processing.runalg(alg, layer, 4, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

def check_validity(filename1, filename2, layer, alg="qgis:checkvalidity", save=False):
    global OutputFile
    save_name1 = OutputFile + filename1 + ".shp"
    save_name2 = OutputFile + filename2 + ".shp"
    if save == False:
        remove = processing.runalg(alg, layer, 0, None, None, None)
        return processing.getObject(remove['VALID_OUTPUT'])
    else:
        processing.runalg(alg, layer, 0, save_name1, save_name2, None)
        data_source = save_name1
        layer_name = filename1
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

path2 = 'C:\\Users\\base7005\\Documents\\CityBoundary\\result\\done'
bau_path = 'C:\\Users\\base7005\\Documents\\QGISimport\\batch1-3\\'
#Residential_path = "C:\\Users\\base7005\\Documents\\QGISimport\\Residential\\Liaoning\\"
cce_path = 'C:\\Users\\base7005\\Documents\\CCE blocks\\kml\\'


df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\QGISimport\\map_file.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_})
#df_selected = pd.read_excel('C:\\Users\\base7005\\Documents\\CityBoundary\\Block_selection_Batch12.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'grid_id': np.str_, 'AD_CODE':np.str_})
df_nopeople = pd.read_excel('C:\\Users\\base7005\\Documents\\CityBoundary\\nopeople_grid\\GRID_nonresidential.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'GRID_ID': np.str_})
df_nopeople= df_nopeople.sort_values(by=['AD_CODE', 'GRID_ID'], ascending=[True, True])
df_nopeople = df_nopeople[~df_nopeople.GRID_ID.duplicated(keep='first')]


river_path = 'C:\\Users\\base7005\\Documents\\QGISimport\\Waters\\big_rivers.shp'
change_city = pd.read_excel('C:\\Users\\base7005\\Documents\\CCE blocks\\ccecities0911.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_})
keep_list = change_city[change_city['fin'] ==0]
keep_list = keep_list.citycode.tolist()

global path, OutputFile
#path = 'C:\\Users\\base7005\\Documents\\QGISimport\\result\\batch3_1-6 rerun\\batch3_1\\广东省\\'
path = 'C:\\Users\\base7005\\Documents\\CityBoundary\\test\\江苏省\\'
path = path.decode('utf-8')
files = os.listdir(path)

special_list = ['231182', '231086', '231025', '232721']

for file in files:
    
    province = path[-4:-1]
    city=file.split("_",1)[0]
    dist = file.split("_",1)[1][:-7]
    AD_CODE = file[-6:]
    print(province + " " + city + " " + dist)
    OutputFile = path + file +'\\'
    OutputFile2 = path2 + '\\'
    citycode = df_map.loc[df_map['ADCODE']==int(AD_CODE),'citycode']
    #batch = df_map.loc[(df_map['PROVINCENA']==province) & (df_map['CITYNAME'] ==city) &(df_map['COUNTYNAME']==dist),'Batch']
    batch = df_map.loc[df_map['ADCODE']==int(AD_CODE),'Batch']
    batch = int(batch)
    citycode = int(citycode)
    citycode =str(citycode).zfill(4)
    
    '''original fin grid'''
    if batch ==3:
        layer_fin_grid = QgsVectorLayer(OutputFile + 'fin_grid.shp','fin_grid', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_fin_grid)
        layer_fin_grid = iface.activeLayer()
        layer_fin_grid.setCrs(QgsCoordinateReferenceSystem(4030))
    elif batch ==1 or batch==2:
        layer_fin_grid = QgsVectorLayer(OutputFile + 'resident_grid.shp','resident_grid', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_fin_grid)
        layer_fin_grid = iface.activeLayer()
        layer_fin_grid.setCrs(QgsCoordinateReferenceSystem(4030))
    
    layer_bau_dsv = QgsVectorLayer(bau_path + 'Batch' + str(batch)+'_city_d.shp',  'Batch' + str(batch)+'_city_d', 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(layer_bau_dsv)
    layer_bau_dsv= iface.activeLayer()
    layer_bau_dsv.setCrs(QgsCoordinateReferenceSystem(4030))
    
    layer_fin1 = difference_load("fin_grid_base", layer_fin_grid, layer_bau_dsv)
    QgsMapLayerRegistry.instance().removeMapLayers( [layer_bau_dsv.id(), layer_fin_grid.id()])
    layer_fin2 = remove_null_load("fin_grid_2", layer_fin1, save=True)
    #    '''CCE blocks'''
    #    if os.path.isfile(cce_path + str(citycode) + '\\' + str(citycode) + '_dsv.shp'):
    #        data_source = cce_path + str(citycode) + '\\' + str(citycode) + '_dsv.shp'
    #        layer_name =str(citycode) + '_dsv'
    #        provider_name = "ogr"
    #        layer_cce_block = iface.addVectorLayer(data_source, layer_name, provider_name)
    #        layer_cce_block.setCrs(QgsCoordinateReferenceSystem(4030))
    #    else:
    #        print('for ' + str(citycode) + ' , CCE city file not found')
    if citycode in keep_list:
        '''carve out special grids'''
        if AD_CODE in special_list:
            df_ori_grid = pd.read_excel(OutputFile + 'Result_grid_' + str(AD_CODE) + 'xlsx',sheetname="Sheet1",encoding='gb18030')
            df_ori_grid.set_index('fin_id')
        else:
            df_ori_grid = pd.DataFrame.from_csv(OutputFile + "Result_Grid2.csv", index_col='fin_id')
        df_ori_grid[['areapl']] = df_ori_grid[['areapl']].fillna(value=0)
        #df_ori_grid.loc[(df_ori_grid['NUMPOINTS']==0) & (df_ori_grid['Resident']==0) & (df_ori_grid['areapl'] <0.03), 'Nopeople'] = 1
        
        df_selected = df_nopeople[df_nopeople.AD_CODE == int(AD_CODE)]
        if len(df_selected) >0:
            lst = df_selected.grid_id.tolist()
            layer_selected_grid=QgsVectorLayer("Polygon", "selected_grid", "memory")
            for i in lst:
                processing.runalg("qgis:selectbyattribute", layer_fin2, u'grid_id', 0, str(i))
                feature = layer_fin2.selectedFeatures()
                temp_data=layer_selected_grid.dataProvider()
                attr=layer_fin2.dataProvider().fields().toList()
                temp_data.addAttributes(attr)
                temp_data.addFeatures(feature)
                layer_selected_grid.updateFields()
                QgsMapLayerRegistry.instance().addMapLayer(layer_selected_grid)
                layer_fin2.removeSelection()
            
            save_name = OutputFile+"special_grid_"+str(AD_CODE)+".shp"
            QgsVectorFileWriter.writeAsVectorFormat(layer_selected_grid, save_name, "utf-8", None, "ESRI Shapefile")
            data_source = save_name
            layer_name = "special_grid_"+str(AD_CODE)+".shp"
            provider_name = "ogr"
            layer_selected_grid =iface.addVectorLayer(data_source, layer_name, provider_name)
        
        layer_fin6 = difference_load("fin_base", layer_fin2, layer_selected_grid)
        layer_fin7 = remove_null_load("fin_" + str(AD_CODE), layer_fin6)
        
        data_source = river_path
        layer_name ="big_rivers"
        provider_name = "ogr"
        layer_Rivers = iface.addVectorLayer(data_source, layer_name, provider_name)
        layer_Rivers.setCrs(QgsCoordinateReferenceSystem(4030))
        
        layer_fin3 = difference_saga("fin_grid_base", layer_fin7, layer_Rivers)
        
        '''Load target nopeople1 - farmland, forest'''
        layer_nopeople1= QgsVectorLayer(OutputFile + 'target_NoPeople1.shp', 'target_NoPeople1', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_nopeople1)
        layer_nopeople1 = iface.activeLayer()
        layer_nopeople1.setCrs(QgsCoordinateReferenceSystem(4030))
        
        layer_fin4 = difference_saga("fin_grid_base", layer_fin3, layer_nopeople1)
        layer_fin5 = remove_null_load("fin_grid5", layer_fin4)
        layer_fin8 = multi_single("fin_base", layer_fin5,save=True)
        
        QgsMapLayerRegistry.instance().removeMapLayers( [layer_Rivers.id()])
        
        layer_base = area_cal("fin_base", layer_fin8, save=True)
        with edit(layer_base):
            request = QgsFeatureRequest().setFilterExpression('"area"<0.01')
            request.setSubsetOfAttributes([])
            request.setFlags(QgsFeatureRequest.NoGeometry)
            for f in layer_base.getFeatures(request):
                layer_base.deleteFeature(f.id())
        
    else:
        print(str(citycode) + '-' + str(AD_CODE) + ' does not have grid to set aside')
        
        data_source = river_path
        layer_name ="big_rivers"
        provider_name = "ogr"
        layer_Rivers = iface.addVectorLayer(data_source, layer_name, provider_name)
        layer_Rivers.setCrs(QgsCoordinateReferenceSystem(4030))
        
        layer_fin3 = difference_saga("fin_grid_base", layer_fin2, layer_Rivers)
        
        '''Load target nopeople1 - farmland, forest'''
        layer_nopeople1= QgsVectorLayer(OutputFile + 'target_NoPeople1.shp', 'target_NoPeople1', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_nopeople1)
        layer_nopeople1 = iface.activeLayer()
        layer_nopeople1.setCrs(QgsCoordinateReferenceSystem(4030))
        
        layer_fin4 = difference_saga("fin_grid_base", layer_fin3, layer_nopeople1)
        layer_fin5 = remove_null_load("fin_grid5", layer_fin4)
        layer_fin8 = multi_single("fin_base", layer_fin5,save=True)
    
    QgsMapLayerRegistry.instance().removeAllMapLayers()











