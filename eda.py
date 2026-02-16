import pandas as pd

def reporte_estructura(df: pd.DataFrame) -> None:
    print("\n🔎 ESTRUCTURA DEL DATASET")
    print(df.info())

def reporte_nulos(df: pd.DataFrame) -> None:
    print("\n🔎 VALORES NULOS REALES")

    nulos = df.isna().sum()
    nulos = nulos[nulos > 0].sort_values(ascending=False)

    if len(nulos) == 0:
        print("No hay valores nulos en el dataset.")
    else:
        print(nulos)
        print(f"\nTotal de celdas con NA: {df.isna().sum().sum()}")

def reporte_duplicados(df: pd.DataFrame) -> None:
    print("\n🔎 DUPLICADOS")
    print(f"Filas duplicadas: {df.duplicated().sum()}")

def reporte_descriptivo(df: pd.DataFrame) -> None:
    print("\n🔎 DESCRIPCIÓN ESTADÍSTICA")
    print(df.describe(include="all"))
    


