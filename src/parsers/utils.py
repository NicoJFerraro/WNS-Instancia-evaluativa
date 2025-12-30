# src/parsers/utils.py

import pandas as pd

def clean_and_convert_price(value):
    if pd.isna(value):
        return None
    
    #if it is already a number
    if isinstance(value, (int, float)):
        if value < 0:
            return None
        
        if isinstance(value, float) and value != int(value):
            if value < 1000:
                resultado = int(value * 1000)
                return resultado
            else:
                return int(value)
        else:
            return int(value)

    price_str = str(value).strip()
    price_str = price_str.replace('$', '').strip()

    if not price_str or price_str =='nan':
        return None
    
    price_str = price_str.replace('.', '')

    try:
        return int(float(price_str))
    except (ValueError, TypeError):
        return None
