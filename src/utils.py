"""
Utility functions for Mevzuat Radarı:
- Turkish-aware case conversions (title, upper, lower)
- HTML sanitization and escaping
"""
import html


def title_tr(text: str) -> str:
    """Turkish-aware title casing (handles I/ı and İ/i properly)."""
    if not text:
        return ""
    
    words = text.split()
    capitalized_words = []
    for word in words:
        if not word:
            continue
        first_char = word[0]
        rest = word[1:]
        
        # Upper first char
        if first_char == "i":
            first_upper = "İ"
        elif first_char == "ı":
            first_upper = "I"
        else:
            first_upper = first_char.upper()
            
        # Lower rest
        rest_lower = ""
        for c in rest:
            if c == "İ":
                rest_lower += "i"
            elif c == "I":
                rest_lower += "ı"
            else:
                rest_lower += c.lower()
                
        capitalized_words.append(first_upper + rest_lower)
        
    return " ".join(capitalized_words)


def upper_tr(text: str) -> str:
    """Turkish-aware uppercase."""
    if not text:
        return ""
    res = ""
    for c in text:
        if c == "i":
            res += "İ"
        elif c == "ı":
            res += "I"
        else:
            res += c.upper()
    return res


def lower_tr(text: str) -> str:
    """Turkish-aware lowercase."""
    if not text:
        return ""
    res = ""
    for c in text:
        if c == "İ":
            res += "i"
        elif c == "I":
            res += "ı"
        else:
            res += c.lower()
    return res


def safe_html(text: str) -> str:
    """Escapes unsafe HTML characters."""
    if not text:
        return ""
    return html.escape(text)
