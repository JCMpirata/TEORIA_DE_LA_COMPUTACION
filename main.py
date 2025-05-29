import glob
import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lexer import extract_links, extract_images
from parser import is_balanced

"""
Módulo main:
Procesa localmente todos los archivos 'prueba*.html',
analiza una URL usando DOM,
y además procesa tres URLs fijas si no se pasa ningún argumento.
Genera archivos TXT con URLs, estadísticas de etiquetas y muestra balanceo.
"""

def save_list(items, filename):
    """Guarda una lista de strings en un archivo de texto, un item por línea."""
    with open(filename, 'w', encoding='utf-8') as f:
        for item in items:
            f.write(f"{item}\n")

def process_file(filepath):
    """Procesa un archivo HTML local: extrae enlaces, imágenes, cuenta etiquetas y comprueba balanceo."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extracción con regex
    links = [item['URL'] for item in extract_links(html)]
    images = [item['SRC'] for item in extract_images(html)]
    balanced = is_balanced(html)