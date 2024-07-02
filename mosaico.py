import arcpy

# Define o workspace 
arcpy.env.workspace = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb"

# Caminho para o arquivo TIFF
tif_path = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Imagens de Exemplo\\M0683_transparent_mosaic_group1.tif"

# Caminho para o arquivo do projeto do ArcGIS
project_path = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.aprx"

try:
    # Inicializa o objeto ArcGISProject
    aprx = arcpy.mp.ArcGISProject(project_path)

    # Obtem o primeiro mapa no projeto
    map = aprx.listMaps()[0]

    # Cria um objeto RasterDataset a partir do arquivo TIFF
    raster_dataset = arcpy.Raster(tif_path)

    # Mapeia o tipo de pixel para o formato aceito pelo ArcGIS
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

    # Verifica se o tipo de pixel está no mapeamento
    if raster_dataset.pixelType in pixel_type_mapping:
        pixel_type = pixel_type_mapping[raster_dataset.pixelType]
    else:
        raise ValueError(f"Tipo de pixel não suportado: {raster_dataset.pixelType}")

    # Nome do Mosaico
    in_mosaicdataset_name = "teste2_script"

    # Verifica se o Mosaico já existe
    if arcpy.Exists(in_mosaicdataset_name):
        print(f"Um Mosaic Dataset com o nome '{in_mosaicdataset_name}' já existe.")
    else:
        #Se não existe, cria um novo
        arcpy.management.CreateMosaicDataset(arcpy.env.workspace, in_mosaicdataset_name, raster_dataset.spatialReference, raster_dataset.bandCount, pixel_type)
        print("Mosaic Dataset criado com sucesso.")

except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")

finally:
    # Salva e fecha o projeto do ArcGIS
    if 'aprx' in locals() or 'aprx' in globals():
        aprx.save()
        del aprx



import arcpy

# Caminho para o arquivo TIFF
tif_path = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Imagens de Exemplo\\M0683_transparent_mosaic_group1.tif"

# Caminho completo para o Mosaic Dataset
mdname = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb\\teste_script"

try:
    # Verifica se o Mosaic Dataset já existe
    if arcpy.Exists(mdname):
        print(f"O Mosaic Dataset '{mdname}' já existe. Adicionando rasters...")

        # Adiciona rasters ao Mosaic Dataset existente
        arcpy.management.AddRastersToMosaicDataset(mdname, "Raster Dataset", tif_path,
                                                   duplicate_items_action="Overwrite duplicates",
                                                   update_cellsize_ranges="UPDATE_CELL_SIZES",
                                                   update_boundary="UPDATE_BOUNDARY")
        
        print("Rasters adicionados com sucesso ao Mosaic Dataset.")
    else:
        print(f"O Mosaic Dataset '{mdname}' não existe. Verifique o caminho ou crie o dataset antes de adicionar rasters.")

except arcpy.ExecuteError as ee:
    # Captura mensagens de erro específicas do ArcGIS
    print(f"Erro do ArcGIS: {ee}")
except Exception as e:
    # Captura quaisquer outras exceções
    print(f"Ocorreu um erro: {str(e)}")


import arcpy

# Caminho completo para o Mosaic Dataset
mdname = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb\\teste_script"

# Tamanho do pixel para os overviews
pixel_size = 0.1

try:
    # Define overviews para o Mosaic Dataset
    arcpy.management.DefineOverviews(mdname, pixel_size)

    print(f"Overviews definidos com sucesso para o Mosaic Dataset '{mdname}'.")

except arcpy.ExecuteError as ee:
    # Captura mensagens de erro específicas do ArcGIS
    print(f"Erro do ArcGIS: {ee}")

except Exception as e:
    # Captura quaisquer outras exceções
    print(f"Ocorreu um erro: {str(e)}")


import arcpy

# Caminho completo para o Mosaic Dataset
mdname = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb\\teste_script"

try:
    # Define o fator de processamento paralelo
    arcpy.env.parallelProcessingFactor = 1

    # Constrói overviews para o Mosaic Dataset
    arcpy.management.BuildOverviews(mdname)

    print(f"Overviews construídos com sucesso para o Mosaic Dataset '{mdname}'.")

except arcpy.ExecuteError as ee:
    # Captura mensagens de erro específicas do ArcGIS
    print(f"Erro do ArcGIS: {ee}")

except Exception as e:
    # Captura quaisquer outras exceções
    print(f"Ocorreu um erro: {str(e)}")



import arcpy

# Caminho completo para o Mosaic Dataset
mdname = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb\\teste_script"
where_clause = "category = 1"
maintain_edges = "MAINTAIN_EDGES"

try:
   
    # Constrói footprints para o Mosaic Dataset com a cláusula where e mantém as bordas
    arcpy.management.BuildFootprints(mdname, where_clause, "", "", "", "", "", maintain_edges)

    print(f"Footprints construídos com sucesso para o Mosaic Dataset '{mdname}'.")

except arcpy.ExecuteError as ee:
    # Captura mensagens de erro específicas do ArcGIS
    print(f"Erro do ArcGIS: {ee}")

except Exception as e:
    # Captura quaisquer outras exceções
    print(f"Ocorreu um erro: {str(e)}")


import arcpy

# Define o caminho para o footprint
footprint = r"teste_script\Footprint"
cp_feature_class = r"C:\Users\sche7824\OneDrive - ITAIPU Binacional\Documentos\ArcGIS\Projects\mosaico_teste\mosaico_teste.gdb\Footprint_CopyFeatures"
where_clause = "category = 1"

try:
    # Seleciona por atributo
    arcpy.management.SelectLayerByAttribute(footprint, "NEW_SELECTION", where_clause)

    # Copia as features
    arcpy.management.CopyFeatures(footprint, cp_feature_class )

    print("As features foram copiadas com sucesso.")

except arcpy.ExecuteError as ee:
    # Captura mensagens de erro específicas do ArcGIS
    print(f"Erro do ArcGIS: {ee}")

except Exception as e:
    # Captura quaisquer outras exceções
    print(f"Ocorreu um erro: {str(e)}")


mdname = r"C:\\Users\\sche7824\\OneDrive - ITAIPU Binacional\\Documentos\\ArcGIS\\Projects\\mosaico_teste\\mosaico_teste.gdb\\teste_script"
num_bands = 4
band = ['ALL_BANDS', 0]

arcpy.management.DefineMosaicDatasetNoData(mdname, num_bands, band)
