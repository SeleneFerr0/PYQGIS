#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
within new urban bound is 1, outside is 0

for batch 1 & 2, Result_grid2 are used

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
from qgis.core import QgsMessageLog
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import QColor
from qgis.core import QgsMapLayerRegistry, QgsSymbolV2, QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2


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
    #if save =False, the output will be kept only in memory
    #if save =True, the output will be saved to OutputFile and added to the current panel
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

def dsv_saga(filename, layer, field="new_id",alg="saga:polygondissolvebyattribute", save=False) :
    global OutputFile
    save_name = OutputFile + filename + ".shp"
    
    if save == True:
        processing.runalg(alg, layer, field, 0, save_name)
        data_source = save_name
        layer_name = filename
        provider_name = "ogr"
        return iface.addVectorLayer(data_source, layer_name, provider_name)        
        
    else:
        clip = processing.runalg(alg, layer, field, 0, None)
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

def find_neighbor(layer, attr='id2'):
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        index.insertFeature(f)
    
    layer.startEditing()
    for f in feature_dict.values():
        a = f[attr]
        b = f['id2']
        f[_NEW_ID] =f['id2']
        layer.updateFeature(f)
    
    layer.commitChanges()
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
        for intersecting_id in intersecting_ids:
            intersecting_f = feature_dict[intersecting_id]
            if intersecting_f[attr] =='':
                intersecting_f[_NEW_ID] =intersecting_f['id2']
            else:
                pass
            # For our purpose we consider a feature as 'neighbor' if it touches or intersects a feature. We use the 'disjoint' predicate to satisfy
            if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
                neighbors.append(intersecting_f[attr])
                if(intersecting_f["xmin"]==f["xmin"] and intersecting_f["ymin"]==f["ymax"]):
                    north.append(intersecting_f[attr])
                elif(intersecting_f["xmin"]==f["xmin"] and intersecting_f["ymax"]==f["ymin"]):
                    south.append(intersecting_f[attr])
                elif(intersecting_f["ymin"]==f["ymin"] and intersecting_f["xmin"]==f["xmax"]):
                    west.append(intersecting_f[attr])
                elif(intersecting_f["ymin"]==f["ymin"] and intersecting_f["xmax"]==f["xmin"]):
                    east.append(intersecting_f[attr])
        f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
        f[_NEW_NORTH] = ','.join(north)
        f[_NEW_SOUTH] = ','.join(south)
        f[_NEW_SUM_FIELD] = len(north) + len(south) + len(east) + len(west)
        f[_NEW_LEFT] = ','.join(east)
        f[_NEW_RIGHT] = ','.join(west)
        # Update the layer with new attribute values.
        layer.updateFeature(f)
        if (len(north) + len(south) + len(east) + len(west))==0:
            if (len(north)==0 and intersecting_f["ymin"]==f["ymax"] and (f.geometry().area()*12321)<0.3):
                north.append(intersecting_f[attr])
            elif (len(south)==0 and intersecting_f["ymax"]==f["ymin"] and (f.geometry().area()*12321)<0.3):
                south.append(intersecting_f[attr])
            elif (len(west)==0 and intersecting_f["xmin"]==f["xmax"] and (f.geometry().area()*12321)<0.3):
                west.append(intersecting_f[attr])
            elif (len(east)==0 and intersecting_f["xmax"]==f["xmin"] and (f.geometry().area()*12321)<0.3):
                east.append(intersecting_f[attr])
            f[_NEW_NEIGHBORS_FIELD] = ','.join(neighbors)
            f[_NEW_NORTH] = ','.join(north)
            f[_NEW_SOUTH] = ','.join(south)
            f[_NEW_SUM_FIELD] = len(north) + len(south) + len(east) + len(west)
            f[_NEW_LEFT] = ','.join(east)
            f[_NEW_RIGHT] = ','.join(west)
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
            if f[id] ==NULL:
                pass
            else:
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
            f[_NEW_ID] = new
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
        

BAU_path = 'C:\\Users\\base7005\\Documents\\BAU blocks\\'
path2 = 'C:\\Users\\base7005\\Documents\\BAUblocks2018\\done\\'
path ='C:\\Users\\base7005\\Documents\\BAUblocks2018\\bycity\\'

