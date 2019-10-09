#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
For Amin
Convert KML to SHP.
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

def check_validty(layer1, alg = "qgis:checkvalidity", method =0, save=False):
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    if save == False:
        remove = processing.runalg(alg, layer1,  method, None)
        return processing.getObject(remove['OUTPUT_LAYER'])
    else:
        processing.runalg(alg, layer1,  method, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)

path2 = 'C:\\Users\\base7005\\Documents\\BAU blocks\\done'
#Residential_path = "C:\\Users\\base7005\\Documents\\QGISimport\\Residential\\Liaoning\\"
df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\\\Urban\\base\\CCE_2018W2UE_TrackingList.xlsx',sheetname="list18W2",encoding='gb18030',dtype={'citycode': np.str_, 'AD_CODE':np.str_})
#df_stores = pd.read_excel('C:\\Users\\base7005\\Documents\\CCEstores\\ccestores.xlsx',sheetname="aug",encoding='gb18030',dtype={'CITYCODE12': np.str_})

global path, OutputFile, OutputFile2
path = 'C:\\Users\\base7005\\Documents\\BAUblocks2018\\test\\'
path = path.decode('utf-8')
kmls = os.listdir(path)
OutputFile = 'C:\\Users\\base7005\\Documents\\BAUblocks2018\\result\\'
OutputFile2 = path2 + '\\'
invalid_list = []



if os.path.isfile(OutputFile + 'output.shp'):
    print("already done, please delete the shapefiles if rerun")
else:
    for kml in kmls:
        block_id = kml[0:13]
        layer_tmp = QgsVectorLayer(path + kml,kml[0:-4], 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_tmp)
        layer_tmp = iface.activeLayer()
        layer_tmp.setCrs(QgsCoordinateReferenceSystem(4030))
        
        layer_1D = convert_polygon(str(block_id), layer_tmp, save=True)
        layer_1D.dataProvider().addAttributes([QgsField("block_id", QVariant.String)])
        layer_1D.updateFields()
        
        feature_dict = {f.id(): f for f in layer_1D.getFeatures()}
        index = QgsSpatialIndex()
        for f in feature_dict.values():
            index.insertFeature(f)
        
        layer_1D.startEditing()
        for f in feature_dict.values():
            f['block_id'] = block_id
            layer_1D.updateFeature(f)
        
        layer_1D.commitChanges()
        QgsMapLayerRegistry.instance().removeMapLayers([layer_tmp.id()])
    
    layers = QgsMapLayerRegistry.instance().mapLayers().values()
    #all = [QgsMapLayerRegistry.instance().mapLayersByName('layer_1D')[0]]
    save_name = OutputFile2 + "output_tmp.shp"
    processing.runalg("qgis:mergevectorlayers", layers, save_name)
    QgsMapLayerRegistry.instance().removeAllMapLayers()
    
    layer_cce_block = QgsVectorLayer(OutputFile2 + 'output_tmp.shp', 'output_tmp', 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(layer_cce_block)
    layer_cce_block = iface.activeLayer()
    layer_cce_block.setCrs(QgsCoordinateReferenceSystem(4030))
    #from qgis.core import (QgsMessageLog,
    #                   QgsApplication,
    #                   QgsMapLayer,
    #                   QgsProcessingProvider,
    #                   QgsProcessingAlgorithm,
    #                   QgsProcessingException,
    #                   QgsProcessingParameterDefinition,
    #                   QgsProcessingOutputVectorLayer,
    #                   QgsProcessingOutputRasterLayer,
    #                   QgsProcessingOutputMapLayer,
    #                   QgsProcessingOutputMultipleLayers,
    #                   QgsProcessingFeedback)
    extent = layer_cce_block.extent()
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()
    
    save_name = OutputFile + "output.shp"
    processing.runalg("grass7:v.clean",layer_cce_block, 6, 0.1,"%f,%f,%f,%f" % (xmin, xmax, ymin, ymax), 0, 0.001, save_name, None)
    
    layer_cce_rmdupl = QgsVectorLayer(OutputFile + 'output.shp','output', 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(layer_cce_rmdupl)
    layer_cce_rmdupl = iface.activeLayer()
    layer_cce_rmdupl.setCrs(QgsCoordinateReferenceSystem(4030))
    
    layer_cce_dsv = dsv_load("output_dsv", layer_cce_rmdupl, field = "block_id", save=True)
    layer_chk = check_validity("output_valid",  "output_invalid", layer_cce_dsv, save=True)
    
    if int(layer_cce_dsv.featureCount()) == int(layer_chk.featureCount()):
        print("all valid")
    else:
        print(str(citycode) +' has ' + str(int(layer_cce_dsv.featureCount()) - int(layer_chk.featureCount())) + ' features not valid')
        invalid_list.append(citycode)
    
    QgsMapLayerRegistry.instance().removeAllMapLayers()







