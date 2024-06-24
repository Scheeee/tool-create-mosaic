import arcpy

def create_mosaic_dataset(workspace, name, raster_path):
    try:
        arcpy.env.workspace = workspace
        raster_dataset = arcpy.Raster(raster_path)
        pixel_type_mapping = {
            'U1': '1_BIT',
            'U2': '2_BIT',
            'U4': '4_BIT',
            'U8': '8_BIT_UNSIGNED',
            'S8': '8_BIT_SIGNED',
            'U16': '16_BIT_UNSIGNED',
            'S16': '16_BIT_SIGNED',
            'U32': '32_BIT_UNSIGNED',
            'S32': '32_BIT_SIGNED',
            'F32': '32_BIT_FLOAT',
            'F64': '64_BIT'
        }

        if raster_dataset.pixelType in pixel_type_mapping:
            pixel_type = pixel_type_mapping[raster_dataset.pixelType]
        else:
            raise ValueError(f"Tipo de pixel não suportado: {raster_dataset.pixelType}")

        if arcpy.Exists(name):
            arcpy.AddWarning(f"Um Mosaic Dataset com o nome '{name}' já existe.")
        else:
            arcpy.management.CreateMosaicDataset(workspace, name, raster_dataset.spatialReference, raster_dataset.bandCount, pixel_type)
            arcpy.AddMessage("Mosaic Dataset criado com sucesso.")
    except ValueError as ve:
        arcpy.AddError(f"Erro ao criar Mosaic Dataset: {str(ve)}") 
    except arcpy.ExecuteError:
        error_msg = arcpy.GetMessages(2)
        arcpy.AddError(f"Erro de execução no arcpy: {error_msg}")
           
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no Create_Mosaic: {str(e)}")
    arcpy.AddMessage("Processo de criação de Mosaic Dataset concluído.")
        

def add_rasters_to_mosaic_dataset(mdname, raster_path):
    try:
        if arcpy.Exists(mdname):
            arcpy.AddMessage(f"O Mosaic Dataset '{mdname}' já existe. Adicionando rasters...")
            arcpy.management.AddRastersToMosaicDataset(mdname, "Raster Dataset", raster_path,
                                                       duplicate_items_action="Overwrite duplicates",
                                                       update_cellsize_ranges="UPDATE_CELL_SIZES",
                                                       update_boundary="UPDATE_BOUNDARY")
            arcpy.AddMessage("Rasters adicionados com sucesso ao Mosaic Dataset.")
        else:
            arcpy.AddError(f"O Mosaic Dataset '{mdname}' não existe. Verifique o caminho ou crie o dataset antes de adicionar rasters.")

    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no add_rasters: {str(e)}")   

def define_overviews(mdname):
    try:
        arcpy.management.DefineOverviews(mdname, 0.1)
        arcpy.AddMessage(f"Overviews definidos com sucesso para o Mosaic Dataset '{mdname}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no overview: {str(e)}")

def build_overviews(mdname):
    try:
        arcpy.env.parallelProcessingFactor = 1
        arcpy.management.BuildOverviews(mdname)
        arcpy.AddMessage(f"Overviews construídos com sucesso para o Mosaic Dataset '{mdname}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def build_footprints(mdname):
    try:
        arcpy.management.BuildFootprints(mdname, "category = 1", "", "", "", "", "", "MAINTAIN_EDGES")
        arcpy.AddMessage(f"Footprints construídos com sucesso para o Mosaic Dataset '{mdname}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def copy_features(footprint):
    try:
        #arcpy.management.SelectLayerByAttribute(footprint, "category = 1")
        arcpy.management.CopyFeatures(footprint)
        arcpy.AddMessage("As features foram copiadas com sucesso.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def define_mosaic_dataset_no_data(mdname, raster_path):
    raster_dataset = arcpy.Raster(raster_path)
    num_bands = raster_dataset.bandCount
    band = ['ALL_BANDS', 0]
    try:
        arcpy.management.DefineMosaicDatasetNoData(mdname, num_bands, band)
        arcpy.AddMessage(f"NoData definido com sucesso para o Mosaic Dataset '{mdname}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")
