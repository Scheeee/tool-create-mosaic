import arcpy
import mosaic_dataset_functions
import logging

 
def execute(parameters, messages):
    try:
        operation = arcpy.GetParameterAsText(0)
        md_layer_path = arcpy.GetParameterAsText(1)
        mosaic_name = arcpy.Describe(md_layer_path).basename
        footprint_path = f"AMD_{mosaic_name}_CAT"
        aprx = arcpy.mp.ArcGISProject("CURRENT")
        m = aprx.listMaps()[0]
        if operation == "Publicar Mosaico":
            name = arcpy.GetParameterAsText(2)
            summary = arcpy.GetParameterAsText(3)
            tags = arcpy.GetParameterAsText(4)
            portal_folder = arcpy.GetParameterAsText(5)
            
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
 
            mosaic_dataset_functions.publish_mosaic_web_layer(md_layer_path, name, summary, tags, server, folder)
         
        elif operation == "Sobrescrever Mosaico":
            service_name = arcpy.GetParameterAsText(2)
            server_url = "https://maps.itaipu.gov.br/image"  # URL do servidor onde o serviço será publicado

            arcpy.AddMessage(f"Operação selecionada: {operation}")
            arcpy.AddMessage(f"Nome do Serviço: {service_name}")
            arcpy.AddMessage(f"Caminho do Mosaic Dataset: {md_layer_path}")
            try:
                mosaic_dataset_functions.overwrite_mosaic_web_layer(service_name, md_layer_path, server_url)
            except Exception as e:
                arcpy.AddError(f"Ocorreu um erro ao obter o nome do serviço: {str(e)}")
                logging.error(f"Ocorreu um erro ao obter o nome do serviço: {str(e)}")

        
    
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
    arcpy.env.overwriteOutput = True  
    execute(None, None)
