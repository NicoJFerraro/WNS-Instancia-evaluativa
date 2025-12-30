# src/parsers/__init__.py

from .recetas import parse_recetas, parse_ingrediente_linea
from .precios_carnes import parse_precios_carnes
from .precios_verduras import parse_precios_verduras

__all__ = [
    'parse_recetas',
    'parse_ingrediente_linea',
    'parse_precios_carnes',
    'parse_precios_verduras'
]