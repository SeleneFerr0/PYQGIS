#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
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
import json
import urllib
import math
from qgis.core import *
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QColor
from qgis.core import QgsMapLayerRegistry, QgsVectorJoinInfo
from qgis.core import QgsMessageLog
import mmqgis

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

path2 = 'C:\\Users\\base7005\\Documents\\CCE blocks\\done'
#Residential_path = "C:\\Users\\base7005\\Documents\\QGISimport\\Residential\\Liaoning\\"
df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\QGISimport\\map_file.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_})
#df_stores = pd.read_excel('C:\\Users\\base7005\\Documents\\CCEstores\\ccestores.xlsx',sheetname="aug",encoding='gb18030',dtype={'CITYCODE12': np.str_})


global path, OutputFile, OutputFile2
#path = 'C:\\Users\\base7005\\Documents\\QGISimport\\result\\batch3_1-6 rerun\\batch3_1\\广东省\\'
path = 'C:\\Users\\base7005\\Documents\\BAUchange\\kml1106\\'
path = path.decode('utf-8')
files = os.listdir(path)
OutputFile2 = path2 + '\\'
lost_list = []
for file in files:
    OutputFile = path + file + '\\'
    citycode = file[0:4]
    print(citycode)
    if os.path.isfile(OutputFile + str(citycode) + '_dsv'+ '.shp'):
        layer_tmp = QgsVectorLayer(OutputFile + str(citycode) + '_dsv'+ '.shp' ,str(citycode) + '_dsv', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_tmp)
        layer_tmp = iface.activeLayer()
        layer_tmp.setCrs(QgsCoordinateReferenceSystem(4030))
    else:
        print("blocks not found")
        pass
    
    #print(invalid_list)
    
layers = QgsMapLayerRegistry.instance().mapLayers().values()
    
    #QgsMapLayerRegistry.instance().removeAllMapLayers()









