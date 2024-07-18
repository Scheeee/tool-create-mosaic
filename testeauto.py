import arcpy
import os
import mosaic_dataset_functions 

def mosaic_tool(parameters, messages):
    try:
        folder = arcpy.GetParameterAsText(0)
        fgdb_name = os.path.basename(folder) + ".gdb"
        md_name = "mosaico"
        location = folder
        raster_folder = folder
        tif = os.path.join(folder, "mosaico.tif")
        bands_for_nodata_value = [['ALL_BANDS', 0]]
            
        # Verificação de parâmetros de entrada
        if not tif or not fgdb_name or not location or not md_name or not raster_folder:
            raise ValueError("Todos os parâmetros são obrigatórios.")
        
        # Criação do FGDB
        mosaic_dataset_functions.create_fileGDB(location, fgdb_name)
        if not fgdb_name.endswith(".gdb"):
            fgdb_name += ".gdb"
        workspace = os.path.join(location, fgdb_name)
        arcpy.AddMessage(f"Caminho do FGDB: {workspace}")

        # Criação do Mosaic Dataset
        mosaic_dataset_functions.create_mosaic_dataset(workspace, md_name, tif)
        md_layer = os.path.join(workspace, md_name)
        
        # Verificação da existência do Mosaic Dataset
        if not arcpy.Exists(md_layer):
            raise ValueError(f"O Mosaic Dataset '{md_layer}' não foi criado corretamente.")
        # Formatação dos valores de NoData
        desc = arcpy.Describe(md_layer)
        num_bands = desc.bandCount
        # no_data_values = []
        # for i in range(bands_for_nodata_value.rowCount):
        #     band = bands_for_nodata_value.getValue(i, 0)  # Primeira coluna é a Band
        #     no_data_value = bands_for_nodata_value.getValue(i, 1)  # Segunda coluna é o NoDataValue
        #     no_data_values.append(f"{band} {no_data_value}")
        # bands_for_nodata_value_str = ",".join(no_data_values)
        #arcpy.AddMessage(f"Valores de NoData formatados: {bands_for_nodata_value_str}")
        nome_arquivo = os.path.basename(md_layer)
        name_footprint = os.path.join(nome_arquivo, "Footprint")
        # Adição de rasters ao Mosaic Dataset
        arcpy.AddMessage("Adicionando rasters ao mosaic dataset")
        if mosaic_dataset_functions.add_rasters_to_mosaic_dataset(md_layer, raster_folder):
            arcpy.AddMessage("Rasters adicionados ao mosaic dataset com sucesso!")

            # Definição de overviews
            arcpy.AddMessage("Definindo overviews")
            mosaic_dataset_functions.define_overviews(md_layer)
            arcpy.AddMessage("Definição de overviews concluída com sucesso.")

            # Criação de overviews
            arcpy.AddMessage("Criando overviews")
            mosaic_dataset_functions.build_overviews(md_layer)
            arcpy.AddMessage("Criação de overviews concluída com sucesso.")

            # Definição de NoData
            arcpy.AddMessage("Definindo NoData")
            mosaic_dataset_functions.define_mosaic_dataset_no_data(md_layer, num_bands, bands_for_nodata_value)
            arcpy.AddMessage("Definição de NoData concluída com sucesso.")

            # Construção de footprints
            arcpy.AddMessage("Construindo footprints")
            mosaic_dataset_functions.build_footprints(md_layer)
            arcpy.AddMessage("Construção de footprints concluída com sucesso.")

            # Copiando features
            arcpy.AddMessage("Copiando features")
               
            mosaic_dataset_functions.copy_features(md_layer, name_footprint, nome_arquivo)
            arcpy.AddMessage("Cópia de features concluída com sucesso.")
        
    except arcpy.ExecuteError:
        error_msg = arcpy.GetMessages(2)
        arcpy.AddError(f"Erro de execução no arcpy: {error_msg}")
    except ValueError as ve:
        arcpy.AddError(f"Erro ao criar Mosaic Dataset: {str(ve)}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")


if __name__ == "__main__":
    arcpy.env.overwriteOutput = True  
    mosaic_tool(None, None)
