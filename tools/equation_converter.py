#!/usr/bin/env python3
"""
LATEX TO OMML (WORD EQUATION BUILDER) CONVERTER
Converts LaTeX math expressions to Microsoft Word native Equation XML (OMML).
"""

import latex2mathml.converter
from lxml import etree
import docx

XSLT_PATH = "/Users/dogukancihanbeyoglu/Gemini/tools/MML2OMML.XSL"
_xslt_doc = etree.parse(XSLT_PATH)
_transform = etree.XSLT(_xslt_doc)

def latex_to_omml_element(latex_str):
    """
    Converts a LaTeX string into an lxml element representing Word's <m:oMathPara> or <m:oMath>.
    """
    # Clean string
    clean_latex = latex_str.strip()
    if clean_latex.startswith("$$") and clean_latex.endswith("$$"):
        clean_latex = clean_latex[2:-2].strip()
    elif clean_latex.startswith("$") and clean_latex.endswith("$"):
        clean_latex = clean_latex[1:-1].strip()

    # Sanitize & for XML compatibility if present inside text macros
    sanitized_latex = clean_latex.replace(r'\&', '&amp;').replace('&', '&amp;') if '&amp;' not in clean_latex else clean_latex
    # But latex2mathml wants plain text or \&, let's replace \& with and or remove ampersand
    sanitized_latex = clean_latex.replace(r'\&', '-').replace('&', '-')

    # Convert to MathML
    mml_str = latex2mathml.converter.convert(sanitized_latex)
    mml_tree = etree.fromstring(mml_str)

    # Transform to OMML
    omml_tree = _transform(mml_tree)
    root = omml_tree.getroot()
    return root

def add_equation_to_paragraph(paragraph, latex_str):
    """
    Appends a native Word Equation (OMML) to a docx Paragraph.
    """
    try:
        omml_elem = latex_to_omml_element(latex_str)
        paragraph._p.append(omml_elem)
        return True
    except Exception as e:
        print(f"[!] Warning: Failed to convert equation '{latex_str}': {e}")
        r = paragraph.add_run(latex_str)
        r.italic = True
        return False

if __name__ == "__main__":
    import sys
    test_eq = r"Y = \rho W Y + X \beta + W X \theta + \mu + \varepsilon"
    elem = latex_to_omml_element(test_eq)
    print("Converted successfully! Root:", elem.tag)
