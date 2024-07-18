import arcpy
import os
import mosaic_dataset_functions 

# Função para definir os parâmetros da ferramenta
def get_parameter_info():
    params = []

    param = arcpy.Parameter(
        displayName="Nome do Mosaic Dataset", name="md_layer", datatype="GPMosaicLayer", parameterType="Required", direction="Input")
    params.append(param)

    param = arcpy.Parameter(
        displayName="Inserir footprint", name="footprint", datatype="GPBoolean", parameterType="Optional", direction="Input")
    param.value = False  # Valor padrão é False (não executar)
    params.append(param)

    param = arcpy.Parameter(
            displayName="Inserir Copy_features", name="copy_features", datatype="GPBoolean", parameterType="Optional", direction="Input")
    param.value = False  # Valor padrão é False (não executar)
    params.append(param)

    return params


def execute(parameters, messages):
    try:
        md_layer = arcpy.GetParameterAsText(0)
        footprint = arcpy.GetParameterAsText(1).lower() == 'true'  
        copy_features = arcpy.GetParameterAsText(2).lower() == 'true'  
                

        # Extrair apenas o nome do arquivo (último componente do caminho)
        nome_arquivo = os.path.basename(md_layer)

        # Juntar com o footprint
        name_footprint = os.path.join(nome_arquivo, "Footprint" )
                       
        arcpy.AddMessage(f"Caminho do Mosaico: {md_layer}")
        arcpy.AddMessage(f"footprint: {footprint}")
        arcpy.AddMessage(f"copy_features: {copy_features}")
        
        arcpy.AddMessage(f"nome footprint: {name_footprint}")
        
        if footprint:
            arcpy.AddMessage("footprint")
            mosaic_dataset_functions.build_footprints(md_layer)
            arcpy.AddMessage("footprint concluído com sucesso.")
        if copy_features:
            arcpy.AddMessage("copy_features")
            mosaic_dataset_functions.copy_features(md_layer, name_footprint, nome_arquivo) 
            arcpy.AddMessage("copy_features concluído com sucesso.")
        
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