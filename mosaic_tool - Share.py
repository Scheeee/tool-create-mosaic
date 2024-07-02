import arcpy
import mosaic_dataset_functions
from arcgis.gis import GIS
 
def get_portal_folder(user):
    gis = GIS("home")
    user = gis.users.me
    return user.folders
 
def get_parameter_info():
    params = []
 
    param = arcpy.Parameter(
        displayName="Operação a Executar",
        name="operation",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
    )
    param.filter.list = ["Publicar Mosaico", "Sobrescrever Mosaico", "Publicar Footprint", "Sobrescrever Footprint"]
    params.append(param)
 
    # Parâmetros comuns a todas as operações
    common_params = [
        ("service_name", "Nome do Serviço", "GPString"),
        ("name", "Nome", "GPString"),
        ("summary", "Resumo", "GPString"),
        ("tags", "Tags", "GPString"),
        ("portal_folder", "Portal Folder", "GPString"),  # Keeping GPString to set folder names manually
        ("server", "DEGISServerConnection", "Server"),
        ("folder", "Folder", "GPString")
    ]
 
    for param_name, display_name, data_type in common_params:
        param = arcpy.Parameter(
            displayName=display_name,
            name=param_name,
            datatype=data_type,
            parameterType="Optional",
            direction="Input"
        )
        params.append(param)
 
    param = arcpy.Parameter(
        displayName="Caminho do Mosaic Dataset",
        name="md_layer_path",
        datatype="GPMosaicLayer",
        parameterType="Required",
        direction="Input"
    )
    params.append(param)
 
    return params
 
def execute(parameters, messages):
    try:
        operation = arcpy.GetParameterAsText(0)
        md_layer_path = arcpy.GetParameterAsText(1)
        footprint_path = arcpy.management.Describe(md_layer_path).footprint
 
        if operation == "Publicar Mosaico":
            name = arcpy.GetParameterAsText(2)
            summary = arcpy.GetParameterAsText(3)
            tags = arcpy.GetParameterAsText(4)
            portal_folder = arcpy.GetParameterAsText(5)
            if not portal_folder:
                user = GIS("home").users.me
                portal_folder = user.folders[0] if user.folders else None
            server = arcpy.GetParameterAsText(6)
            folder = arcpy.GetParameterAsText(7)
 
            arcpy.AddMessage(f"Operação selecionada: {operation}")
            arcpy.AddMessage(f"Caminho do Mosaic Dataset: {md_layer_path}")
            arcpy.AddMessage(f"Nome: {name}")
            arcpy.AddMessage(f"Resumo: {summary}")
            arcpy.AddMessage(f"Tags: {tags}")
            arcpy.AddMessage(f"Portal Folder: {portal_folder}")
            arcpy.AddMessage(f"Server: {server}")
            arcpy.AddMessage(f"Folder: {folder}")
 
            mosaic_dataset_functions.publish_mosaic_web_layer(md_layer_path, name, summary, tags, portal_folder, server, folder)
 
        elif operation == "Sobrescrever Mosaico":
            service_name = arcpy.GetParameterAsText(2)
            arcpy.AddMessage(f"Operação selecionada: {operation}")
            arcpy.AddMessage(f"Nome do Serviço: {service_name}")
            arcpy.AddMessage(f"Caminho do Mosaic Dataset: {md_layer_path}")
 
            mosaic_dataset_functions.overwrite_mosaic_web_layer(service_name, md_layer_path)
 
        elif operation == "Publicar Footprint":
            name = arcpy.GetParameterAsText(2)
            summary = arcpy.GetParameterAsText(3)
            tags = arcpy.GetParameterAsText(4)
            portal_folder = arcpy.GetParameterAsText(5)
            if not portal_folder:
                user = GIS("home").users.me
                portal_folder = user.folders[0] if user.folders else None
            server = arcpy.GetParameterAsText(6)
            folder = arcpy.GetParameterAsText(7)
 
            arcpy.AddMessage(f"Operação selecionada: {operation}")
            arcpy.AddMessage(f"Caminho do Footprint: {footprint_path}")
            arcpy.AddMessage(f"Nome: {name}")
            arcpy.AddMessage(f"Resumo: {summary}")
            arcpy.AddMessage(f"Tags: {tags}")
            arcpy.AddMessage(f"Portal Folder: {portal_folder}")
            arcpy.AddMessage(f"Server: {server}")
            arcpy.AddMessage(f"Folder: {folder}")
 
            mosaic_dataset_functions.publish_footprint_web_layer(footprint_path, name, summary, tags, portal_folder, server, folder)
 
        elif operation == "Sobrescrever Footprint":
            service_name = arcpy.GetParameterAsText(2)
 
            arcpy.AddMessage(f"Operação selecionada: {operation}")
            arcpy.AddMessage(f"Nome do Serviço: {service_name}")
            arcpy.AddMessage(f"Caminho do Footprint: {footprint_path}")
 
            mosaic_dataset_functions.overwrite_footprint_web_layer(service_name, footprint_path)
 
        arcpy.AddMessage("Processo de publicação e sobrescrita concluído com sucesso.")
 
    except arcpy.ExecuteError:
        error_msg = arcpy.GetMessages(2)
        arcpy.AddError(f"Erro de execução no arcpy: {error_msg}")
    except ValueError as ve:
        arcpy.AddError(f"Erro ao executar operação: {str(ve)}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")
 
if __name__ == "__main__":
    arcpy.env.overwriteOutput = True  # Permitir sobrescrever dados de saída
    execute(None, None)
