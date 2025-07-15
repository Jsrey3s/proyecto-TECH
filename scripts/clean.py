import os
import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from utils.paths import get_data_path

ruta_base = get_data_path('raw')

columnas_mapeo = {
    "FECH": ["FECH"],
    "PAIS": ["PAIS", "PAIS4"],
    "DEPTO": ["DPTOR4", "DEPTO", "DEPTO4", "DTOR4", "DPTO1"],
    "VIA": ["VIA", "VIA4", "via4"],
    "POSARA": ["POSARA", "POSARA4", "POSAR"],
    "UNIDAD": ["CODUNI4", "CODUNI2", "CODUNI"],
    "PNK": ["PNK", "PNK4"],
    "FOBDOL": ["FOBDOL4", "FOBDOL"],
    "AGRENA": ["AGRENA4", "AGRENA"],
    "FLETES": ["FLETES4", "FLETES"],
    "CANTIDAD": ["CANTIDA4", "CANTI"]
}

dataframes = []

for carpeta in os.listdir(ruta_base):
    ruta_expo = os.path.join(ruta_base, carpeta)
    if not (os.path.isdir(ruta_expo) and carpeta.startswith("Expo_")):
        continue

    print(f"\n📁 Procesando carpeta: {carpeta}")
    for archivo in os.listdir(ruta_expo):
        if not archivo.lower().endswith(".csv"):
            continue

        ruta_csv = os.path.join(ruta_expo, archivo)
        try:
            # Detectar separador
            with open(ruta_csv, 'r', encoding="latin1", errors="ignore") as f:
                primera_linea = f.readline()
                sep = ";" if primera_linea.count(";") > primera_linea.count(",") else ","

            # Leer todo el archivo sin usecols
            df = pd.read_csv(
                ruta_csv,
                sep=sep,
                encoding="latin1",
                low_memory=False,
                on_bad_lines="skip"
            )

            # Limpiar columnas incluyendo BOM, espacios y capitalizar
            df.columns = [col.encode('latin1').decode('utf-8-sig').strip().upper() for col in df.columns]

            # Mapear columnas
            renombrar = {}
            for col_final, variantes in columnas_mapeo.items():
                for variante in variantes:
                    variante_limpia = variante.strip().upper()
                    for col_real in df.columns:
                        if col_real == variante_limpia:
                            renombrar[col_real] = col_final
                            break
                    if col_final in renombrar.values():
                        break

            df = df.rename(columns=renombrar)

            # Validación de FECH
            if "FECH" not in df.columns:
                print(f"❌ {archivo}: columna 'FECH' no encontrada, se omite.")
                continue

            # Completar columnas faltantes
            for col in columnas_mapeo:
                if col not in df.columns:
                    df[col] = None

            # Filtrar columnas relevantes
            df = df[[col for col in columnas_mapeo if col in df.columns]]

            # Procesar FECH
            df = df[df["FECH"].notna()]
            df["FECH"] = pd.to_numeric(df["FECH"], errors="coerce")
            df = df[df["FECH"].notna()]
            df["FECH"] = df["FECH"].astype("int64")

            df["AÑO"] = df["FECH"] // 100 + 2000
            df["MES"] = df["FECH"] % 100
            df["FECH"] = pd.to_datetime(
                df["AÑO"].astype(str) + "-" + df["MES"].astype(str).str.zfill(2),
                errors="coerce"
            ).dt.to_period("M")

            orden_final = [
                "FECH", "AÑO", "MES", "PAIS", "DEPTO", "VIA", "POSARA",
                "UNIDAD", "CANTIDAD", "PNK", "FOBDOL", "AGRENA", "FLETES"
            ]
            df = df[[col for col in orden_final if col in df.columns]]

            dataframes.append(df)
            print(f"✅ {archivo}: {df.shape[0]} filas procesadas.")

        except Exception as e:
            print(f"❌ Error en {archivo}: {str(e)}")


# Concatenar
df_total = pd.concat(dataframes, ignore_index=True)

columnas_num = ["CANTIDAD", "PNK", "FOBDOL", "AGRENA", "FLETES"]

for col in columnas_num:
    if col in df_total.columns:
        df_total[col] = (
            df_total[col]
            .astype(str)
            .str.strip()
            .str.replace(",", ".")
            .str.replace(r"[^\d.]", "", regex=True)
            .str.replace(r"\.(?=.*\.)", "", regex=True)
            .replace({"": np.nan, "nan": np.nan})
            .astype(float)
            .fillna(0.0)
        )


# Conversión limpia de columnas float innecesarias
for col in df_total.select_dtypes(include=["float", "float64", "float32"]).columns:
    if (df_total[col].dropna() % 1 == 0).all():
        df_total[col] = df_total[col].astype("Int64")

# Guardar CSV con coma
ruta_salida = get_data_path('cleaned', 'exportaciones_clean.csv')
df_total.to_csv(ruta_salida, index=False, encoding="utf-8-sig", sep=",")

# Resumen
print("\n🎯 Finalizado")
print(f"🔢 Total filas: {df_total.shape[0]}")
print(f"💾 Guardado en: {ruta_salida}")