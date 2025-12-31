# src/parsers/precios_carnes.py

import pandas as pd
from src.parsers.utils import clean_and_convert_price

MEAT_NAME_COL = 2
MEAT_PRICE_COL = 3
FISH_NAME_COL = 5
FISH_PRICE_COL = 6

def _process_corte(row, name_index, price_index, posibles_headers, precios):
    corte = str(row.iloc[name_index]).strip() if pd.notna(row.iloc[name_index]) else None
    precio_raw = row.iloc[price_index]
    
    if not corte or corte == 'nan' or corte in posibles_headers:
        return
    
    precio = clean_and_convert_price(precio_raw)
    if precio is not None:
        precios[corte] = precio

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
            _process_corte(row, MEAT_NAME_COL, MEAT_PRICE_COL, posibles_headers, precios)
            _process_corte(row, FISH_NAME_COL, FISH_PRICE_COL, posibles_headers, precios)

        return precios 
    
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        return {}
    except pd.errors.EmptyDataError as e:
        print(f"Error: Excel file is empty: {e}")
        return {}
    except pd.errors.ExcelFileError as e:
        print(f"Error reading Excel file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error reading Excel file: {e}")
        import traceback
        traceback.print_exc()
        return {}