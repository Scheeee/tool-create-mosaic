import arcpy
import os
import mosaic_dataset_functions 

# Função para definir os parâmetros da ferramenta
def get_parameter_info():
    params = []

    # Parâmetro 1: Workspace
    param = arcpy.Parameter(
        displayName="Workspace", name="workspace", datatype="DEWorkspace", parameterType="Required", direction="Input")
    params.append(param)

    # Parâmetro 2: Nome do Mosaic Dataset
    param = arcpy.Parameter(
        displayName="Nome do Mosaic Dataset", name="md_name", datatype="GPString", parameterType="Required", direction="Input")
    params.append(param)

    # Parâmetro 3: Caminho para o Raster
    param = arcpy.Parameter(
        displayName="Caminho para o Raster", name="raster_path", datatype="DERasterDataset", parameterType="Required", direction="Input")
    params.append(param)

    param = arcpy.Parameter(displayName="Caminho para o diretório de rasters", name="raster_folder", datatype="Folder", parameterType="Required",direction="Input")

    # Parâmetro 4: Executar funções adicionais
    param = arcpy.Parameter(
        displayName="Inserir footprint", name="footprint", datatype="GPBoolean", parameterType="Optional", direction="Input")
    param.value = False  # Valor padrão é False (não executar)
    params.append(param)

        
    return params


def execute(parameters, messages):
    try:
        workspace = arcpy.GetParameterAsText(0)
        md_name = arcpy.GetParameterAsText(1)
        raster_path = arcpy.GetParameterAsText(2)
        raster_folder = arcpy.GetParameterAsText(3)
        footprint = arcpy.GetParameterAsText(4).lower() == 'true'  
        md_full_path = os.path.join(workspace, md_name)
        name_footprint = os.path.join(md_name, "Footprint")
       # cp_feature_class = "Footprint_CopyFeatures"
        arcpy.AddMessage(f"Workspace: {workspace}")
        arcpy.AddMessage(f"Nome do Mosaic Dataset: {md_name}")
        arcpy.AddMessage(f"Caminho para o Raster: {raster_path}")
        arcpy.AddMessage(f"Caminho para o Raster: {raster_folder}")
        arcpy.AddMessage(f"Caminho do Mosaico: {md_full_path}")
        arcpy.AddMessage(f"footprint: {footprint}")
                
        arcpy.AddMessage("0")
        mosaic_dataset_functions.create_mosaic_dataset(workspace, md_name, raster_path)
        arcpy.AddMessage("1")       
        mosaic_dataset_functions.add_rasters_to_mosaic_dataset(md_full_path, raster_folder)
        arcpy.AddMessage("2")
        mosaic_dataset_functions.define_overviews(md_full_path)
        arcpy.AddMessage("3") 
        mosaic_dataset_functions.build_overviews(md_full_path)
        arcpy.AddMessage("4")

        if footprint:
            arcpy.AddMessage("footprint")
            mosaic_dataset_functions.build_footprints(md_full_path)
            arcpy.AddMessage("5")
           # mosaic_dataset_functions.copy_features(name_footprint) 
           # arcpy.AddMessage("6")
           # mosaic_dataset_functions.define_mosaic_dataset_no_data(md_full_path, raster_path)
            arcpy.AddMessage("Processo concluído com sucesso.")
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
