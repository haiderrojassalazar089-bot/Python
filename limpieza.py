# ═══════════════════════════════════════════════════════════
# ARCHIVO: limpieza.py
# Funciones puras de limpieza
# ═══════════════════════════════════════════════════════════

import pandas as pd
import numpy as np


def estandarizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia nombres de columnas: minúsculas, sin espacios.
    """
    df_limpio = df.copy()
    df_limpio.columns = (
        df_limpio.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("á", "a")
        .str.replace("é", "e")
        .str.replace("í", "i")
        .str.replace("ó", "o")
        .str.replace("ú", "u")
    )
    return df_limpio


def eliminar_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas duplicadas.
    """
    n_antes = len(df)
    df_limpio = df.drop_duplicates()
    n_despues = len(df_limpio)

    print(f"Duplicados eliminados: {n_antes - n_despues}")
    return df_limpio


def eliminar_filas_nulas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina filas completamente vacías.
    """
    n_antes = len(df)
    df_limpio = df.dropna(how="all")
    n_despues = len(df_limpio)

    print(f"Filas con nulos eliminadas: {n_antes - n_despues}")
    return df_limpio


def convertir_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte automáticamente a numéricas las columnas que parecen números.
    No afecta columnas de texto.
    """
    df_limpio = df.copy()

    for col in df_limpio.columns:
        # Intentar convertir; si no se puede, deja NaN en lo no convertible
        serie_convertida = pd.to_numeric(df_limpio[col], errors="coerce")

        # Solo reemplazar si realmente era una columna numérica
        if serie_convertida.notna().sum() > 0:
            df_limpio[col] = serie_convertida

    print("Columnas numéricas convertidas correctamente")

    return df_limpio
