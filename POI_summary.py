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
import json
import urllib
import math
def multi_single(filename, layer, alg="qgis:multiparttosingleparts", save=False):
    global OutputFile
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

df_map = pd.read_excel('C:\\Users\\base7005\\Documents\\\\Urban\\base\\CCE_2018W2UE_TrackingList.xlsx',sheetname="list18W2",encoding='gb18030',dtype={'citycode': np.str_, 'AD_CODE':np.str_})

path_dest =  'C:\\Users\\base7005\\Documents\\CityBoundary\\summary\\'
path_people = 'C:\\Users\\base7005\\Documents\\CityBoundary\\result\\Poi_results\\'
path_people = path_people.decode('utf-8')
path_dest = path_dest.decode('utf-8')


'''FOR CHECK'''
df_bau_city = pd.DataFrame(index=None, columns=None)
df_bau_tgts = pd.DataFrame(index=None, columns=None)
df_bau_cce = pd.DataFrame(index=None, columns=None)
df_inbound = pd.DataFrame(index=None, columns=None)
df_outbound = pd.DataFrame(index=None, columns=None)
global path_people, path, SourceFile
path_all = 'C:\\Users\\base7005\\Documents\\CityBoundary\\UTM_area\\rerun\\'
path_all = path_all.decode('utf-8')
files_all = os.listdir(path_all)
files_all.sort()

#path_new = 'C:\\Users\\base7005\\Documents\\CityBoundary\\result\\Poi_results\\浙江省\\'
#path_new = path_new.decode('utf-8')
#files_new = os.listdir(path_new)
#files_new.sort()

#
#
#path_old = 'C:\\Users\\base7005\\Documents\\CityBoundary\\byProvince\\江苏省\\'
#path_old = path_old.decode('utf-8')
#files_old = os.listdir(path_old)
#files_old.sort()
#
#missed = list(set(files_old) - set(files_new))

for province in files_all:
    n=0
    print(province)
    path = path_all + province + '\\'
    files = os.listdir(path)
    files.sort()
    for file in files:
        OutputFile = path + file + '\\'    
#        SourceFile = path_people + file + '\\'
        city=file.split("_",1)[0]
        dist = file.split("_",1)[1][:-7]
        AD_CODE = file[-6:]
        citycode = df_map.loc[df_map['AD_CODE']==AD_CODE,'citycode']
        citycode = int(citycode)
        citycode =str(citycode).zfill(4)
        print(AD_CODE)
        n=n+1
        
