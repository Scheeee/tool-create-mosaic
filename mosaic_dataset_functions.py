import arcpy
import os
import re

def create_fileGDB(location, fgdb_name):
    try: 
        arcpy.management.CreateFileGDB(location, fgdb_name)
        arcpy.AddMessage("FileGeoDatabase criado com sucesso.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no create_fileGDB: {str(e)}")   

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
        

def add_rasters_to_mosaic_dataset(md_layer, raster_folder):
    filter_regex = r"REGEX:.*M\d{4}_D\d{8}_\d{4}\.tif*"
    success = False
    try:
        arcpy.AddMessage(f"Verificando a existência do Mosaic Dataset: {md_layer}")
        if arcpy.Exists(md_layer):
            arcpy.AddMessage(f"Mosaic Dataset encontrado: {md_layer}")
            result = arcpy.management.AddRastersToMosaicDataset(
                in_mosaic_dataset=md_layer,
                raster_type="Raster Dataset", 
                input_path= raster_folder,
                filter=filter_regex,
                duplicate_items_action="OVERWRITE_DUPLICATES",
                update_cellsize_ranges="UPDATE_CELL_SIZES",
                update_boundary="UPDATE_BOUNDARY"
            )
            success = True if result.getOutput(0) else False
        else:
            arcpy.AddMessage(f"O Mosaic Dataset '{md_layer}' não existe. Verifique o caminho ou crie o dataset antes de adicionar rasters.")
 
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS (ExecuteError): {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no add_rasters: {str(e)}") 
    return success

def define_overviews(md_layer):
    try:
        arcpy.management.DefineOverviews(md_layer, 0.1)
        arcpy.AddMessage(f"Overviews definidos com sucesso para o Mosaic Dataset '{md_layer}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro no overview: {str(e)}")

def build_overviews(md_layer):
    try:
        arcpy.env.parallelProcessingFactor = 1
        arcpy.management.BuildOverviews(md_layer)
        arcpy.AddMessage(f"Overviews construídos com sucesso para o Mosaic Dataset '{md_layer}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def build_footprints(md_layer):
    try:
        arcpy.management.BuildFootprints(md_layer, "category = 1", "", "", "", "", "", "MAINTAIN_EDGES")
        arcpy.AddMessage(f"Footprints construídos com sucesso para o Mosaic Dataset '{md_layer}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def copy_features(md_layer, footprint, nome_layer):
    try:

        arcpy.management.MakeMosaicLayer(md_layer)
        arcpy.management.SelectLayerByAttribute(nome_layer, "NEW_SELECTION", "category = 1")
        arcpy.management.CopyFeatures(footprint)
        arcpy.AddMessage("As features foram copiadas com sucesso.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def define_mosaic_dataset_no_data(md_layer, num_bands, bands_for_nodata_value):
    # raster_dataset = arcpy.Raster(raster_path)
    #band = ['ALL_BANDS', 0]
    try:
        arcpy.management.DefineMosaicDatasetNoData(md_layer, num_bands,  bands_for_nodata_value)
        arcpy.AddMessage(f"NoData definido com sucesso para o Mosaic Dataset '{md_layer}'.")
    except arcpy.ExecuteError as ee:
        arcpy.AddError(f"Erro do ArcGIS: {ee}")
    except Exception as e:
        arcpy.AddError(f"Ocorreu um erro: {str(e)}")

def publish_mosaic_web_layer(md_layer_path, name, summary, tags, portal_folder, server, folder):
    try:

        sharing_draft = arcpy.sharing.CreateSharingDraft("STANDALONE_SERVER", "IMAGE_SERVER", name, md_layer_path)
        sharing_draft.portalFolder = portal_folder
        sharing_draft.server = server
        sharing_draft.folderName = folder
        sharing_draft.summary = summary
        sharing_draft.tags = tags

     
        arcpy.AddMessage("Analisando o rascunho do serviço de mosaico...")
        analysis = sharing_draft.analyze()
        if analysis['errors'] == {}:
            arcpy.AddMessage("Análise concluída sem erros. Publicando o serviço...")

            
            arcpy.StageService_server(sharing_draft.filePath, out_folder='.')

            arcpy.UploadServiceDefinition_server(sharing_draft.filePath, server)
            
            arcpy.AddMessage("Serviço de mosaico publicado com sucesso.")
        else:
            arcpy.AddWarning(f"A análise do rascunho encontrou os seguintes erros: {analysis['errors']}")
        
    except Exception as e:
        arcpy.AddError(f"Erro ao publicar serviço de mosaico: {str(e)}")


def overwrite_mosaic_web_layer(service_name, md_layer_path):
    try:
       
        arcpy.server.OverwriteService(service_name, "STANDALONE_SERVER", md_layer_path)
        
        arcpy.AddMessage(f"Serviço de mosaico '{service_name}' sobrescrito com sucesso.")

    except Exception as e:
        arcpy.AddError(f"Erro ao sobrescrever serviço de mosaico '{service_name}': {str(e)}")


def publish_footprint_web_layer(footprint_path, name, summary, tags, portal_folder, server, folder):
    try:
     
        sharing_draft = arcpy.sharing.CreateSharingDraft("STANDALONE_SERVER", "FEATURE", name, footprint_path)
        sharing_draft.portalFolder = portal_folder
        sharing_draft.server = server
        sharing_draft.folderName = folder
        sharing_draft.summary = summary
        sharing_draft.tags = tags

 
        arcpy.AddMessage("Analisando o rascunho do serviço de footprint...")
        analysis = sharing_draft.analyze()
        if analysis['errors'] == {}:
            arcpy.AddMessage("Análise concluída sem erros. Publicando o serviço...")

            arcpy.StageService_server(sharing_draft.filePath, out_folder='.')
            arcpy.UploadServiceDefinition_server(sharing_draft.filePath, server)
            
            arcpy.AddMessage("Serviço de footprint publicado com sucesso.")
        else:
            arcpy.AddWarning(f"A análise do rascunho encontrou os seguintes erros: {analysis['errors']}")
        
    except Exception as e:
        arcpy.AddError(f"Erro ao publicar serviço de footprint: {str(e)}")


def overwrite_footprint_web_layer(service_name, footprint_path):
    try:
       
        arcpy.server.OverwriteService(service_name, "STANDALONE_SERVER", footprint_path)

        arcpy.AddMessage(f"Serviço de footprint '{service_name}' sobrescrito com sucesso.")

    except Exception as e:
        arcpy.AddError(f"Erro ao sobrescrever serviço de footprint '{service_name}': {str(e)}")

