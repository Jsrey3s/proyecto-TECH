import pandas as pd
import sys
sys.path.append('..')
from utils.paths import get_data_path, get_file_path

# Rutas
exportaciones = get_file_path('cleaned', 'data')
paises = get_file_path('mappings', 'paises')
departamentos = get_file_path('mappings', 'departamentos')
vias = get_file_path('mappings', 'vias')
ruta_salida = get_data_path('cleaned', 'exportaciones.csv')

# Cargar archivo base
df = pd.read_csv(exportaciones, low_memory=False)

# Cargar archivos de mapeo
df_paises = pd.read_csv(paises)
df_departamentos = pd.read_csv(departamentos)
df_vias = pd.read_csv(vias)

# Crear diccionarios de mapeo
dict_paises = pd.Series(df_paises.Nombre.values, index=df_paises.Código).to_dict()
dict_departamentos = pd.Series(df_departamentos.Nombre.values, index=df_departamentos.Código).to_dict()
dict_vias = pd.Series(df_vias.Nombre.values, index=df_vias.Código).to_dict()

# Aplicar mapeo
df["PAIS"] = df["PAIS"].map(dict_paises).fillna("No Declarado")
df["DEPTO"] = df["DEPTO"].map(dict_departamentos)
df["VIA"] = df["VIA"].map(dict_vias)

df.to_csv(ruta_salida, index=False, encoding="utf-8-sig", sep=",")