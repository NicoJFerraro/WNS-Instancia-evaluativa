# test_parsers.py (temp testing file)
from src.parsers import parse_recetas

recetas = parse_recetas('inputs/Recetas.md')

print(f"Se encontraron {len(recetas)} recetas:")
for receta in recetas:
    print(f"\n- {receta['nombre']}")
    print(f"  Ingredientes: {len(receta['ingredientes'])}")
    for ing in receta['ingredientes']:
        print(f"    {ing['cantidad']}g de {ing['nombre']}")