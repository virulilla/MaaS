# coding: utf-8
import arcpy, os

path = "C://SyK//05_MaaS_concat//data"
gdb = "LineasEMT_PRO.gdb"
network_DS = "ds_ND"
outNALayerName = "Route"
impedance = "PRECIO"
tolerance = "100 Meters"
stopsShp = os.path.join(path, "Stops", "Stops.shp")
outNALayer_lyr = os.path.join(path, "Route.lyr")

arcpy.env.workspace = os.path.join(path, gdb, "ds")
arcpy.env.overwriteOutput = True

if arcpy.CheckExtension("network") == "Available":
    arcpy.CheckOutExtension("network")
else:
    raise arcpy.ExecuteError("Network Analyst Extension license is not available.")

# Se crea la capa de analisis de ruta y establece sus propiedades de analisis
outNALayer = arcpy.na.MakeRouteLayer(network_DS, outNALayerName, impedance)

# Se obtiene la capa del objeto resultado de MakeRouteLayer()
outNALayer = outNALayer.getOutput(0)

# Se obtienen las subcapas en la capa del objeto resultado de MakeRouteLayer()
subLayerNames = arcpy.na.GetNAClassNames(outNALayer)

# Se obtienen la capa 'Stops' de las subcapas
stopsLayerName = subLayerNames["Stops"]

# Se genera la vista de Stops.shp
arcpy.MakeTableView_management(stopsShp, "stops_view")

# Se añaden las localizaciones
arcpy.na.AddLocations(outNALayer, stopsLayerName, "stops_view", "", tolerance)

# Se soluciona la ruta
arcpy.na.Solve(outNALayer)

# Se almacena en disco el resultado del calculo ruta
arcpy.management.SaveToLayerFile(outNALayer, outNALayer_lyr)
