import arcpy
import S1_LineasEMT, S2_GenerarInfoVelEMT, S3_CREAR_GDB_FINAL, S4_Build

flag = 0
path_data = "C://SyK//05_MaaS_concat//data"
path_WGS84gdb = "C://SyK//05_MaaS_concat//data//LineasEMT_WGS84.gdb"
path_FICH_VELOCIDADES = "C://SyK//05_MaaS_concat//data//velocidades_emt.info"

if flag == 0:
    flag = S1_LineasEMT.LineasEMT_function(path_data)
elif flag == 1:
    flag = S2_GenerarInfoVelEMT.generarInfoVelEMT_function(path_WGS84gdb, path_FICH_VELOCIDADES)
elif flag == 2:
    flag = S3_CREAR_GDB_FINAL.crearGDBfinal_function(path_data)
elif flag == 3:
    S4_Build.build_function(path_data)