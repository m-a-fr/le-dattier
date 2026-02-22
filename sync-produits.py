#!/usr/bin/env python3
"""
sync-produits.py — Le Dattier
Lit produits.csv et met a jour :
  1. products.js  (catalogue JS pour l'affichage)
  2. index.html   (bloc hidden pour la validation Snipcart)

Usage : python3 sync-produits.py
"""

import csv
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "produits.csv")
JS_PATH = os.path.join(BASE, "products.js")
HTML_PATH = os.path.join(BASE, "index.html")


def read_csv():
    """Lit produits.csv (UTF-8 avec ou sans BOM, separateur ;)."""
    products = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            row["prix"] = float(row["prix"])
            row["poids"] = int(row["poids"])
            products.append(row)
    return products


def generate_products_js(products):
    """Genere le contenu de products.js."""
    lines = []
    lines.append("// ============================================================")
    lines.append("// CATALOGUE PRODUITS — LE DATTIER")
    lines.append("// Auto-genere par sync-produits.py — Ne pas modifier a la main")
    lines.append("// Source : produits.csv")
    lines.append("// ============================================================")
    lines.append("")
    lines.append("const products = [")

    categories = {}
    for p in products:
        cat = p["categorie"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(p)

    first = True
    for cat, items in categories.items():
        lines.append(f"  // {cat.upper()}")
        for p in items:
            if not first:
                lines.append("")
            first = False
            badge_str = f'"{p["badge"]}"' if p["badge"] else '""'
            desc_escaped = p["description"].replace('"', '\\"')
            name_escaped = p["nom"].replace('"', '\\"')
            lines.append("  {")
            lines.append(f'    id: "{p["id"]}",')
            lines.append(f'    name: "{name_escaped}",')
            lines.append(f'    origin: "{p["origine"]}",')
            lines.append(f'    cat: "{p["categorie"]}",')
            lines.append(f'    desc: "{desc_escaped}",')
            lines.append(f'    price: {p["prix"]:.2f},')
            lines.append(f'    unit: "{p["unite"]}",')
            lines.append(f"    badge: {badge_str},")
            lines.append(f'    img: "{p["image"]}",')
            lines.append(f'    weight: {p["poids"]}')
            lines.append("  },")

    lines.append("];")
    lines.append("")
    return "\n".join(lines)


def generate_hidden_html(products):
    """Genere le bloc HTML hidden pour la validation Snipcart."""
    lines = []
    lines.append('  <!-- Produits caches pour la validation Snipcart (auto-genere par sync-produits.py) -->')
    lines.append('  <div hidden>')

    for p in products:
        desc_escaped = p["description"].replace('"', '&quot;')
        name_escaped = p["nom"].replace('"', '&quot;')
        lines.append(
            f'    <button class="snipcart-add-item"'
            f' data-item-id="{p["id"]}"'
            f' data-item-name="{name_escaped}"'
            f' data-item-price="{p["prix"]:.2f}"'
            f' data-item-url="/"'
            f' data-item-description="{desc_escaped}"'
            f' data-item-image="{p["image"]}"'
            f' data-item-weight="{p["poids"]}"'
            f' data-item-categories="{p["categorie"]}"'
            f"></button>"
        )

    lines.append("  </div>")
    return "\n".join(lines)


def update_index_html(hidden_html):
    """Remplace le bloc hidden dans index.html."""
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    pattern = r'  <!-- Produits cach.*?</div>'
    replacement = hidden_html

    if re.search(pattern, html, re.DOTALL):
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        html = html.replace(
            '<div class="products-grid" id="productsGrid"></div>',
            '<div class="products-grid" id="productsGrid"></div>\n\n' + hidden_html
        )

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    print("Lecture de produits.csv...")
    products = read_csv()
    print(f"  {len(products)} produits trouves")

    cats = set(p["categorie"] for p in products)
    for cat in sorted(cats):
        count = sum(1 for p in products if p["categorie"] == cat)
        print(f"  > {cat}: {count} produits")

    print("\nGeneration de products.js...")
    js_content = generate_products_js(products)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("  OK products.js mis a jour")

    print("\nMise a jour du bloc hidden dans index.html...")
    hidden_html = generate_hidden_html(products)
    update_index_html(hidden_html)
    print("  OK index.html mis a jour")

    print(f"\nSynchronisation terminee -- {len(products)} produits")
    print("  git add . && git commit -m 'maj produits' && git push")


if __name__ == "__main__":
    main()
