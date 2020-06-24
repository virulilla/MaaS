#-------------------------------------------------------------------------------
# Name:        1_LineasEMT
# Purpose:
#
# Author:      Elena Salido
#
# Created:     12/06/2020
# Copyright:   (c) sykgis 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os
from datetime import datetime

arcpy.env.overwriteOutput = True
# print("Inicio", datetime.now().time())

gdb = "LineasEMT_1.gdb"

flag = False
while not flag:
    path = "C://SyK//05_MaaS_concat//data"
    arcpy.env.workspace = path
    if arcpy.Exists(gdb):
        flag = True
        arcpy.env.workspace = os.path.join(path, gdb)
    else:
        print("El directorio no contiene la gdb")

emtPublic = os.path.join(path, "EMTPUBLIC.gdb")
gdbWGS84 = os.path.join(path, "LineasEMT_WGS84.gdb")

if arcpy.Exists(gdbWGS84):
    arcpy.Delete_management(gdbWGS84)
arcpy.CreateFileGDB_management(path, "LineasEMT_WGS84")

arcpy.env.workspace = os.path.join(gdb, "ds")
srWGS84 = arcpy.SpatialReference(4326)
listaFC = ["here_streets_walk", "here_streets_bike", "bus_lines", "bus_lines_elevation", "here_streets_bike_elevation"]

# Importante: Si una fc forma parte de otra estructura de datos avanzadas, la referencia
# espacial no se puede cambiar, por lo que hay que establecer como salida un shp o proyectar el dataset completo.
# En este caso se han copiado previamente las fc a la nueva gdb de manera que la proyeccion se hara sobre fc que no
# pertenecen a ninguna estructura de datos avanzada

# Importante: La entrada en un Join debe ser una layer o una vista de tabla; no puede ser una fc o tabla.
# En los casos que ha sido necesario, se han creado layers antes de hacer cualquier Join.

for fc in listaFC:
    nFC_copy = os.path.join(gdbWGS84, fc + "_copy")
    nFC = os.path.join(gdbWGS84, fc)
    arcpy.CopyFeatures_management(fc, nFC_copy)
    for t in arcpy.ListTransformations(arcpy.Describe(fc).spatialReference, srWGS84):
        if t == "ED_1950_To_WGS_1984_41_NTv2_Spain_v2":
            arcpy.Project_management(nFC_copy, nFC, srWGS84, t)
            break
    arcpy.Delete_management(nFC_copy)

arcpy.env.workspace = gdbWGS84
for fc in arcpy.ListFeatureClasses():
    if fc == "bus_lines":
        arcpy.AddField_management(fc, "METERS", "FLOAT", field_scale=3)
        for field in arcpy.ListFields(fc):
            if field.name == "METERS":
                arcpy.CalculateField_management(fc, field.name, '!shape.length@meters!', "PYTHON")
                break
        fcLayer = fc + "_layer"
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        selectionLineNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "LINEA IS NULL")
        arcpy.CalculateField_management(selectionLineNull, "LINEA", 0, "PYTHON")
        selectionNameNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "NAME IS NULL")
        arcpy.CalculateField_management(selectionNameNull, "NAME", "\"Servicios especiales\"", "PYTHON")
    elif fc == "here_streets_walk" or fc == "here_streets_bike":
        arcpy.AddField_management(fc, "METROS", "FLOAT", field_scale=3)
        for field in arcpy.ListFields(fc):
            if field.name == "METROS":
                arcpy.CalculateField_management(fc, field.name, '!shape.length@meters!', "PYTHON")
                break
    elif fc == "here_streets_bike_elevation":
        fcLayer = fc + "_layer"
        fcBasesBiciMad = os.path.join(emtPublic, "MapaPublico", "BasesBiciMad")
        arcpy.CopyFeatures_management(fcBasesBiciMad, "BasesBiciMad")
        fcBasesBiciMadLayer = "BasesBiciMad_layer"
        arcpy.AddField_management(fc, "IDSTATION", "TEXT", field_length=4)
        arcpy.AddField_management(fc, "IDESTACION", "LONG")
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        arcpy.MakeFeatureLayer_management(fcBasesBiciMad, fcBasesBiciMadLayer)
        arcpy.AddField_management(fcLayer, "AUX", "TEXT")
        arcpy.CalculateField_management(fcLayer, "AUX", "!NAME![10:]", "PYTHON")
        arcpy.AddJoin_management(fcLayer, "AUX", fcBasesBiciMadLayer, "name")
        arcpy.CalculateField_management(fcLayer, "IDESTACION", "!BasesBiciMad.STATION_ID!", "PYTHON")
        arcpy.RemoveJoin_management(fcLayer)
        arcpy.Delete_management("BasesBiciMad")
        arcpy.CalculateField_management(fcLayer, "IDSTATION", "str(!IDESTACION!).zfill(4)", "PYTHON")
        arcpy.DeleteField_management(fcLayer, "AUX")
    elif fc == "bus_lines_elevation":
        fcLayer = fc + "_layer"
        fcParadasAutobus = os.path.join(emtPublic, "MapaPublico", "ParadasAutobus")
        arcpy.CopyFeatures_management(fcParadasAutobus, "ParadasAutobus")
        fcParadasAutobusLayer = "ParadasAutobus_layer"
        arcpy.AddField_management(fc, "DESCRIP", "TEXT")
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        arcpy.MakeFeatureLayer_management(fcParadasAutobus, fcParadasAutobusLayer)
        arcpy.AddJoin_management(fcLayer, "CodParada", fcParadasAutobusLayer, "CodParada")
        arcpy.CalculateField_management(fcLayer, "DESCRIP", "!ParadasAutobus.Descripcion!", "PYTHON")
        arcpy.RemoveJoin_management(fcLayer)
        arcpy.Delete_management("ParadasAutobus")
        selectionDescripNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "DESCRIP IS NULL")
        arcpy.CalculateField_management(selectionDescripNull, "DESCRIP", "\"\"", "PYTHON")
        arcpy.AddField_management(fc, "PRECIO", "DOUBLE")
        selectionName = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION",
                                                                       "NAME = 'Linea 5658' OR NAME = 'Linea 5662'")
        arcpy.CalculateField_management(selectionName, "PRECIO", '0.001', "PYTHON")
        selectionName = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION",
                                                                "NAME = 'Linea 5675' OR NAME = 'Linea 5676'")
        arcpy.CalculateField_management(selectionName, "PRECIO", '5', "PYTHON")
        selectionName = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION",
                        "NAME <> 'Linea 5658' AND NAME <> 'Linea 5662' AND NAME <> 'Linea 5675' AND NAME <> 'Linea 5676'")
        arcpy.CalculateField_management(selectionName, "PRECIO", '1.5', "PYTHON")

# print("Fin", datetime.now().time())
execfile(os.path.join("C://SyK//05_MaaS_concat//MaaS.git//S2_GenerarInfoVelEMT.py"))