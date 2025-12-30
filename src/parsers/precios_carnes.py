# src/parsers/precios_carnes.py

import pandas as pd
from src.parsers.utils import clean_and_convert_price

def parse_meat_prices(file_path):

    # Read excel file, return dictionary:
    # key: meat/fish name
    # value: price per kg
    # example: {'Asado de Tira': 1500.0, 'Merluza': 1200.0}

    try:
        df = pd.read_excel(file_path, header=None, skiprows=3)

        precios = {}

        posibles_headers = ['Carne Vacuna', 'Carne de Cerdo', 'Pollo', 'Corte', 'Precio (ARS/kg)', 'Tipo']

        for _, row in df.iterrows():
            corte_carne = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else None
            precio_corte_carne = row.iloc[3]

            if not corte_carne or corte_carne == 'nan' or corte_carne in posibles_headers:
                continue

            precio = clean_and_convert_price(precio_corte_carne)
            if precio is not None:
                precios[corte_carne] = precio

            corte_pescado = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else None
            precio_corte_pescado = row.iloc[6]

            if not corte_pescado or corte_pescado == 'nan' or corte_pescado in posibles_headers:
                continue

            precio = clean_and_convert_price(precio_corte_pescado)
            if precio is not None:
                precios[corte_pescado] = precio

        return precios 
    
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
        return {}