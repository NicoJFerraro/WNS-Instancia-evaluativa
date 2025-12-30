# src/parsers/recetas.py

import re

def parse_recetas(file_path):
    # Read md recipe file and return dictionary list
    # Each dictionary represents a recipe, with keys: 'title', 'name', 'ingredients'

    recetas = []

    with open(file_path, 'r', encoding='utf-8') as file:
        contenido = file.read()

    recetas_raw =  re.split(r'\n# ', contenido)

    if recetas_raw[0].strip() == '' or not recetas_raw[0].startswith('#'):
        recetas_raw = recetas_raw[1:]
    else:
        recetas_raw[0] = '#' + recetas_raw[0]

    for receta_texto in recetas_raw:
        if not receta_texto.strip():
            continue

        #Get recipe title
        lines = receta_texto.strip().split('\n')
        nombre_receta = lines[0].replace('#', '').strip()

        #Get ingredients
        ingredientes = []
        seccion_ingredientes = False

        for line in lines:
            if line.strip().startswith('##') and ('ingrediente' in line.lower() or line.strip() == '## Lista'):
                seccion_ingredientes = True
                continue
            
            if seccion_ingredientes:
                if line.startswith('##') and 'ingrediente' not in line.lower():
                    break

                if not line.strip() or line.strip().startswith('-') and len(line.strip()) == 1:
                    continue
                
                ingrediente = parse_ingrediente_linea(line)
                if ingrediente:
                    ingredientes.append(ingrediente)
    
        if nombre_receta and ingredientes:
            recetas.append({
                'nombre': nombre_receta,
                'ingredientes': ingredientes
            })
    
    return recetas

def parse_ingrediente_linea(line):
    #Parse a single ingredient line, then extracts quantity, unity and name.

    #Examples
    # 1kg de asado de tira
    # Merluza fresca 500g
    # 1,25kg de lomo
    # Bondiola 1,75kg

    line = line.strip()

    #Remove vignettes chars
    line = re.sub(r'^[-•]\s*', '', line)
    line = re.sub(r'^\d+\.\s*', '', line)
    line = re.sub(r'^[a-z]\.\s*', '', line, flags=re.IGNORECASE)

    #Search for quantity and unit patterns
    patron_cantidad = r'(\d+[.,]?\d*)\s*(kg|g)'
    match = re.search(patron_cantidad, line, re.IGNORECASE)

    if not match:
        return None
    
    cantidad_str = match.group(1).replace(',', '.')
    unidad = match.group(2)
    cantidad = float(cantidad_str)

    #Normalize units
    if unidad == 'kg':
        cantidad *= 1000
    
    #Get ingredient name
    nombre = re.sub(patron_cantidad, '', line).strip()
    nombre = re.sub(r'^de\s+','', nombre, flags=re.IGNORECASE)
    nombre = re.sub(r':\s*$', '', nombre)
    nombre = nombre.strip()

    if not nombre:
        return None
    
    return {
        'nombre': nombre,
        'cantidad': cantidad,
        'unidad': 'g'
    }