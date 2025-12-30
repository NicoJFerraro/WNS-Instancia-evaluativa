# src/parsers/__init__.py

from .recetas import parse_recipes, parse_ingrediente_linea
from .precios_carnes import parse_meat_prices
from .precios_verduras import parse_vegetables_prices

__all__ = [
    'parse_recipes',
    'parse_ingrediente_linea',
    'parse_meat_prices',
    'parse_vegetables_prices'
]