df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\QGISimport\\map_file.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_})
df_17 = pd.read_excel('C:\\Users\\base7005\\Documents\\BAUblocks2018\\city.xlsx',sheetname="sheet1",encoding='gb18030',dtype={'citycode': np.str_,'Block_id': np.str_,'towncode': np.str_})
df_16 = pd.read_excel('C:\\Users\\base7005\\Documents\\BAUblocks2018\\16UU.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'Citycode_16': np.str_,'Block_id': np.str_, 'TownCode': np.str_})
df_18 = pd.read_excel('C:\\Users\\base7005\\Documents\\BAUblocks2018\\Joey18.xlsx',sheetname='Sheet1',encoding='gb18030',dtype={'Block_id': np.str_,'Block_id_dc': np.str_, 'Citycode_before': np.str_, 'citycode':np.str_})


'''
df_17 - what we have got in the layers 
df_16 - blocks that have ID assigned in 16UU
df_18_joey - block upgrades until 18W1, Block_id denotes all the blocks named by DA

'''
blk_17 = set(df_17.Block_id.unique())
blk_16 = set(df_16.Block_id.unique())
len(blk_17 - blk_16)
len(blk_16 - blk_17)
len(blk_17 & blk_16)
blk_shared_1 = list(blk_17 & blk_16)

blk_18 = set(df_18.Block_id.unique())
len(blk_18 - blk_17)
len(blk_17 - blk_18)
len(blk_17 & blk_18)
blk_shared_2 = list(blk_17 & blk_18)


df_city16 = df_16[df_16['Block_id'].isin(blk_shared_1)]
df_city16 = df_city16[['Block_id', 'Citycode_16', 'Region', 'DistrictCode', 'ID']]
df_city16= df_city16.sort_values(by=['Citycode_16', 'Block_id', 'DistrictCode'], ascending=[True, True, True])


#block id that in both 16&17
df_city = df_17[df_17['Block_id'].isin(blk_shared_1)]
df_city = df_city[['Block_id', 'citycode', 'towncode', 'batch']]
df_city= df_city.sort_values(by=['citycode', 'Block_id','batch'], ascending=[True, True, True])
chk = df_city[df_city.Block_id.duplicated()]
if len(chk>0):
    print("duplicated block ids. " + str(len(chk)) + ' block ids are duplicated' )
    df_city = df_city[~df_city.Block_id.duplicated(keep='first')]
else:
    pass


#df_tmp.to_excel(path+ '_upgraded.xlsx',encoding="gb18030")



df_upgrade = df_18.drop(df_18[df_18['Block_id'].isin(blk_16)].index)
len(df_upgrade)

df_sum = df_city16[['Block_id', 'Region','DistrictCode', 'ID']]
df_tmp = df_upgrade[['Block_id', 'Region' ,'DistrictCode']]
df_tmp['citycode'] = df_tmp.Block_id.str.slice(0, 4)
df_tmp= df_tmp.sort_values(by=['citycode', 'DistrictCode','Block_id'], ascending=[True, True, True])
df_tmp['ID'] = 6

cities = list(df_tmp.citycode.unique())

for city in cities:
    temp = df_tmp[df_tmp.citycode == str(city)]
    dists = list(temp.DistrictCode.unique())
    R0 = 6
    for dist in dists:
        df_tmp.loc[(df_tmp['citycode'] == str(city)) & (df_tmp['DistrictCode']==int(dist)), 'ID'] = R0
        R0 = R0 + 1
    
    df_sum =df_sum.append(df_tmp)

blk_18 = set(df_sum.Block_id.unique())
len(blk_18 - blk_17)
len(blk_17 - blk_18)
len(blk_17 & blk_18)
blk_shared_2 = list(blk_17 & blk_18)

df_sum=df_sum[df_sum['Block_id'].isin(blk_shared_2)]
df_sum['citycode'] = df_sum.Block_id.str.slice(0, 4)
from pandas import ExcelWriter

writer = ExcelWriter(path + 'Tier_Export2.xlsx')
df_sum.to_excel(writer,'Sheet1')
writer.save()

df_iter = df_sum.pivot_table(values='Block_id', index='citycode', columns='ID', aggfunc=lambda x: len(x.unique()))
df_iter['cntna'] = df_iter.isnull().sum(axis=1)

df_iter = df_iter[df_iter.cntna<5]

cities = list(df_iter.index.unique())
city = cities[0]


for city in cities:
    OutputFile = path + city+ '\\'
    print(str(city))
    
    if os.path.exists(OutputFile):
        print(city + ' folder already exist')
        pass
    else:
        os.mkdir(OutputFile)
    
    
    df_city_tmp = df_city[df_city.citycode == city]
    batch = list(df_city_tmp.batch.unique())

    if len(batch)>1:
        print("different batches for " + str(citycode))
        print(batch)
    else:
        batch = batch[0]
    
    data_source = BAU_path + 'B' + batch[0] + '\\' + batch[0:3] + '\\' + 'batch' + batch + '.shp'
    layer_name = 'batch' + batch
    provider_name = "ogr"
    layer_block = iface.addVectorLayer(data_source, layer_name, provider_name)
    layer_block = iface.activeLayer()
    layer_block.setCrs(QgsCoordinateReferenceSystem(4030))
    
    processing.runalg("qgis:selectbyattribute", layer_block, u'citycode', 0, city)
    filename="city_" +str(city) 
    save_name = OutputFile + filename + ".shp"
    processing.runalg("qgis:saveselectedfeatures",layer_block,save_name)
    data_source = save_name
    layer_name = filename
    provider_name = "ogr"
    layer_city=iface.addVectorLayer(data_source, layer_name, provider_name)
    layer_city.dataProvider().setEncoding(u'gb18030')
    QgsMapLayerRegistry.instance().removeMapLayers( [layer_block.id()])
    
    field_names = [field.name() for field in layer_city.pendingFields() ]
    if 'ringtier' in field_names:
        print("Ring Tier has been added")
        pass
    else:
            layer_city.dataProvider().addAttributes([QgsField("ringtier", QVariant.Int)])
            layer_city.updateFields()
            
            feature_dict = {f.id(): f for f in layer_city.getFeatures()}
            index = QgsSpatialIndex()
            for f in feature_dict.values():
                index.insertFeature(f)
    
    feature_dict = {f.id(): f for f in layer_city.getFeatures()}
    layer_city.startEditing()
    for f in feature_dict.values():
        block_id =  f['Block_id']
        try:
            f['ringtier'] = int(df_sum[df_sum['Block_id'] == str(block_id)].ID)
        except TypeError:
            f['ringtier'] = 0
        layer_city.updateFeature(f)
    
    layer_city.commitChanges()
    QgsMapLayerRegistry.instance().removeAllMapLayers()


'''round 2 - summary file'''

path = 'C:\\Users\\base7005\\Documents\\BAUblocks2018\\bycity\\'
path = path.decode('utf-8')
files = os.listdir(path)

df_summary = pd.DataFrame(index=None, columns=None)
for file in files:
    print(file)
    file_path = path + file + '\\'
    layer_bau_city = QgsVectorLayer(file_path + 'city_' +str(file)+ '.shp','city_' +str(file), 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(layer_bau_city)
    layer_bau_city = iface.activeLayer()
    layer_bau_city.setCrs(QgsCoordinateReferenceSystem(4030))
    QgsVectorFileWriter.writeAsVectorFormat(layer_bau_city, file_path + str(file) + "_ringtier", "ANSI", None, "CSV", layerOptions='GEOMETRY=AS_XYZ')
    df_city = pd.DataFrame.from_csv(file_path + str(file)  + "_ringtier.csv", index_col='Block_id')
    df_summary=df_summary.append(df_city)
    QgsMapLayerRegistry.instance().removeAllMapLayers()


from pandas import ExcelWriter

writer = ExcelWriter(path + 'Tier_Export.xlsx')
df_summary.to_excel(writer,'Sheet1')
writer.save()






#for city in cities:
#    OutputFile = path + city+ '\\'
#    print(str(city))
#    
#    df_city_tmp = df_city[df_city.citycode == city]
#    filename = 'city_'+str(city)
#    save_name = OutputFile + filename + ".shp"
#    
#    data_source = save_name
#    layer_name = filename
#    provider_name = "ogr"
#    layer_city=iface.addVectorLayer(data_source, layer_name, provider_name)
#    layer_city.dataProvider().setEncoding(u'gb18030')
#    QgsMapLayerRegistry.instance().removeMapLayers( [layer_block.id()])
#    
#    field_names = [field.name() for field in layer_city.pendingFields() ]
#    if 'ringtier' in field_names:
#        print("Ring Tier has been added")
#        pass
#    else:
#            layer_city.dataProvider().addAttributes([QgsField("ringtier", QVariant.Int)])
#            layer_city.updateFields()
#            
#            feature_dict = {f.id(): f for f in layer_city.getFeatures()}
#            index = QgsSpatialIndex()
#            for f in feature_dict.values():
#                index.insertFeature(f)
#    
#    feature_dict = {f.id(): f for f in layer_city.getFeatures()}
#    layer_city.startEditing()
#    for f in feature_dict.values():
#        block_id =  f['Block_id']
#        if f['ringtier']>5:
#            try:
#                f['ringtier'] = int(df_tmp[df_tmp['Block_id'] == str(block_id)].ID)
#            except TypeError:
#                print('block ' +str(block_id) + ' not found')
#                f['ringtier'] = 0
#            layer_city.updateFeature(f)
#        else:
#            pass
#    
#    layer_city.commitChanges()
#    QgsMapLayerRegistry.instance().removeAllMapLayers()



#Coloring
#symbols = layer_city.rendererV2().symbols()
#symbol = symbols[0]
#symbol.setColor(QColor.fromRgb(110,135,212))
#qgis.utils.iface.mapCanvas().refresh() 
#qgis.utils.iface.legendInterface().refreshLayerSymbology(layer_city)
#extent = layer_boundary_grid.extent()
#iface.mapCanvas().setExtent(extent)
#iface.mapCanvas().refresh()
#layer_boundary_grid.setLayerTransparency(70)
#iface.mapCanvas().refresh()


#values = (
#    ('Low', 1, 8, 'green'),
#    ('Medium', 9, 16, 'yellow'),
#    ('Large', 17, 24, 'orange'),
#)
#
## create a category for each item in values
#ranges = []
#for label, lower, upper, color in values:
#    symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
#    symbol.setColor(QColor(color))
#    rng = QgsRendererRangeV2(lower, upper, symbol, label)
#    ranges.append(rng)
#
## create the renderer and assign it to a layer
#expression = 'random' # field name
#renderer = QgsGraduatedSymbolRendererV2(expression, ranges)
#layer.setRendererV2(renderer)
#
#iface.mapCanvas().refresh()