#        if os.path.exists(SourceFile + 'outbound_resident.shp'):
#            layer_boundary_grid= QgsVectorLayer(SourceFile + 'outbound_resident.shp','outbound_resident', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_boundary_grid, True)
#            cnt0 = int(layer_boundary_grid.featureCount())
#            if cnt0 <2:
#                print(AD_CODE + " has " + str(cnt0) + " features for outbounds")
#            layer_temp = multi_single("outbound_resident_single", layer_boundary_grid)
#            cnt1 = int(layer_temp.featureCount())
#            if cnt0 != cnt1:
#                print(AD_CODE + " outbound chk.")
#                print(cnt1 - cnt0)
#        elif os.path.exists(SourceFile + ' outbound_resident.shp'):
#            layer_boundary_grid= QgsVectorLayer(SourceFile + ' outbound_resident.shp',' outbound_resident', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_boundary_grid, True)
#            cnt0 = int(layer_boundary_grid.featureCount())
#            if cnt0 <2:
#                print(AD_CODE + " has " + str(cnt0) + " features for outbounds")
#            layer_temp = multi_single("outbound_resident_single", layer_boundary_grid)
#            cnt1 = int(layer_temp.featureCount())
#            if cnt0 != cnt1:
#                print(AD_CODE + " outbound chk.")
#                print(cnt1 - cnt0)
#
#        
#        if os.path.exists(SourceFile + 'inbound_resident.shp'):
#            layer_boundary_grid= QgsVectorLayer(SourceFile + 'inbound_resident.shp','inbound_resident', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_boundary_grid, True)
#            cnt0 = int(layer_boundary_grid.featureCount())
#            if cnt0 <2:
#                print(AD_CODE + " has " + str(cnt0) + " features for inbounds")
#            layer_temp = multi_single("inbound_resident_single", layer_boundary_grid)
#            cnt1 = int(layer_temp.featureCount())
#            if cnt0 != cnt1:
#                print(AD_CODE + " inbound chk.")
#                print(cnt1 - cnt0)
#        elif os.path.exists(SourceFile + ' inbound_resident.shp'):
#            layer_boundary_grid= QgsVectorLayer(SourceFile + ' inbound_resident.shp',' inbound_resident', 'ogr')
#            QgsMapLayerRegistry.instance().addMapLayer(layer_boundary_grid, True)
#            cnt0 = int(layer_boundary_grid.featureCount())
#            if cnt0 <2:
#                print(AD_CODE + " has " + str(cnt0) + " features for inbounds")
#            layer_temp = multi_single("inbound_resident_single", layer_boundary_grid)
#            cnt1 = int(layer_temp.featureCount())
#            if cnt0 != cnt1:
#                print(AD_CODE + " inbound chk.")
#                print(cnt1 - cnt0)
#
#        QgsMapLayerRegistry.instance().removeAllMapLayers()
        
        
        if os.path.exists(OutputFile+"Bau_city_utm.csv"):
            df_city = pd.DataFrame.from_csv(OutputFile+"Bau_city_utm.csv", index_col='block_id')
            df_city["AD_CODE"] = AD_CODE
            df_bau_city=df_bau_city.append(df_city)
        elif os.path.exists(OutputFile+" Bau_city_utm.csv"):
            df_city = pd.DataFrame.from_csv(OutputFile+" Bau_city_utm.csv", index_col='block_id')
            df_city["AD_CODE"] = AD_CODE
            df_bau_city=df_bau_city.append(df_city)
        else:
            print(str(AD_CODE) + ' have no BAU_city file')
        
        if os.path.exists(OutputFile+"Bau_tgts_utm.csv"):
            df_tgts = pd.DataFrame.from_csv(OutputFile+"Bau_tgts_utm.csv", index_col='block_id')
            df_tgts["AD_CODE"] = AD_CODE
            df_bau_tgts=df_bau_tgts.append(df_tgts)
        elif os.path.exists(OutputFile+" BBau_tgts_utm.csv"):
            df_tgts = pd.DataFrame.from_csv(OutputFile+" Bau_tgts_utm.csv", index_col='block_id')
            df_tgts["AD_CODE"] = AD_CODE
            df_bau_tgts=df_bau_tgts.append(df_tgts)
        else:
            print(str(AD_CODE) + ' have no BAU_tgts file')
        
        if os.path.exists(OutputFile+"Bau_cce_utm.csv"):
            df_cce = pd.DataFrame.from_csv(OutputFile+"Bau_cce_utm.csv", index_col='block_id')
            df_cce["AD_CODE"] = AD_CODE
            df_bau_cce=df_bau_cce.append(df_cce)
        elif os.path.exists(OutputFile+" Bau_cce_utm.csv"):
            df_cce = pd.DataFrame.from_csv(OutputFile+" Bau_cce_utm.csv", index_col='block_id')
            df_cce["AD_CODE"] = AD_CODE
            df_bau_cce=df_bau_cce.append(df_cce)
        else:
            print(str(AD_CODE) + ' have no BAU_cce file')
    
    print(n)

        if os.path.exists(SourceFile+"fin_in_people.csv"):
            df_inpeople = pd.DataFrame.from_csv(SourceFile+"fin_in_people.csv", index_col='new_id')
            df_inpeople2 =pd.DataFrame(df_inpeople.groupby(level=0)['area'].agg('sum').reset_index(name='area'))
            df_inpeople2.set_index('new_id',inplace=True)
        elif os.path.exists(SourceFile+" fin_in_people.csv"):
            df_inpeople = pd.DataFrame.from_csv(SourceFile+" fin_in_people.csv", index_col='new_id')
            df_inpeople2 =pd.DataFrame(df_inpeople.groupby(level=0)['area'].agg('sum').reset_index(name='area'))
            df_inpeople2.set_index('new_id',inplace=True)
        else:
            pass

        if os.path.exists(SourceFile+"fin_out_people.csv"):
            df_outpeople = pd.DataFrame.from_csv(SourceFile+"fin_out_people.csv", index_col='new_id')
            df_outpeople2 =pd.DataFrame(df_outpeople.groupby(level=0)['area'].agg('sum').reset_index(name='area'))
            df_outpeople2.set_index('new_id',inplace=True)
        elif os.path.exists(SourceFile+" fin_out_people.csv"):
            df_outpeople = pd.DataFrame.from_csv(SourceFile+" fin_out_people.csv", index_col='new_id')
            df_outpeople2 =pd.DataFrame(df_outpeople.groupby(level=0)['area'].agg('sum').reset_index(name='area'))
            df_outpeople2.set_index('new_id',inplace=True)
        else:
            pass

        if os.path.exists(OutputFile+"Unv_grid_inbound.csv"):
            df_in = pd.DataFrame.from_csv(OutputFile+"Unv_grid_inbound.csv", index_col='new_id')
            df_intemp = pd.DataFrame.from_csv(OutputFile+"inbound_poires.csv", index_col='new_id')
            df_in['area'] = df_intemp['area']
            df_in.loc[(df_in['shopping'] > 0) & (df_in['areapl'].isna()) & (df_in['Resident']>0), 'areapl'] = df_intemp['area']
            df_in.loc[df_in['area'] < df_in['areapl'], 'areapl'] = df_in['area']
            df_in.to_csv(OutputFile + 'Unv_grid_inbound' + '.csv')
            df_inbound=df_inbound.append(df_in)
        elif os.path.exists(OutputFile+" Unv_grid_inbound.csv"):
            df_in = pd.DataFrame.from_csv(OutputFile+" Unv_grid_inbound.csv", index_col='new_id')
            df_intemp = pd.DataFrame.from_csv(OutputFile+" inbound_poires.csv", index_col='new_id')
            df_in['area'] = df_intemp['area']
            df_in.loc[(df_in['shopping'] > 0) & (df_in['areapl'].isna()) & (df_in['Resident']>0), 'areapl'] = df_intemp['area']
            df_in.loc[df_in['area'] < df_in['areapl'], 'areapl'] = df_in['area']
            df_in.to_csv(OutputFile + 'Unv_grid_inbound' + '.csv')
            df_inbound=df_inbound.append(df_in)
        else:
            pass

        if os.path.exists(OutputFile+"Unv_grid_outbound.csv"):
            df_out = pd.DataFrame.from_csv(OutputFile+"Unv_grid_outbound.csv", index_col='new_id')
            df_outtemp = pd.DataFrame.from_csv(OutputFile+"outbound_poires.csv", index_col='new_id')
    #        df_out['area'] = df_outtemp['area']
    #        df_out.loc[(df_out['shopping'] > 0) & (df_out['areapl'].isna()) & (df_out['Resident']>0), 'areapl'] = df_outtemp['area']
    #        df_out.loc[df_out['area'] < df_out['areapl'], 'areapl'] = df_out['area']
    #        df_out.to_csv(OutputFile + 'Unv_grid_outbound' + '.csv')
            df_outbound=df_outbound.append(df_out)
        if os.path.exists(OutputFile+" Unv_grid_outbound.csv"):
            df_out = pd.DataFrame.from_csv(OutputFile+" Unv_grid_outbound.csv", index_col='new_id')
            df_outtemp = pd.DataFrame.from_csv(OutputFile+" outbound_poires.csv", index_col='new_id')
            #df_out['area'] = df_outtemp['area']
            #df_out.loc[(df_in['shopping'] > 0) & (df_out['areapl'].isna()) & (df_out['Resident']>0), 'areapl'] = df_outtemp['area']
            #df_out.loc[df_out['area'] < df_out['areapl'], 'areapl'] = df_out['area']
    #        df_out.to_csv(OutputFile + 'Unv_grid_outbound' + '.csv')
            df_outbound=df_outbound.append(df_out)
        else:
            pass
    
    from pandas import ExcelWriter
    writer = ExcelWriter('C:\\Users\\base7005\\Documents\\CityBoundary\\UTM_area\\rerun\\' + province +  'summary.xlsx')

    df_bau_city.to_excel(writer,'bau_city')
    df_bau_tgts.to_excel(writer,'bau_tgts')
    df_bau_cce.to_excel(writer,'bau_cce')

    writer.save()


