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

# print("Inicio", datetime.now().time())
gdb = "LineasEMT.gdb"
flag = False
while not flag:
    # path = input("Ubicación de " + gdb + ": ")

    #PONER AQUI lA PATH
    path = "D:\Proyecto\ESRI001_MAASEMT2019\Datos\Script\Proceso"
    arcpy.env.workspace = path
    if arcpy.Exists(gdb):
        flag = True
        arcpy.env.workspace = os.path.join(path, gdb)
    else:
        print("El directorio no contiene la gdb")

gdbWGS84 = os.path.join(path, "LineasEMT_WGS84.gdb")
if arcpy.Exists(gdbWGS84):
    arcpy.Delete_management(gdbWGS84)
arcpy.CreateFileGDB_management(path, "LineasEMT_WGS84")

arcpy.env.workspace = os.path.join(gdb, "ds")
srWGS84 = arcpy.SpatialReference(4326)
listaFC = ["here_streets_walk", "here_streets_bike", "bus_lines", "bus_lines_elevation", "here_streets_bike_elevation"]
listaFieldsDelete_busLines = ["OrdenTramo", "Descripcion", "CodLineaSAE", "CodLineaCRTM", "ValidadoCRTM", "SubLineaSAE",
                              "DenominacionSecundaria", "DescripcionSAE", "DescripcionMobile", "PAS",
                              "LongitudCalculadaSentidoIda", "LongitudCalculadaSentidoVuelta", "LongitudOficialSentidoIda",
                              "LongitudOficialSentidoVuelta", "PrioridadMin", "PrioridadMax", "CircuitoNeutralizado",
                              "UsarDenominacionSecundaria", "EtiquetaOpcional", "IdTipoRegulacion", "DenominacionA",
                              "DenominacionB", "PanelFrontalA", "PanelFrontalB", "PanelLateralA", "PanelLateralB",
                              "SeccionTopologia", "IDSeccion", "IdParadaInicio", "IdParadaFin", "IDLinea", "IDMacro",
                              "IDConfiguracion", "CodParadaInicio", "Sentido"]
listaFieldsDelete_walkBikes = ["SpeedCat", "FuncClass", "Paved", "Tollway", "Time_Zone", "DST_Exist", "TimeZoneID",
                               "RestrictCars", "RestrictBuses", "RestrictTaxis", "RestrictDeliveries", "RestrictTrucks",
                               "RestrictCarpools", "RestrictEmergencies", "RestrictThroughTraffic", "RestrictMotorcycles",
                               "ISOCountryCode", "CarpoolRoad", "ExpressLane"]

# ¡Importante!: Si una fc forma parte de otra estructura de datos avanzadas, la referencia
# espacial no se puede cambiar, por lo que hay que establecer como salida un shp o proyectar el dataset completo.
# En este caso se han copiado previamente las fc a la nueva gdb de manera que la proyección se hará sobre fc que no
# pertenecen a ninguna estructura de datos avanzada

# ¡Importante!: La entrada en un Join debe ser una layer o una vista de tabla; no puede ser una fc o tabla.
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
##        arcpy.DeleteField_management(fc, listaFieldsDelete_busLines)
        arcpy.AddField_management(fc, "METERS", "FLOAT", field_scale=3)
        for field in arcpy.ListFields(fc):
            if field.name == "METERS":
                # arcpy.CalculateGeometryAttributes_management(fc, field.name + " LENGTH", "METERS")
                arcpy.CalculateField_management(fc, field.name, '!shape.length@meters!', "PYTHON")
                break
        fcLayer = fc + "_layer"
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        selectionLineNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "LINEA IS NULL")
        # selectionLineNull = arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", "LINEA IS NULL")
        arcpy.CalculateField_management(selectionLineNull, "LINEA", 0, "PYTHON")
        selectionNameNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "NAME IS NULL")
        # selectionNameNull = arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", "NAME IS NULL")
        arcpy.CalculateField_management(selectionNameNull, "NAME", "\"Servicios especiales\"", "PYTHON")
    elif fc == "here_streets_walk" or fc == "here_streets_bike":
##        arcpy.DeleteField_management(fc, listaFieldsDelete_walkBikes)
        arcpy.AddField_management(fc, "METROS", "FLOAT", field_scale=3)
        for field in arcpy.ListFields(fc):
            if field.name == "METROS":
                # arcpy.CalculateGeometryAttributes_management(fc, field.name + " LENGTH", "METERS")
                arcpy.CalculateField_management(fc, field.name, '!shape.length@meters!', "PYTHON")
                break
    elif fc == "here_streets_bike_elevation":
        fcLayer = fc + "_layer"
        fcBasesBiciMad = os.path.join(path, gdb, "BasesBiciMad")
        fcBasesBiciMadLayer = fcBasesBiciMad + "_layer"
        arcpy.AddField_management(fc, "IDSTATION", "TEXT", field_length=4)
        arcpy.AddField_management(fc, "IDESTACION", "LONG")
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        arcpy.MakeFeatureLayer_management(fcBasesBiciMad, fcBasesBiciMadLayer)
        arcpy.AddJoin_management(fcLayer, "OBJECTID", fcBasesBiciMadLayer, "OBJECTID")
        print("El campo \"name\" no es unico para cada entidad. No es válido como clave.")
        # arcpy.AddField_management(fcLayer, "AUX", "TEXT")
        # arcpy.CalculateField_management(fcLayer, "AUX", "!NAME![10:]", "PYTHON")
        # arcpy.AddJoin_management(fcLayer, "AUX", fcBasesBiciMadLayer, "name")
        # arcpy.DeleteField_management(fcLayer, "AUX")

        arcpy.CalculateField_management(fcLayer, "here_streets_bike_elevation.IDSTATION",
                                        "str(!BasesBiciMad.STATION_ID!).zfill(4)", "PYTHON")
        arcpy.RemoveJoin_management(fcLayer)
        arcpy.JoinField_management(fcLayer, "OBJECTID", fcBasesBiciMadLayer, "OBJECTID", "STATION_ID")
        # arcpy.JoinField_management(fcLayer, "AUX", fcBasesBiciMadLayer, "name", "STATION_ID")
        arcpy.CalculateField_management(fcLayer, "IDESTACION", "!STATION_ID!", "PYTHON")
        arcpy.DeleteField_management(fcLayer, "STATION_ID")
    elif fc == "bus_lines_elevation":
        fcLayer = fc + "_layer"
        emtPublic = os.path.join(path, "EMTPUBLIC.gdb")
        fcParadasAutobus = os.path.join(path, emtPublic, "ParadasAutobus")
        fcParadasAutobusLayer = fcParadasAutobus + "_layer"
        # fcParadasAutobus = os.path.join(path, gdb, "ParadasAutobus")
        arcpy.AddField_management(fc, "DESCRIP", "TEXT")
        arcpy.MakeFeatureLayer_management(fc, fcLayer)
        arcpy.MakeFeatureLayer_management(fcParadasAutobus, fcParadasAutobusLayer)
        arcpy.AddJoin_management(fcLayer, "CodParada", fcParadasAutobusLayer,
                                 "CodParada")
        arcpy.CalculateField_management(fcLayer, "bus_lines_elevation.DESCRIP",
                                        "!ParadasAutobus.Descripcion!", "PYTHON")
        arcpy.RemoveJoin_management(fcLayer)
        selectionDescripNull = arcpy.SelectLayerByAttribute_management(fcLayer, "NEW_SELECTION", "DESCRIP IS NULL")
        # selectionDescripNull = arcpy.SelectLayerByAttribute_management(fc, "NEW_SELECTION", "DESCRIP IS NULL")
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
