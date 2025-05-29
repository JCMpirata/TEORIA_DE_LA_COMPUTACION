import re
import networkx as nx
import matplotlib.pyplot as plt

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

def render_automaton_image():
    """
    Dibuja con matplotlib el grafo del autómata finito que reconoce:
      - etiquetas <a href="...">texto</a>
      - etiquetas <img src="..." alt="...">
      - cualquier otro <…>
    """
    # Usamos un grafo dirigido simple (DiGraph) para soportar edge_labels
    G = nx.DiGraph()

    # Nodos
    G.add_nodes_from(['S', 'A', 'I', 'X'])

    # Aristas con etiquetas (no hay duplicados de par (u,v))
    edges = [
        ('S', 'A', '<a'),        # inicio <a
        ('A', 'A', '[^>]'),      # dentro de <a ...>
        ('A', 'S', '>'),         # cierre >
        ('S', 'I', '<img'),      # inicio <img
        ('I', 'I', '[^>]'),      # dentro de <img ...>
        ('I', 'S', '>'),         # cierre >
        ('S', 'X', '<'),         # inicio de cualquier otro <
        ('X', 'X', '[^>]'),      # caracteres hasta >
        ('X', 'S', '>'),         # cierre >
        ('S', 'S', '[^<]'),      # texto fuera de etiquetas
    ]
    G.add_weighted_edges_from([(u, v, 1) for u, v, _ in edges])  # weight genérico
    # Guardamos etiquetas aparte
    edge_labels = {(u, v): label for u, v, label in edges}

    # Posiciones manuales
    pos = {
        'S': (0, 0),
        'A': (1, 1),
        'I': (1, 0),
        'X': (1, -1),
    }

    # Dibujar nodos y etiquetas
    nx.draw_networkx_nodes(G, pos, node_size=1800, node_color='lightgray')
    nx.draw_networkx_labels(G, pos, font_size=12)

    # Dibujar aristas
    nx.draw_networkx_edges(
        G, pos,
        connectionstyle='arc3, rad=0.1',
        arrowsize=20
    )

    # Dibujar las etiquetas de las aristas
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=10,
        label_pos=0.5,
        rotate=False
    )

    plt.title("Autómata finito del Lexer HTML")
    plt.axis('off')
    plt.tight_layout()
    plt.show()