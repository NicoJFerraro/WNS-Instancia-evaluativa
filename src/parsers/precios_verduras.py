# src/parsers/precios_verduras.py

import re
import pdfplumber as pdf
from src.parsers.utils import clean_and_convert_price

def parse_vegetables_prices(file_path):
    
    # read pdf file
    prices = {}

    try:
        with pdf.open(file_path) as pdf_file:
            for page in pdf_file.pages:
                text = page.extract_text()
                
                if not text:
                    continue

                regex_pattern = r'^([A-Za-záéíóúÁÉÍÓÚñÑ\s]+)\s+\$([\d.]+)'
                
                lines = text.split('\n')

                for line in lines:
                    match = re.match(regex_pattern, line)

                    if match:
                        vegetable_name = match.group(1).strip()
                        price_str = match.group(2)

                        price = clean_and_convert_price(price_str)

                        if price and vegetable_name:
                            # Filter out non-vegetable entries
                            common_descriptions = ['De estación', 'Fruto por kg', 'Hoja por kg', 
                                           'Raiz por kg', 'Tuberculo por kg', 'Built with',
                                           'Consulte por compras', 'Los precios pueden variar']

                            if not any(desc in vegetable_name for desc in common_descriptions):
                                prices[vegetable_name] = price
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        import traceback
        traceback.print_exc()
    return prices