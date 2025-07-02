import pandas as pd 
import yaml

# Cargar archivo config.yaml
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

# Acceder a rutas y parámetros
ruta_exportaciones = config["rutas"]["exportaciones"]
ruta_paises = config["rutas"]["paises"]
encoding = config["parametros"]["encoding"]

# Cargar los archivos con pandas
df_exportaciones = pd.read_csv(ruta_exportaciones, encoding=encoding)
df_paises = pd.read_csv(ruta_paises, encoding=encoding)

# Mostrar primeras filas como prueba
print(df_exportaciones.head())
print(df_paises.head())
