import pandas as pd

from eda import (
    reporte_estructura,
    reporte_nulos,
    reporte_duplicados,
    reporte_descriptivo
)

from limpieza import (
    estandarizar_columnas,
    eliminar_duplicados,
    eliminar_filas_vacias,
    convertir_tipos,
    imputar_nulos
)

# -------------------------------------------------
# 1. CARGAR BASE DE DATOS
# -------------------------------------------------

ruta = "data/EPM8_personas.xlsx"
df = pd.read_excel(ruta)

print("====================================")
print("BASE ORIGINAL")
print("====================================")
print(f"Dimensión original: {df.shape}")

# -------------------------------------------------
# 2. ANÁLISIS EXPLORATORIO (ANTES DE LIMPIAR)
# -------------------------------------------------

reporte_estructura(df)
reporte_nulos(df)
reporte_duplicados(df)
reporte_descriptivo(df)

print("\n--- INICIANDO LIMPIEZA ---")

# -------------------------------------------------
# 3. LIMPIEZA DE DATOS
# -------------------------------------------------

df = estandarizar_columnas(df)
print("Columnas estandarizadas")

df = eliminar_duplicados(df)
print("Duplicados eliminados")

df = eliminar_filas_vacias(df)
print("Filas completamente vacías eliminadas")

df = convertir_tipos(df)
print("Tipos de datos corregidos")

# Detectar columnas numéricas automáticamente
numericas = df.select_dtypes(include="number").columns

print(f"Columnas numéricas detectadas: {len(numericas)}")

df = imputar_nulos(df, numericas)
print("Nulos imputados")

# -------------------------------------------------
# 4. VALIDACIÓN DE LA IMPUTACIÓN (MUY IMPORTANTE)
# -------------------------------------------------

print("\n====================================")
print("VALIDACIÓN POST-LIMPIEZA")
print("====================================")

# Verificar si aún hay nulos
nulos_restantes = df.isna().sum().sum()
print(f"Total de NaN después de imputar: {nulos_restantes}")

# Comparar estadísticas antes y después
print("\nEstadísticas finales:")
print(df[numericas].describe())

# Ver cuántos ceros hay (para validar si eran imputaciones)
conteo_ceros = (df[numericas] == 0).sum().sum()
print(f"\nCantidad total de ceros en variables numéricas: {conteo_ceros}")

# -------------------------------------------------
# 5. EXPORTAR BASE LIMPIA
# -------------------------------------------------

print("\n====================================")
print("GUARDANDO ARCHIVO LIMPIO")
print("====================================")

print(f"Dimensión final: {df.shape}")

df.to_csv("data/personas_limpio.csv", index=False)

print("Archivo limpio guardado correctamente.")
