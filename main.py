import arcpy
import LineasEMT, GenerarInfoVelEMT, CREAR_GDB_FINAL, Build

flag = 0
path_data = "C://SyK//05_MaaS_concat//data"
path_WGS84gdb = "C://SyK//05_MaaS_concat//data//LineasEMT_WGS84.gdb"
path_FICH_VELOCIDADES = "C://SyK//05_MaaS_concat//data//velocidades_emt.info"
path_PROgdb = "C://SyK//05_MaaS_concat//data//LineasEMT_PRO.gdb"

# if flag == 0:
#     flag = LineasEMT.LineasEMT_function(path_data)
# if flag == 1:
#     flag = GenerarInfoVelEMT.generarInfoVelEMT_function(path_WGS84gdb, path_FICH_VELOCIDADES)
# if flag == 2:
flag = CREAR_GDB_FINAL.crearGDBfinal_function(path_data)
# if flag == 3:
    # Build.build_function()