# ═══════════════════════════════════════════════════════════
# ARCHIVO: main.py
# Script principal de limpieza
# ═══════════════════════════════════════════════════════════

import pandas as pd
from limpieza import (
    estandarizar_columnas,
    eliminar_duplicados,
    eliminar_filas_nulas,
    convertir_numericas
)

# -----------------------------------------------------------
# 1. Cargar la base de datos
# -----------------------------------------------------------

ruta = "data/PIB_Departamental_con_proyección_20260212.xlsx"

df = pd.read_excel(ruta, engine="openpyxl")

print(f"Dimensión original: {df.shape}")

# -----------------------------------------------------------
# 2. Limpieza básica
# -----------------------------------------------------------

df = estandarizar_columnas(df)
print("Columnas limpiadas")

df = eliminar_duplicados(df)

df = eliminar_filas_nulas(df)

df = convertir_numericas(df)

# -----------------------------------------------------------
# 3. Resultado final
# -----------------------------------------------------------

print(f"Dimensión final: {df.shape}")

# -----------------------------------------------------------
# 4. Guardar dataset limpio
# -----------------------------------------------------------

df.to_csv("data/pib_limpio.csv", index=False)

print("Archivo limpio guardado correctamente.")
