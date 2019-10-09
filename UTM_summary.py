#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
#import utm
from qgis.core import *
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QInputDialog

global path, path_all, path_stella, SourceFile
path_all =  'C:\\Users\\base7005\\Documents\\CityBoundary\\POI_results_merge\\'
path_all = path_all.decode('utf-8')
files_all = os.listdir(path_all)
files_all.sort()
files_all.index(u"安徽省")

path_stella = 'C:\\Users\\base7005\\Documents\\CityBoundary\\ToStella\\'


df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\Urban\\base\\CCE_2018W2UE_TrackingList.xlsx',sheetname="list18W2",encoding='gb18030',dtype={'citycode': np.str_, 'AD_CODE':np.str_})
df_record = pd.read_excel('C:\\Users\\base7005\\Documents\\CityBoundary\\infi_tostella\\Summary.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_, 'AD_CODE':np.str_})

path_dest = 'C:\\Users\\base7005\\Documents\\CityBoundary\\summary\\'
n =0

for file_prv in files_all:
    print(file_prv)
    df_prv_record = df_record[df_record.Province == file_prv]
    path = path_all + file_prv + '\\'
    files = os.listdir(path)
    files.sort()
    for file in files:
        SourceFile = path + file +'\\'
        SourceFile2 = path_stella + file_prv + '\\' + file + '\\'
        city=file.split("_",1)[0]
        dist = file.split("_",1)[1][:-7]
        AD_CODE = file[-6:]
        print(file_prv + " " + city + " " + dist)
        citycode = df_map.loc[df_map['AD_CODE']==AD_CODE,'citycode']
        citycode = int(citycode)
        citycode =str(citycode).zfill(4)
        
        
#        if not os.path.exists(path_dest + province):
#            os.makedirs(path_dest + province)
#            if not os.path.exists(path_dest + province +'\\' + file):
#                os.makedirs(path_dest + province +'\\' + file)
#            else:
#                pass
#        else:
#            if not os.path.exists(path_dest + province +'\\' + file):
#                os.makedirs(path_dest + province +'\\' + file)
#            else: 
#                pass
#
#        OutputFile = path_dest + province +'\\' + file +'\\'


        if os.path.exists( SourceFile + 'inbound_poires.shp'):
            layer_in = QgsVectorLayer(SourceFile + 'inbound_poires.shp','inbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_in)
#            layer_in = iface.activeLayer()
#            df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'inbound'] = int(layer_in.featureCount())
            
            layer_in2 = QgsVectorLayer(SourceFile2 + 'inbound_poires.shp','inbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_in2)
#            layer_in2 = iface.activeLayer()
            
            if int(layer_in.featureCount()) != int(layer_in2.featureCount()):
                print("inbound")
                print(int(layer_in.featureCount()) - int(layer_in2.featureCount()) )
    #        QgsVectorFileWriter.writeAsVectorFormat(layer_in,  OutputFile + "inbound_poires.shp", "utf-8", None, "ESRI Shapefile")
        elif os.path.exists( SourceFile +' inbound_poires.shp'):
            layer_in = QgsVectorLayer(SourceFile + ' inbound_poires.shp',' inbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_in)
#            layer_in = iface.activeLayer()
#            df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'inbound'] = int(layer_in.featureCount())
            layer_in2 = QgsVectorLayer(SourceFile2 + 'inbound_poires.shp','inbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_in2)
#            layer_in2 = iface.activeLayer()
            
            if int(layer_in.featureCount()) != int(layer_in2.featureCount()):
                print("inbound")
                print(int(layer_in.featureCount()) - int(layer_in2.featureCount()) )
    #        QgsVectorFileWriter.writeAsVectorFormat(layer_in,  OutputFile + "inbound_poires.shp", "utf-8", None, "ESRI Shapefile")


        if os.path.exists( SourceFile +'outbound_poires.shp'):
            layer_out = QgsVectorLayer(SourceFile + 'outbound_poires.shp','outbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_out)
#            layer_out = iface.activeLayer()
#            df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'outbound'] = int(layer_out.featureCount())
            layer_out2 = QgsVectorLayer(SourceFile2 + 'outbound_poires.shp','outbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_out2)
#            layer_out2 = iface.activeLayer()
            if int(layer_out.featureCount()) != int(layer_out2.featureCount()):
                print("outbound")
                print(int(layer_out.featureCount()) - int(layer_out2.featureCount()) )
    #        QgsVectorFileWriter.writeAsVectorFormat(layer_out,  OutputFile + "outbound_poires.shp", "utf-8", None, "ESRI Shapefile")
        elif os.path.exists( SourceFile +' outbound_poires.shp'):
            layer_out = QgsVectorLayer(SourceFile + ' outbound_poires.shp',' outbound_poires', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_out)
#            layer_out = iface.activeLayer()
#            df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'outbound'] = int(layer_out.featureCount())
            layer_out2 = QgsVectorLayer(SourceFile2 + 'outbound_poires.shp','outbound_poires', 'ogr')
            if int(layer_out.featureCount()) != int(layer_out2.featureCount()):
                print("outbound")
                print(int(layer_out.featureCount()) - int(layer_out2.featureCount()) )
    #        QgsVectorFileWriter.writeAsVectorFormat(layer_out,  OutputFile + "outbound_poires.shp", "utf-8", None, "ESRI Shapefile")


        layer_bau_city = QgsVectorLayer(SourceFile + 'boundary_city.shp','boundary_city', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_bau_city)
#        layer_bau_city = iface.activeLayer()
#        df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'city'] = int(layer_bau_city.featureCount())
        layer_bau_city2 = QgsVectorLayer(SourceFile2 + 'boundary_city.shp','boundary_city', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_bau_city2)
#        layer_bau_city2 = iface.activeLayer()
        if int(layer_bau_city.featureCount()) != int(layer_bau_city2.featureCount()):
            print("bau city")
            print(int(layer_bau_city.featureCount()) - int(layer_bau_city2.featureCount()) )
    #    QgsVectorFileWriter.writeAsVectorFormat(layer_bau_city,  OutputFile + "boundary_city.shp", "utf-8", None, "ESRI Shapefile")

        layer_bau_tgts = QgsVectorLayer(SourceFile + 'boundary_TGTS.shp','boundary_TGTS', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_bau_tgts)
#        layer_bau_tgts = iface.activeLayer()
        layer_bau_tgts2 = QgsVectorLayer(SourceFile2 + 'boundary_TGTS.shp','boundary_TGTS', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_bau_tgts2)
#        layer_bau_tgts2 = iface.activeLayer()
#        df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'tgts'] = int(layer_bau_tgts.featureCount())
        if int(layer_bau_tgts.featureCount()) != int(layer_bau_tgts2.featureCount()):
            print("bau tgts")
            print(int(layer_bau_tgts.featureCount()) - int(layer_bau_tgts2.featureCount()) )
    #    QgsVectorFileWriter.writeAsVectorFormat(layer_bau_tgts,  OutputFile + "boundary_TGTS.shp", "utf-8", None, "ESRI Shapefile")

        layer_cce = QgsVectorLayer(SourceFile + 'boundary_cce.shp','boundary_cce', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_cce)
#        layer_cce = iface.activeLayer()
        layer_cce2 = QgsVectorLayer(SourceFile2 + 'boundary_cce.shp','boundary_cce', 'ogr')
#        QgsMapLayerRegistry.instance().addMapLayer(layer_cce2)
#        layer_cce2 = iface.activeLayer()
#        df_prv_record.loc[(df_prv_record.AD_CODE == AD_CODE),'cce'] = int(layer_cce.featureCount())
        if int(layer_cce.featureCount()) != int(layer_cce2.featureCount()):
            print("bau tgts")
            print(int(layer_cce.featureCount()) - int(layer_cce2.featureCount()) )
    #    QgsVectorFileWriter.writeAsVectorFormat(layer_cce, OutputFile + "boundary_cce.shp", "utf-8", None, "ESRI Shapefile")

        QgsMapLayerRegistry.instance().removeAllMapLayers()
        n = n+1
#    df_prv_record= df_prv_record[['citycode', 'AD_CODE', 'AD_string', 'Province', 'Cityname', 'Distname', 'Tier', 'Ringtier', 'city', 'tgts', 'cce', 'inbound', 'outbound']]
#    from pandas import ExcelWriter
#    writer = ExcelWriter(path_dest +  file_prv + 'rd3_record.xlsx')
#    df_prv_record.to_excel(writer,file_prv,index=False)
#    writer.save()
#




