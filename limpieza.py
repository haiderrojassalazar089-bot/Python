# ═══════════════════════════════════════════════════════════
# ARCHIVO: limpieza.py
# Funciones puras para limpieza de DataFrames
# No modifican el objeto original (buenas prácticas ETL)
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
from typing import List, Optional


# -----------------------------------------------------------
# 1. LIMPIAR NOMBRES DE COLUMNAS
# -----------------------------------------------------------
def limpiar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas:
    - minúsculas
    - sin espacios
    - sin caracteres raros
    """
    df_limpio = df.copy()

    df_limpio.columns = (
        df_limpio.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w_]", "", regex=True)
    )

    print("Columnas limpiadas")
    return df_limpio


# -----------------------------------------------------------
# 2. ELIMINAR DUPLICADOS
# -----------------------------------------------------------
def eliminar_duplicados(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Elimina filas duplicadas.
    """
    df_limpio = df.copy()

    n_antes = len(df_limpio)
    df_limpio = df_limpio.drop_duplicates(subset=subset, keep="first")
    n_despues = len(df_limpio)

    print(f"Duplicados eliminados: {n_antes - n_despues}")
    return df_limpio


# -----------------------------------------------------------
# 3. CORREGIR TIPOS DE DATOS
# -----------------------------------------------------------
def convertir_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte automáticamente columnas que parecen numéricas.
    No daña variables categóricas.
    """
    df_limpio = df.copy()

    for col in df_limpio.columns:
        convertido = pd.to_numeric(df_limpio[col], errors="coerce")

        # Solo reemplaza si realmente tiene estructura numérica
        if convertido.notna().sum() > 0:
            df_limpio[col] = convertido

    print("Tipos de datos corregidos")
    return df_limpio


# -----------------------------------------------------------
# 4. IMPUTACIÓN INTELIGENTE (CLAVE EN ENCUESTAS)
# -----------------------------------------------------------
def imputar_inteligente(df: pd.DataFrame) -> pd.DataFrame:
    """
    Imputa valores faltantes dependiendo del tipo de variable:

    - Variables continuas  -> MEDIANA
    - Variables categóricas codificadas -> MODA

    Detecta automáticamente el tipo según número de categorías.
    """
    df_limpio = df.copy()

    columnas_numericas = df_limpio.select_dtypes(include="number").columns

    for col in columnas_numericas:

        n_nulos = df_limpio[col].isna().sum()
        if n_nulos == 0:
            continue

        # Detectar si parece categórica (pocas categorías)
        if df_limpio[col].nunique() <= 10:
            valor = df_limpio[col].mode()[0]
            metodo = "moda (variable categórica)"
        else:
            valor = df_limpio[col].median()
            metodo = "mediana (variable continua)"

        df_limpio[col] = df_limpio[col].fillna(valor)

        print(f"{col}: {n_nulos} nulos imputados con {metodo}")

    print("Nulos imputados en columnas numéricas")
    return df_limpio


# -----------------------------------------------------------
# 5. ELIMINAR FILAS TOTALMENTE VACÍAS (SI EXISTEN)
# -----------------------------------------------------------
def eliminar_filas_vacias(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas completamente vacías.
    """
    df_limpio = df.copy()

    n_antes = len(df_limpio)
    df_limpio = df_limpio.dropna(how="all")
    n_despues = len(df_limpio)

    print(f"Filas completamente vacías eliminadas: {n_antes - n_despues}")
    return df_limpio


# -----------------------------------------------------------
# 6. PIPELINE DE LIMPIEZA (ORQUESTADOR)
# -----------------------------------------------------------
def limpieza_basica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ejecuta toda la limpieza básica en orden correcto.
    """

    print("\n--- INICIANDO LIMPIEZA ---")

    df = limpiar_columnas(df)
    df = eliminar_duplicados(df)
    df = eliminar_filas_vacias(df)
    df = convertir_numericas(df)
    df = imputar_inteligente(df)

    print("Proceso de limpieza finalizado")
    return df

# -----------------------------------------------------------
# 7. ALIAS DE COMPATIBILIDAD (para main.py antiguo)
# -----------------------------------------------------------
# Estas funciones permiten que scripts antiguos sigan funcionando
# sin cambiar nombres en main.py.

def estandarizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    return limpiar_columnas(df)


def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
    return convertir_numericas(df)


def imputar_nulos(df: pd.DataFrame, columnas=None) -> pd.DataFrame:
    # columnas se ignora porque la imputación ya es inteligente
    return imputar_inteligente(df)
