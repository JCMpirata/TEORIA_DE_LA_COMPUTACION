import re

"""
Módulo lexer:
Funciones para extraer enlaces e imágenes de HTML usando expresiones regulares.
"""

# Patrón para hiperenlaces <a href="...">texto</a>
_link_pattern = re.compile(
    r'<a\s+[^>]*href="([^\"]*)"[^>]*>(.*?)</a>',
    re.IGNORECASE | re.DOTALL
)

# Patrón para imágenes <img ...>
_img_pattern = re.compile(
    r'<img\s+([^>]*?)>',
    re.IGNORECASE | re.DOTALL
)

void_tags = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
}

def extract_links(html_text):
    """
    Extrae todas las URLs de hiperenlaces (<a href="...">texto</a>).
    Devuelve lista de diccionarios: {'Texto': texto, 'URL': href}.
    """
    links = []
    for href, inner in _link_pattern.findall(html_text):
        text = re.sub(r'\s+', ' ', inner).strip()
        links.append({'Texto': text, 'URL': href})
    return links


def extract_images(html_text):
    """
    Extrae todas las URLs de imágenes (<img ...>). Devuelve lista de dicts: {'SRC': src, 'ALT': alt}.
    """
    images = []
    for attrs in _img_pattern.findall(html_text):
        src_m = re.search(r'src="([^\"]*)"', attrs, re.IGNORECASE)
        alt_m = re.search(r'alt="([^\"]*)"', attrs, re.IGNORECASE)
        src = src_m.group(1) if src_m else ''
        alt = alt_m.group(1) if alt_m else ''
        images.append({'SRC': src, 'ALT': alt})
    return images

