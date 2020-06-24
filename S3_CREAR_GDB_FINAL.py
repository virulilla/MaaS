#-------------------------------------------------------------------------------
# Name:        3_CREAR_GDB_FINAL
# Purpose:
#
# Author:      Sergio Infanzon
#
# Created:     12/06/2020
# Copyright:   (c) sykgis 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy, os


print "arranca"

path =r"C:\SyK\05_MaaS_concat\data"

arcpy.env.workspace = path

arcpy.env.overwriteOutput = True

#esta es la base de datos funcional, de la que sacamos el esquema para crear la GDB nueva
gdb = os.path.join(path, "LineasEMT_PRO.gdb")

xml = os.path.join(path, "Schema.xml")

arcpy.ExportXMLWorkspaceDocument_management(gdb, xml, "SCHEMA_ONLY")

# #Creamos una GDB nueva vacia y le importamos el esquema de la GDB anterior
gdbFINAL = os.path.join(path, "LineasEMT_PRE.gdb")
if arcpy.Exists(gdbFINAL):
    arcpy.Delete_management(gdbFINAL)
arcpy.CreateFileGDB_management(path, "LineasEMT_PRE.gdb")

# arcpy.ImportXMLWorkspaceDocument_management(gdbFINAL, xml, "SCHEMA_ONLY")

#Importamos los datos a las nueva GDB

#INTERURBANO
interurbano = os.path.join(path, "LineasEMT_PRO.gdb\ds")
#Lineas
inputs=os.path.join(interurbano, "Interurbanos_Lineas")
target=os.path.join(gdbFINAL,"ds\Interurbanos_Lineas")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#accesos
inputs=os.path.join(interurbano, "Interurbanos_Accesos")
target=os.path.join(gdbFINAL,"ds\Interurbanos_Accesos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#elevations
inputs=os.path.join(interurbano, "Interurbanos_Elevation")
target=os.path.join(gdbFINAL,"ds\Interurbanos_Elevation")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#transbordos
inputs=os.path.join(interurbano, "Interurbanos_Transbordos")
target=os.path.join(gdbFINAL,"ds\Interurbanos_Transbordos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)


#METRO
metro = os.path.join(path, "LineasEMT_PRO.gdb\ds")
#Lineas
inputs=os.path.join(metro, "Metro_Lines")
target=os.path.join(gdbFINAL,"ds\Metro_Lines")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#accesos
inputs=os.path.join(metro, "Metro_Accesos")
target=os.path.join(gdbFINAL,"ds\Metro_Accesos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#elevations
inputs=os.path.join(metro, "Metro_lines_elevation")
target=os.path.join(gdbFINAL,"ds\Metro_lines_elevation")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#transbordos
inputs=os.path.join(metro, "Metro_transbordos")
target=os.path.join(gdbFINAL,"ds\Metro_transbordos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)

#METRO LIGERO
metro_ligero = os.path.join(path, "LineasEMT_PRO.gdb\ds")
#Lineas
inputs=os.path.join(metro_ligero, "Ligero_Lineas")
target=os.path.join(gdbFINAL,"ds\Ligero_Lineas")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#accesos
inputs=os.path.join(metro_ligero, "Ligero_Accesos")
target=os.path.join(gdbFINAL,"ds\Ligero_Accesos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#elevations
inputs=os.path.join(metro_ligero, "Ligero_Elevations")
target=os.path.join(gdbFINAL,"ds\Ligero_Elevations")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#transbordos
inputs=os.path.join(metro_ligero, "Ligero_Transbordos")
target=os.path.join(gdbFINAL,"ds\Ligero_Transbordos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)

#CERCANIAS
cercanias = os.path.join(path, "LineasEMT_PRO.gdb\ds")
#Lineas
inputs=os.path.join(cercanias, "Cercanias_Lineas")
target=os.path.join(gdbFINAL,"ds\Cercanias_Lineas")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#accesos
inputs=os.path.join(cercanias, "Cercanias_Accesos")
target=os.path.join(gdbFINAL,"ds\Cercanias_Accesos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#elevations
inputs=os.path.join(cercanias, "Cercanias_Elevations")
target=os.path.join(gdbFINAL,"ds\Cercanias_Elevations")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#transbordos
inputs=os.path.join(cercanias, "Cercanias_Transbordos")
target=os.path.join(gdbFINAL,"ds\Cercanias_Transbordos")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)


#De la GDB de EMT sacamos los datos de bus, bikes y walk
gdbEMT = os.path.join(path, "LineasEMT_WGS84.gdb")

#BUS
#Lineas
inputs=os.path.join(gdbEMT,"bus_lines")
target=os.path.join(gdbFINAL,"ds\\bus_lines")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
#elevations
inputs=os.path.join(gdbEMT, "bus_lines_elevation")
target=os.path.join(gdbFINAL, "ds\\bus_lines_elevation")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)

#BIKES
#lines
inputs=os.path.join(gdbEMT, "here_streets_bike")
target=os.path.join(gdbFINAL, "ds\here_streets_bike")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)
###elevations
inputs=os.path.join(gdbEMT, "here_streets_bike_elevation")
target=os.path.join(gdbFINAL, "ds\here_streets_bike_elevation")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)

#WALK
#lines
inputs=os.path.join(gdbEMT, "here_streets_walk")
target=os.path.join(gdbFINAL, "ds\here_streets_walk")
schema_type="NO_TEST"
arcpy.Append_management(inputs,target,schema_type)

arcpy.Delete_management(xml)

print "final"

execfile(os.path.join("C://SyK//05_MaaS_concat//MaaS.git//S4_Build.py"))