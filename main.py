# main.py
import glob
import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from lexer import extract_links, extract_images, render_automaton_image
from parser import is_balanced

"""
Módulo main:
Procesa localmente todos los archivos 'prueba*.html',
analiza una URL usando DOM,
y además procesa tres URLs fijas si no se pasa ningún argumento.
Genera archivos TXT con URLs, estadísticas de etiquetas y muestra balanceo.
Además permite dibujar el grafo del autómata del lexer.
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
    
    # Estadísticas de etiquetas con BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    tags_to_count = ['a', 'img', 'br', 'div', 'li', 'ul', 'p', 'span', 'table', 'td', 'tr']
    stats = {tag: len(soup.find_all(tag)) for tag in tags_to_count}

    base = os.path.splitext(os.path.basename(filepath))[0]
    save_list(links, f"{base}_links.txt")
    save_list(images, f"{base}_images.txt")

    print(f"Procesado local '{base}':")
    print(f"- {len(links)} enlaces -> {base}_links.txt")
    print(f"- {len(images)} imágenes -> {base}_images.txt")
    print(f"- Balanceado: {'Sí' if balanced else 'No'}")
    print("- Estadísticas de etiquetas:")
    for tag, count in stats.items():
        print(f"  {tag}: {count}")
    print()

def process_url(url):
    """Procesa una URL: usa BeautifulSoup para extraer enlaces, imágenes, estadísticas de etiquetas y comprueba balanceo."""
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        html = resp.text
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return

    # Comprueba balanceo usando el HTML crudo
    balanced = is_balanced(html)

    soup = BeautifulSoup(html, 'html.parser')

    # Extraer enlaces e imágenes desde DOM
    a_tags = soup.find_all('a', href=True)
    img_tags = soup.find_all('img', src=True)
    links = [tag['href'] for tag in a_tags]
    images = [tag['src'] for tag in img_tags]

    # Guardar URLs
    parsed = urlparse(url)
    base = parsed.netloc.replace(':', '_')
    save_list(links, f"{base}_links.txt")
    save_list(images, f"{base}_images.txt")
    
    # Estadísticas de etiquetas
    tags_to_count = ['a', 'img', 'br', 'div', 'li', 'ul', 'p', 'span', 'table', 'td', 'tr']
    stats = {tag: len(soup.find_all(tag)) for tag in tags_to_count}

    print(f"Procesado URL '{url}':")
    print(f"- {len(links)} enlaces -> {base}_links.txt")
    print(f"- {len(images)} imágenes -> {base}_images.txt")
    print(f"- Balanceado: {'Sí' if balanced else 'No'}")
    print("- Estadísticas de etiquetas:")
    for tag, count in stats.items():
        print(f"  {tag}: {count}")
    print()
    
def main():
    parser = argparse.ArgumentParser(
        description='Procesar HTML local, web o URLs fijas: extraer enlaces, imágenes, balanceo y estadísticas. También dibujar el grafo del autómata.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file',
                       help='Archivo HTML o directorio con .html para procesar localmente')
    group.add_argument('-u', '--url',
                       help='URL de la página web a procesar con BeautifulSoup')
    group.add_argument('-g', '--graph', action='store_true',
                       help='Dibuja el grafo del autómata del lexer')
    args = parser.parse_args()

    
    print("Grafo del autómata")
    render_automaton_image()
    

    if args.url:
        # Procesar la URL indicada en -u
        process_url(args.url)

    elif args.file:
        # Procesar archivos o directorio indicado en -f
        if os.path.isdir(args.file):
            targets = sorted(glob.glob(os.path.join(args.file, '*.html')))
        else:
            targets = [args.file]
        if not targets:
            print("No se encontraron archivos HTML para procesar localmente.")
            return
        for filepath in targets:
            process_file(filepath)

    else:
        # Sin argumentos: procesamos archivos locales y además las 3 URLs fijas

        # 1) HTML locales
        targets = sorted(glob.glob('prueba*.html'))
        if targets:
            for filepath in targets:
                process_file(filepath)
        else:
            print("No se encontraron archivos 'prueba*.html' en el directorio actual.")

        # 2) URLs fijas
        fixed_urls = [
            'https://www.example.org',
            'https://www.python.org',
            'https://www.wikipedia.org'
        ]
        for url in fixed_urls:
            process_url(url)

if __name__ == '__main__':
    main()
