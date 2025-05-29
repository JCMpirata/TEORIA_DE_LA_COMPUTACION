import re
import lexer

"""
Módulo parser:
Función para comprobar el balanceo de etiquetas HTML.
"""

def is_balanced(html_text):
    """
    Comprueba si el HTML está bien balanceado: todas las etiquetas abiertas se cierran en orden,
    ignorando las void_tags.
    Retorna True si está balanceado, False en caso contrario.
    """
    tag_re = re.compile(r'<\s*(/)?\s*([a-zA-Z0-9]+)[^>]*?>')
    stack = []
    for slash, tag in tag_re.findall(html_text):
        tag = tag.lower()
        if slash:
            if not stack or stack[-1] != tag:
                return False
            stack.pop()
        else:
            if tag in lexer.void_tags:
                continue
            stack.append(tag)
    return not stack
