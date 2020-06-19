#-------------------------------------------------------------------------------
# Name:        4_Build
# Purpose:
#
# Author:      Sergio Infanzon
#
# Created:     12/06/2020
# Copyright:   (c) sykgis 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, os
from datetime import time

def build_function():

    path = "C:/SyK/05_MaaS_concat/data"
    gdb = os.path.join(path, "LineasEMT_PRE.gdb")
    arcpy.env.workspace = gdb

    arcpy.CheckOutExtension("Network")
    inNetworkDataset = "/ds/ds_ND"

    #Construimos la red. Si se ha cambiado la geometria, tardara unos 30 minutos. Sino es casi automatico
    arcpy.na.BuildNetwork(inNetworkDataset)

    #Backup de la GDB anterior
    hoy = time.strftime("%Y%m%d_%H%M%S")
    #print hoy
    in_data =  os.path.join(path, "LineasEMT_PRO.gdb")
    #print in_data
    out_data = os.path.join(path, "LineasEMT_PRO"+"_"+ hoy +".gdb")
    #print out_data
    os.rename(in_data, out_data)

    #TODO sleep

    #ahora, renombramos la GDB que hemos contruido en el proceso para pasarla a produccion
    in_data1 =  os.path.join(path, "LineasEMT_PRE.gdb")
    out_data1 = os.path.join(path, "LineasEMT_PRO.gdb")
    os.rename(in_data1, out_data1)

    print "fin"

