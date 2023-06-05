from data_preparation.process_data.functions import download, transform


URL = "https://www.indec.gob.ar/ftp/cuadros/economia/sh_ipc_aperturas.xls"
PATH = "index.csv"
SHEET_NAME = "Índices aperturas"
REGIONS = {"GBA": (5, 46),
           "Pampeana": (56, 44),
           "Noroeste": (105, 44),
           "Noreste": (154, 44),
           "Cuyo": (203,44),
           "Patagonia": (252,44)}
PATH_DATA_TRANSFORMED = "index_transformed.csv"

# download(URL, SHEET_NAME, PATH)
df = transform(PATH, REGIONS, PATH_DATA_TRANSFORMED)
print(df)