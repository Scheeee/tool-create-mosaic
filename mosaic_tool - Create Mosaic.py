import arcpy
import os
import mosaic_dataset_functions 

# Função para definir os parâmetros da ferramenta
def get_parameter_info():
    params = []

    # Pasta de criação do FGDB
    param = arcpy.Parameter(
        displayName="location", name="location", datatype="Folder", parameterType="Required", direction="Input")
    params.append(param)

    # Nome do fileGDB
    param = arcpy.Parameter(
        displayName="Nome do filegdb", name="fdgb_name", datatype="GPString", parameterType="Required", direction="Input")
    params.append(param)

    # Nome do Mosaic Dataset
    param = arcpy.Parameter(
        displayName="Nome do Mosaic Dataset", name="md_name", datatype="GPString", parameterType="Required", direction="Input")
    params.append(param)

     # Caminho para o Raster
    param = arcpy.Parameter(
        displayName="Caminho para o Raster", name="raster_path", datatype="DERasterDataset", parameterType="Required", direction="Input")
    params.append(param)


    return params


def execute(parameters, messages):
    try:
        location = arcpy.GetParameterAsText(0)
        md_name = arcpy.GetParameterAsText(2)
        fgdb_name = arcpy.GetParameterAsText(1)  
        raster_path = arcpy.GetParameterAsText(3)
        
        arcpy.AddMessage(f"Location: {location}")
        arcpy.AddMessage(f"Nome do Mosaic Dataset: {md_name}")
        arcpy.AddMessage(f"Nome do FGDB: {md_name}")
        
                
        arcpy.AddMessage("0")
        mosaic_dataset_functions.create_fileGDB(location, fgdb_name)
        arcpy.AddMessage("1")   
        if not fgdb_name.endswith(".gdb"):
            fgdb_name += ".gdb"
        workspace = os.path.join(location, fgdb_name)    

        arcpy.AddMessage(f"Caminho do FGDB: {workspace}")  
        mosaic_dataset_functions.create_mosaic_dataset(workspace, md_name, raster_path)
        arcpy.AddMessage("2")  
    except arcpy.ExecuteError:
        error_msg = arcpy.GetMessages(2)
        arcpy.AddError(f"Erro de execução no arcpy: {error_msg}")
    except ValueError as ve:
        arcpy.AddError(f"Erro ao criar Mosaic Dataset: {str(ve)}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")
 

if __name__ == "__main__":
    parameters = get_parameter_info()
    execute(parameters, None)
