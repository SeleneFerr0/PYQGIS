#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Round 2: Count POI for merged grid with new CCEblocks
within new urban bound is 1, outside is 0
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
import urllib
import math
import utm
from qgis.core import *
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QInputDialog

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

def merge_layers(filename, layers, alg="qgis:mergevectorlayers", save=False):
    '''
    #This is a warpper-function for "remove_null_geometries"
    '''
    global OutputFile2
    save_name = OutputFile2 + filename + ".shp"
    if save == False:
        remove = processing.runalg(alg, layers, None)
        return processing.getObject(remove['OUTPUT_LAYER'])
    else:
        processing.runalg(alg, layers, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)
        


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
    global OutputFile2
    save_name = OutputFile2 + filename + ".shp"
    
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

def area_update(filename, layer, alg="qgis:fieldcalculator", save=False):
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save == True:
        processing.runalg(alg, layer,"area",0,10,2,False,"$area/1000000",save_name)
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
    save_name = OutputFile2 + filename + ".shp"
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

def find_neighbor(layer, length = 11):
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
        if len(east)>12:
            f[_NEW_LEFT] = east[0:length]
        else:
            f[_NEW_LEFT] = ','.join(east)
        if len(west)>12:
            f[_NEW_RIGHT] = west[0:length]
        else:
            f[_NEW_RIGHT] = ','.join(west)
        f[_NEW_ID] =f["id2"]
        # Update the layer with new attribute values.
        layer.updateFeature(f)
    layer.commitChanges()

def refresh (layer):
    it = layer.getFeatures()
    featureNumber = layer.featureCount()
    n=1
    layer.startEditing()
    for feat, id2 in zip(it, range(1, featureNumber+1)):
        # when using fin_gird, the column is 8; people_grid 6.
        layer.changeAttributeValue(feat.id(), 8, str(AD_CODE) +str(n).zfill(5))
        n=n+1
    
    layer.commitChanges


path2 = 'C:\\Users\\base7005\\Documents\\CityBoundary\\UTM_area\\done'
poi_path = 'C:\\Users\\base7005\\Documents\\CityBoundary\\txt\\'
poi_dest = 'C:\\Users\\base7005\\Documents\\CityBoundary\\poi\\'
path_dest = 'C:\\Users\\base7005\\Documents\\CityBoundary\\UTM_area\\Grids_prv'
df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\\\Urban\\base\\CCE_2018W2UE_TrackingList.xlsx',sheetname="list18W2",encoding='gb18030',dtype={'citycode': np.str_, 'AD_CODE':np.str_})

global path, SourceFile
path =  'C:\\Users\\base7005\\Documents\\CityBoundary\\UTM_area\\utm_light\\重庆市\\'
path = path.decode('utf-8')
files = os.listdir(path)
files.sort()
n = 0
print(path[-4:-1])

for file in files:
    province = path[-4:-1]
    city=file.split("_",1)[0]
    dist = file.split("_",1)[1][:-7]
    AD_CODE = file[-6:]
    citycode = df_map.loc[df_map['AD_CODE']==AD_CODE,'citycode']
    citycode = int(citycode)
    citycode =str(citycode).zfill(4)
    field_ids = []

    fieldnames = set(['grid_id','fin_id', 'new_id', 'NUMPOINTS', 'Resident', 'area2'])
    
    SourceFile = path + file +'\\'
    
    if not os.path.exists(path_dest + '\\'+ province):
        os.makedirs(path_dest + '\\'+province)
    else:
        pass
    
    
    OutputFile2 = path_dest + '\\' + province + '\\'
    if os.path.exists( SourceFile + 'inbound_UTM.shp'):
        layer_in = QgsVectorLayer(SourceFile + 'inbound_UTM.shp','inbound_UTM', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_in)
        layer_in = iface.activeLayer()
#        layer_in.setCrs(QgsCoordinateReferenceSystem(4030))
        for field in layer_in.fields():
            if field.name() not in fieldnames:
                field_ids.append(layer_in.fieldNameIndex(field.name()))
        layer_in.dataProvider().deleteAttributes(field_ids)
        layer_in.updateFields()
        n = n+ int(layer_in.featureCount())
    elif os.path.exists( SourceFile +' inbound_UTM.shp'):
        layer_in = QgsVectorLayer(SourceFile + ' inbound_UTM.shp',' inbound_UTM', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_in)
        layer_in = iface.activeLayer()
#        layer_in.setCrs(QgsCoordinateReferenceSystem(4030))
        for field in layer_in.fields():
            if field.name() not in fieldnames:
                field_ids.append(layer_in.fieldNameIndex(field.name()))
        
        layer_in.dataProvider().deleteAttributes(field_ids)
        layer_in.updateFields()
        n = n+ int(layer_in.featureCount())
    
    if os.path.exists( SourceFile +'outbound_UTM.shp'):
        layer_out = QgsVectorLayer(SourceFile + 'outbound_UTM.shp','outbound_UTM', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_out)
        layer_out = iface.activeLayer()
#        layer_out.setCrs(QgsCoordinateReferenceSystem(4030))
        for field in layer_out.fields():
            if field.name() not in fieldnames:
                field_ids.append(layer_out.fieldNameIndex(field.name()))
        
        layer_out.dataProvider().deleteAttributes(field_ids)
        layer_out.updateFields()
        n = n+ int(layer_out.featureCount())
    elif os.path.exists( SourceFile +' outbound_UTM.shp'):
        layer_out = QgsVectorLayer(SourceFile + ' outbound_UTM.shp',' outbound_UTM', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_out)
        layer_out = iface.activeLayer()
#        layer_out.setCrs(QgsCoordinateReferenceSystem(4030))
        for field in layer_out.fields():
            if field.name() not in fieldnames:
                field_ids.append(layer_out.fieldNameIndex(field.name()))
        
        layer_out.dataProvider().deleteAttributes(field_ids)
        layer_out.updateFields()
        n = n+ int(layer_out.featureCount())

layers = QgsMapLayerRegistry.instance().mapLayers().values()
layer_merge = merge_layers("merged_grids", layers, save=True)

print("feature count: " + str(n))
print("merged feature: " + str(layer_merge.featureCount()))

QgsMapLayerRegistry.instance().removeAllMapLayers()
