import pandas as pd

df = pd.read_csv("exportaciones_v1.csv", low_memory=False)

# Cargar archivos de mapeo
df_paises = pd.read_csv("paises.csv")
df_departamentos = pd.read_csv("departamentos.csv")
df_vias = pd.read_csv("vias.csv")

# Crear diccionarios de mapeo
dict_paises = pd.Series(df_paises.Nombre.values, index=df_paises.Código).to_dict()
dict_departamentos = pd.Series(df_departamentos.Nombre.values, index=df_departamentos.Código).to_dict()
dict_vias = pd.Series(df_vias.Nombre.values, index=df_vias.Código).to_dict()

# Aplicar mapeo
df["PAIS"] = df["PAIS"].map(dict_paises).fillna("No Declarado")
df["DEPTO"] = df["DEPTO"].map(dict_departamentos)
df["VIA"] = df["VIA"].map(dict_vias)

df.to_csv("exportaciones.csv", index=False, encoding="utf-8-sig", sep=",")