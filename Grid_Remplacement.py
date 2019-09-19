#!/usr/bin/env python
# -*- coding: utf-8 -*-
import signal
import sys
import json
import urllib
import math
import pandas as pd
import numpy as np
import os
import shutil
import processing
#from shapely import geometry
from osgeo import ogr
from qgis.analysis import QgsGeometryAnalyzer 
from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QInputDialog
from PyQt4.QtGui import *
from qgis.analysis import QgsGeometryAnalyzer 
import mmqgis
from qgis.analysis import QgsGeometryAnalyzer 
#from sextante.core.Sextante import Sextante


x_pi = 3.1415926535897932384626433832795 * 3000.0 / 180.0
pi = 3.1415926535897932384626433832795  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方
def count_unique_poi(filename, polygon,  points, alg="qgis:countuniquepointsinpolygon", save=False):
    '''
    #This is a warpper-function for "count unique points in polygon"
    '''
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

def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    """
#    if out_of_china(lng, lat):
#        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)

global path, OutputFile
path = 'C:\\Users\\base7005\\Documents\\CityBoundary\\batch3chk\\batch3_6\\广东省\\'
path = path.decode('utf-8')
#**************** 这个路径下不能有中文
path2 ='C:\\Users\\base7005\\Documents\\Grid_Check\\merge'
files = os.listdir(path)
#file = u'\u957f\u6625\u5e02_\u53cc\u9633\u533a_220112'
df_grid = pd.read_excel('C:\\Users\\base7005\\Documents\\Grid_check\\' + "testing.xlsx", sheetname="change",encoding='gb18030')
df_candidate = pd.read_excel('C:\\Users\\base7005\\Documents\\Grid_check\\' + "testing.xlsx", sheetname="candidate",encoding='gb18030')
df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\QGISimport\\map_file.xlsx',sheetname="Sheet1",encoding='gb18030',dtype={'citycode': np.str_})

CELLS = list(df_grid.MCELL.unique())
df_grid2 = df_grid.merge(df_map[['ADCODE','citycode']], how='left', right_on = 'ADCODE', left_on = 'ADCODE' )

OutputFile = 'C:\\Users\\base7005\\Documents\\Grid_Check\\done\\'
summary_change =pd.DataFrame()
for CELL in CELLS:
    df_grid_tmp = df_grid2[df_grid2.MCELL == CELL]
    ADCODES = list(df_grid_tmp.ADCODE.unique())
    
    df_candidate_tmp = df_candidate[df_candidate.MCELL == CELL]
    df_candidate_tmp= df_candidate_tmp.sort_values(by=['ADCODE', 'GRID_CHANGE','PSU_CTRL'], ascending=[True, True, True])
    for ADCODE in ADCODES:
        res = [k for k in files if str(ADCODE) in k]
        grid_path = path + res[0] + '\\'
        layer_boundary_grid= QgsVectorLayer(grid_path + 'fin_grid.shp','fin_grid', 'ogr')
        QgsMapLayerRegistry.instance().addMapLayer(layer_boundary_grid, True)
    
    layers = QgsMapLayerRegistry.instance().mapLayers().values()
    #all = [QgsMapLayerRegistry.instance().mapLayersByName('layer_1D')[0]]
    save_name = path2 + '\\' + str(CELL) + ".shp"
    processing.runalg("qgis:mergevectorlayers", layers, save_name)
    QgsMapLayerRegistry.instance().removeAllMapLayers()
    
    
    from TileLayerPlugin.tiles import BoundingBox, TileLayerDefinition
    plugin = qgis.utils.plugins.get("TileLayerPlugin")
    bbox = None
    layer_google = TileLayerDefinition(u"google",
                                 u"attribution",
                                 "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                                 zmin=1,
                                 zmax=18,
                                 bbox=bbox)
    plugin.addTileLayer(layer_google)
    
    layer_grid_merge = QgsVectorLayer(path2 + '\\' + str(CELL) + '.shp', str(CELL), 'ogr')
    QgsMapLayerRegistry.instance().addMapLayer(layer_grid_merge)
    layer_grid_merge = iface.activeLayer()
    layer_grid_merge.setCrs(QgsCoordinateReferenceSystem(4030))
    symbols = layer_grid_merge.rendererV2().symbols()
    symbol = symbols[0]
    symbol.setColor(QColor.fromRgb(110,135,212))
    qgis.utils.iface.mapCanvas().refresh() 
    qgis.utils.iface.legendInterface().refreshLayerSymbology(layer_grid_merge)
    extent = layer_grid_merge.extent()
    iface.mapCanvas().setExtent(extent)
    iface.mapCanvas().refresh()
    layer_grid_merge.setLayerTransparency(70)
    iface.mapCanvas().refresh()
#    df_rd1 = pd.DataFrame.from_csv('C:\\Users\\base7005\\Documents\\QGISimport\\result\\Grid_Check\\done\\' + "selection_check.csv", index_col=None)
#    df_rd1 = df_rd1.loc[(df_rd1.AD_code==int(AD_code))& (df_rd1.tag == 1)]
    #QgsVectorFileWriter.writeAsVectorFormat(layer_grid, OutputFile+"test", "ANSI", None, "CSV", layerOptions='GEOMETRY=AS_XYZ')
#    extent = layer_boundary_grid.extent()
#    iface.mapCanvas().setExtent(extent)
#        filename="infra_buffer_dsv"
#        save_name = OutputFile + filename + ".shp"
#        data_source = save_name
#        layer_name = filename
#        provider_name = "ogr"
#        layer_infra_dsv=iface.addVectorLayer(data_source, layer_name, provider_name)
    
#    data_source = OutputFile + "target_NoPeople.shp"
#    layer_name = "target_NoPeople"
#    provider_name = "ogr"
#    layer_target_NoPeople=iface.addVectorLayer(data_source, layer_name, provider_name)
    grids_change = list(df_grid_tmp.GRID_ID.unique())
    layer_selected_grid=QgsVectorLayer("Polygon", "selected_grid", "memory")
    for grid_change in grids_change:
        df_selection =df_candidate_tmp.loc[(df_candidate_tmp.GRID_CHANGE==grid_change),'GRID_ID']
        df_se = pd.DataFrame(df_selection)
        print("For grid " + str(grid_change) + ", you have " + str(len(df_selection)) + " grids to check")
        #feat_infra = layer_infra_dsv.getFeatures().next()
        change = pd.DataFrame({"grid_change": list( [str(grid_change)])})
        for i in df_selection:
            processing.runalg("qgis:selectbyattribute", layer_grid_merge, u'grid_id', 0, i)
            #layer_buffer = QgsGeometryAnalyzer().buffer(layer_boundary_grid, OutputFile2 + 'infra_buffer.shp', distance, False, False, -1)
            feature = layer_grid_merge.selectedFeatures()
            qgis.utils.iface.mapCanvas().zoomToSelected(layer_grid_merge)
            #pt = feature[0].geometry().centroid().asPoint()
            #p =geometry.Point(pt)
            #circle_buffer = p.buffer(distance)
            action = QInputDialog.getText(None,'Yes-1 or No-0','Should it be tagged?')
            while True: 
                try: 
                    action = int(action[0])
                    break
                except ValueError:
                    action = QInputDialog.getText(None,'Put a Number','1 or 0?')
                    action = action[0]
                if action==9:
                    processing.runalg("qgis:selectbyattribute",layer_grid_merge, u'grid_id', 0, i)
                    #layer_buffer = QgsGeometryAnalyzer().buffer(layer_boundary_grid, OutputFile2 + 'infra_buffer.shp', distance, False, False, -1)
                    feature =layer_grid_merge.selectedFeatures()
                    qgis.utils.iface.mapCanvas().zoomToSelected(layer_grid_merge)
                    action = QInputDialog.getText(None,'Yes-1 or No-0', 'Candidate: ' + str(i) + 'Should it be tagged?')
                    while True: 
                        try: 
                            action = int(action[0])
                            break
                        except ValueError:
                            action = QInputDialog.getText(None,'Put a Number','1 or 0?')
                            action = action[0]
            
            df_grid_tmp.loc[(df_grid_tmp.GRID_ID == i),'tag'] = action
            df_grid.loc[(df_grid.GRID_ID == i),'tag'] = action
            df_se.loc[(df_se.GRID_ID == i),'tag'] = action
            temp_data=layer_selected_grid.dataProvider()
            attr=layer_grid_merge.dataProvider().fields().toList()
            if action == 1:
                temp_data.addAttributes(attr)
                temp_data.addFeatures(feature)
                layer_selected_grid.updateFields()
                QgsMapLayerRegistry.instance().addMapLayer(layer_selected_grid)
                change['candidate'] = str(i)
                summary_change=summary_change.append(change)
                layer_grid_merge.removeSelection()
                break
            
            df_se.to_csv(OutputFile+'grid_change_'+ str(grid_change) + '.csv',encoding="gb18030")
            layer_grid_merge.removeSelection()
    
    save_name = OutputFile+"selected_grid2_"+str(CELL)+".shp"
    QgsVectorFileWriter.writeAsVectorFormat(layer_selected_grid, save_name, "utf-8", None, "ESRI Shapefile")
    
    data_source = save_name
    layer_name = "selected_grid_"+str(CELL)+".shp"
    provider_name = "ogr"
    layer_selected_grid =iface.addVectorLayer(data_source, layer_name, provider_name)
    QgsMapLayerRegistry.instance().removeAllMapLayers()

summary_change.to_csv('C:\\Users\\base7005\\Documents\\Grid_check\\' +'Grid_replacement' +'.csv',encoding="gb18030")


