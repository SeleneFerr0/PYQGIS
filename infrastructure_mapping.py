#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
##ReadMe

1. Please install 'pandas' following the tutorial.
    Download Link: https://pan.baidu.com/s/1bIh0WA  
    Password: 2cra
    
'''

import pandas as pd
import numpy as np
import processing
import os
import shutil
import shapely
import json
import urllib
import math
from qgis.core import *
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import *
from qgis.core import QgsMessageLog

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.utils import iface


global path, OutputFile
path = 'C:\\Users\\base7005\\Documents\\CityBoundary\\江苏省\\'
path = path.decode('utf-8')
#**************** 用于记录已处理完毕的poi, 这个路径下不能有中文！！！！！！
path2 ='C:\\Users\\base7005\\Documents\\CityBoundary\\result'
files = os.listdir(path)

citylist_path = 'C:\\Users\\base7005\\Documents\\CityBoundary\\Citylist.csv'
citylist = pd.read_csv(citylist_path, index_col=None,encoding="gb18030")
citylist['AD_Code'] =citylist['CTB'].astype(str).str[0:6]
#file = u'\u65e0\u9521\u5e02_\u6ee8\u6e56\u533a_320211.txt'

for file in files:

    OutputFile = path + file[:-4] + '\\'
    OutputFile2 = path2 + '\\'
    os.mkdir(OutputFile)
    os.rename(path + file, path + file[-10:])
    shutil.move(path + file[-10:], path2)
    AD_Code=int(file[-10:-4])



    uri = "file:///" + path2 + '\\' + file[-10:] +"?encoding=GB2312&type=csv&delimiter=,%20%5Ct&xField=X&yField=Y&spatialIndex=no&subsetIndex=no&watchFile=no"
    layer_total_csv = QgsVectorLayer(uri, file,'delimitedtext')
    layer_total_csv.setCrs(QgsCoordinateReferenceSystem(4030))
    QgsMapLayerRegistry.instance().addMapLayer(layer_total_csv)
    layer_total_csv = iface.activeLayer()
    layer_total_csv.setCrs(QgsCoordinateReferenceSystem(4030))

    csvdata_total = pd.read_table(path2 + '\\' + file[-10:], index_col=None, encoding="gb18030", delimiter= ',')
    csvdata7 = csvdata_total[csvdata_total['L1']==u'公共设施']
    csvdata7.to_csv(path2+ '\\'+file[-10:-4] +'_infrastructure.csv',encoding="gb18030")

    i = '_infrastructure.csv'
    uri = "file:///" + path2+ '\\' + file[-10:-4] + i +"?type=csv&xField=X&yField=Y&spatialIndex=no&subsetIndex=no&watchFile=no"
    layer_poi = QgsVectorLayer(uri,  file[-10:-4] + i,'delimitedtext')
    layer_poi.setCrs(QgsCoordinateReferenceSystem(4030))
    QgsMapLayerRegistry.instance().addMapLayer(layer_poi)
    layer_poi = iface.activeLayer()
    layer_poi.setCrs(QgsCoordinateReferenceSystem(4030))

    QgsMapLayerRegistry.instance().removeMapLayers( [layer_total_csv.id()] )

    #clean city list name
    city_total = citylist[citylist['AD_Code']==str(AD_Code)]

    city_name = city_total['City'].unique()
    city_name = city_name[0]

    dist_name = city_total['District'].unique()
    dist_name = dist_name[0]

    city_total['NAME'] = city_total.NAME.replace(city_name, '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(dist_name, '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(city_name[:-1], '', regex=True)
    city_total['NAME'] = city_total.NAME.replace(dist_name[:-1], '',regex=True)

    city_total['NAME'] = city_total.NAME.replace(u'（', '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'）', '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'市', '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'区', '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'县', '',regex=True)

    city_total['NAME'] = city_total.NAME.replace(u'居民委员会', u'居委会',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'村民委员会', u'村委会',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'村村', u'村',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'镇', '',regex=True)
    city_total['NAME'] = city_total.NAME.replace(u'街道', '',regex=True)

    city_total['Townname'] = city_total.Townname.replace(city_name, '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(dist_name, '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(city_name[:-1], '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(dist_name[:-1], '',regex=True)
    
    city_total['Townname'] = city_total.Townname.replace(u'（', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'）', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'镇', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'县', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'区', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'街道', '',regex=True)
    city_total['Townname'] = city_total.Townname.replace(u'办事处', '',regex=True)

    # generate combined name
    city_total['NameCmb'] = city_total[['Townname', 'NAME']].apply(lambda x: ''.join(x), axis=1)

    city_total['NameCmb'] = city_total.NameCmb.replace(u'社', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'区', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'县', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'镇', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'街道', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'居委会', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'村委会', '',regex=True)
    city_total['NameCmb'] = city_total.NameCmb.replace(u'村', '',regex=True)

    city_total.to_csv(OutputFile + 'city_total.csv', encoding="gb18030")


    # clean POI name
    df_infra = pd.read_csv(path2+ '\\'+file[-10:-4] +'_infrastructure.csv', index_col=None,encoding="GB18030")
    df_infra = df_infra[df_infra['L2']==u'政府及管理机构']
    df_infra = pd.DataFrame(df_infra)

    df_infra['content'] = df_infra['NAME'].str.lower().str.split()

    df_infra['NAME'] = df_infra.NAME.replace(u'（', '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'）', '',regex=True)

    df_infra['NAME'] = df_infra.NAME.replace(city_name, '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(dist_name, '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(city_name[:-1], '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(dist_name[:-1], '',regex=True)

    df_infra['NAME'] = df_infra.NAME.replace(u'居民委员会', u'居委会',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'村民委员会', u'村委会',regex=True)

    df_infra['NAME'] = df_infra.NAME.replace(u'村村', u'村',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'镇', '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'区', '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'县', '',regex=True)
    df_infra['NAME'] = df_infra.NAME.replace(u'街道', '',regex=True)



    for j in [111, 112, 121, 122, 123, 210, 220]:
        
        temp = city_total[city_total['LEVEL']==j]
        print(str(j) +' has '+ str(len(temp)) + ' items')
        if len(temp) >0:
            nameList = '|'.join(temp['NameCmb'].tolist())
            df_infra.loc[df_infra['NAME'].str.contains(nameList, case=False), 'level'] = str(j)
        temp2 = df_infra[df_infra['level']==str(j)]
        temp2.to_csv(path2+ '\\'+file[-10:-4] + '_' + str(j) +'.csv',encoding="gb18030")

    df_infra.to_csv(OutputFile + 'df_infra.csv', encoding="gb18030")


    df_infra['level'] = 0
    it = iter([111, 112, 121, 122, 123, 210, 220])
    for j in it:
        uri = "file:///" + path2+ '\\' + file[-10:-4] + '_' + str(j) +'.csv' +"?type=csv&xField=X&yField=Y&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer_poi = QgsVectorLayer(uri,  file[-10:-4] + '_' + str(j) +'.csv','delimitedtext')
        layer_poi.setCrs(QgsCoordinateReferenceSystem(4030))
        if int(layer_poi.featureCount())==0:
            if j ==220:
                break
            else:
                next(it)
        else:
            if j == 111:
                fontStyle = {}
                fontStyle['color'] = '#585aee'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = 'G'
                fontStyle['size'] = '6'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j == 112:
                fontStyle = {}
                fontStyle['color'] = '#7374ae'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = '5'
                fontStyle['size'] = '7'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j == 121:
                fontStyle = {}
                fontStyle['color'] = '#8d0017'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = 'g'
                fontStyle['size'] = '6'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j == 122:
                fontStyle = {}
                fontStyle['color'] = '#c35774'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = '1'
                fontStyle['size'] = '6'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j ==123:
                fontStyle = {}
                fontStyle['color'] = '#a988c5'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = 'n'
                fontStyle['size'] = '6'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j ==210:
                fontStyle = {}
                fontStyle['color'] = '#7fcfc7'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = 'Q'
                fontStyle['size'] = '5'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            elif j ==220:
                fontStyle = {}
                fontStyle['color'] = '#4eae3c'
                fontStyle['font'] = 'Webdings'
                fontStyle['chr'] = 'M'
                fontStyle['size'] = '5'
                symLyr1 = QgsFontMarkerSymbolLayerV2.create(fontStyle)
                layer_poi.rendererV2().symbols()[0].changeSymbolLayer(0, symLyr1)
            QgsMapLayerRegistry.instance().addMapLayer(layer_poi)
            layer_poi = iface.activeLayer()
            layer_poi.setCrs(QgsCoordinateReferenceSystem(4030))
            save_name = OutputFile+ str(AD_Code) + '_' + str(j) + '.shp'
            QgsVectorFileWriter.writeAsVectorFormat(layer_poi, save_name, "utf-8", None, "ESRI Shapefile")
    
    QgsMapLayerRegistry.instance().removeAllMapLayers()


