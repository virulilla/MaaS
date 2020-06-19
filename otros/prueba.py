import arcpy
gdb = "C://SyK//05_MaaS_concat//data//LineasEMT_PRO.gdb"
xml = "C://SyK//05_MaaS_concat//data//Schema.xml"
arcpy.ExportXMLWorkspaceDocument_management(gdb + "//ds",xml, "SCHEMA_ONLY", "NORMALIZED", False)