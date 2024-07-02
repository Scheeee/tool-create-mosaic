import arcpy
import mosaic_dataset_functions
 
def get_parameter_info():
    params = []
 
    param = arcpy.Parameter(
        displayName="Nome do Mosaic Dataset", name="md_layer", datatype="GPMosaicLayer", parameterType="Required", direction="Input")
    params.append(param)
 
    param = arcpy.Parameter(
        displayName="Caminho para o diretório de rasters", name="raster_folder", datatype="Folder", parameterType="Required", direction="Input")
    params.append(param)
 
    param_bands_for_nodata_value = arcpy.Parameter(
        displayName="Valores NoData para as Bandas", name="bands_for_nodata_value", datatype="GPValueTable", parameterType="Required", direction="Input")
    param_bands_for_nodata_value.columns = [["GPString", "Banda"], ["GPString", "NoDataValue"]]
    params.append(param_bands_for_nodata_value)

    param = arcpy.Parameter(
        displayName="Laser", name="laser", datatype="GPBoolean", parameterType="Optional", direction="Input")
    param.value = False  
    params.append(param)
 
    return params
 
def execute(parameters, messages):
    try:
        md_layer = arcpy.GetParameterAsText(0)
        raster_folder = arcpy.GetParameterAsText(1)
        bands_for_nodata_value = arcpy.GetParameter(2)
        laser = arcpy.GetParameterAsText(3).lower() == 'true'  
 
        desc = arcpy.Describe(md_layer)
        num_bands = desc.bandCount
 
        arcpy.AddMessage(f"Nome do Mosaic Dataset: {md_layer}")
        arcpy.AddMessage(f"Caminho para o diretório de rasters: {raster_folder}")
        arcpy.AddMessage(f"Num. de bandas: {num_bands}")
 
        # Convertendo a ValueTable em uma lista de valores
        no_data_values = []
        for i in range(bands_for_nodata_value.rowCount):
            band = bands_for_nodata_value.getValue(i, 0)  # Primeira coluna é a Band
            no_data_value = bands_for_nodata_value.getValue(i, 1)  # Segunda coluna é o NoDataValue
            no_data_values.append(f"{band} {no_data_value}")
 
        # Converter a lista em uma string separada por vírgulas
        bands_for_nodata_value_str = ",".join(no_data_values)
        arcpy.AddMessage(f"Valores de NoData formatados: {bands_for_nodata_value_str}")
 
        arcpy.AddMessage("add_rasters_to_mosaic_dataset")
        if mosaic_dataset_functions.add_rasters_to_mosaic_dataset(md_layer, raster_folder):
            arcpy.AddMessage("Rasters adicionados ao mosaic dataset com sucesso!")
            
            arcpy.AddMessage("define_overviews")
            mosaic_dataset_functions.define_overviews(md_layer)
            arcpy.AddMessage("Definição de overviews concluída com sucesso.")
            if laser:
                arcpy.AddMessage("no_data")
                mosaic_dataset_functions.define_mosaic_dataset_no_data(md_layer, num_bands, bands_for_nodata_value_str)
                arcpy.AddMessage("Definição de NoData concluída com sucesso.")
 
                arcpy.AddMessage("build_overviews")
                mosaic_dataset_functions.build_overviews(md_layer)
                arcpy.AddMessage("Criação de overviews concluída com sucesso.")
            else: 
                arcpy.AddMessage("build_overviews")
                mosaic_dataset_functions.build_overviews(md_layer)
                arcpy.AddMessage("Criação de overviews concluída com sucesso.")   
                arcpy.AddMessage("no_data")
                mosaic_dataset_functions.define_mosaic_dataset_no_data(md_layer, num_bands, bands_for_nodata_value_str)
                arcpy.AddMessage("Definição de NoData concluída com sucesso.")
  
 
            arcpy.AddMessage("Todas as funções foram executadas com sucesso.")
        else:
            arcpy.AddWarning("Nenhum raster foi adicionado ao Mosaic Dataset. As funções subsequentes não serão executadas.")
 
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