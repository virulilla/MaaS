
# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
import datetime
import time
import os

##path = "D:/Proyecto/ESRI001_MAASEMT2019/Datos/Script/Proceso"
##FILE_GDB=os.path.join(path, "LineasEMT_WGS84.gdb")
FILE_GDB="D:/Proyecto/ESRI001_MAASEMT2019/Datos/Script/Proceso/LineasEMT_WGS84.gdb"
FICH_VELOCIDADES="D:/Proyecto/ESRI001_MAASEMT2019/Datos/Script/Proceso/velocidades_emt.info"

def ObtenerNumFranjas():
    numFranjas = 0

    desc = arcpy.Describe(FILE_GDB+'/bus_lines')
    for f in desc.fields:
        if f.name[:3] == 'D1F':
            #print(f.name)
            numFranjas = numFranjas + 1

    return numFranjas/2

numFranjas = ObtenerNumFranjas()
print('Numero franjas = ' + str(numFranjas))
aCampos = ["LINEA"]
nombreCampo = ""
for d in range(7):
    kk = 0
    for f in range(numFranjas):
        nombreCampo = "D" + str(d+1) + "F" + str(f+1) + "HORAS"
        aCampos.append(nombreCampo)
        nombreCampo = "D" + str(d+1) + "F" + str(f+1) + "VEL"
        aCampos.append(nombreCampo)

ficheroVelocidades = open(FICH_VELOCIDADES,'w')
nroCampos = len(aCampos)
lineaAct = None
lineaAnt = None
diaAct = None
diaAnt = None

cursorSearch = arcpy.da.SearchCursor(FILE_GDB+'/bus_lines', aCampos, sql_clause=(None, "ORDER BY LINEA ASC"))
for fila in cursorSearch:
    lineaAct = fila[0]
    if lineaAct != lineaAnt:
        lineaAnt = lineaAct
        filaStr = ""
        diaAnt = None
        for indCampo in range(nroCampos):
            if indCampo > 0:
                diaAct = aCampos[indCampo][1:2]
                if diaAnt == None:
                    diaAnt = diaAct

                if (diaAct != diaAnt) or (indCampo == nroCampos - 1):
                    if (indCampo == nroCampos - 1):
                        filaStr = filaStr + str(fila[indCampo]) + " "
                    ficheroVelocidades.write(filaStr[:-1] + '\n')
                    #ficheroVelocidades.flush()
                    filaStr = str(lineaAct) + ','
                filaStr = filaStr + str(fila[indCampo])
                if diaAct != diaAnt:
                    diaAnt = diaAct
                if diaAct == diaAnt:
                    filaStr = filaStr + ','
            else:
                filaStr = filaStr + str(fila[indCampo]) + ','

ficheroVelocidades.close()
