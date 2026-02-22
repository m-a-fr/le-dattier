#!/usr/bin/env python3
"""
sync-produits.py — Le Dattier
Lit produits.json et met a jour :
  1. products.js  (catalogue JS pour l'affichage)
  2. index.html   (bloc hidden pour Snipcart + JSON-LD SEO)

Usage : python3 sync-produits.py

Source : produits.json (edite via Decap CMS ou manuellement)
"""

import json
import re
import os
import hashlib

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE, "produits.json")
JS_PATH = os.path.join(BASE, "products.js")
HTML_PATH = os.path.join(BASE, "index.html")
SITE_URL = "https://www.ledattier.fr"


def read_products():
    """Lit produits.json."""
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    products = data.get("produits", [])
    # Normaliser les types et les champs optionnels
    for p in products:
        p["prix"] = float(p.get("prix", 0))
        p["poids"] = int(p.get("poids", 0))
        # Champs optionnels : valeur par défaut si absent ou None
        if not p.get("badge"):
            p["badge"] = ""
        if not p.get("image"):
            p["image"] = ""
        if not p.get("description"):
            p["description"] = ""
    return products


def generate_products_js(products):
    """Genere le contenu de products.js."""
    lines = []
    lines.append("// ============================================================")
    lines.append("// CATALOGUE PRODUITS — LE DATTIER")
    lines.append("// Auto-genere par sync-produits.py — Ne pas modifier a la main")
    lines.append("// Source : produits.json")
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
        img_attr = f' data-item-image="{p["image"]}"' if p["image"] else ""
        lines.append(
            f'    <button class="snipcart-add-item"'
            f' data-item-id="{p["id"]}"'
            f' data-item-name="{name_escaped}"'
            f' data-item-price="{p["prix"]:.2f}"'
            f' data-item-url="/"'
            f' data-item-description="{desc_escaped}"'
            f'{img_attr}'
            f' data-item-weight="{p["poids"]}"'
            f' data-item-categories="{p["categorie"]}"'
            f"></button>"
        )

    lines.append("  </div>")
    return "\n".join(lines)


def generate_jsonld_products(products):
    """Genere le bloc JSON-LD pour le SEO produits."""
    cat_labels = {
        "dattes": "Dattes",
        "savons": "Savons artisanaux",
        "nigelle": "Huile de Nigelle"
    }

    items = []
    for p in products:
        item = {
            "@type": "Product",
            "name": p["nom"],
            "description": p["description"],
            "brand": {
                "@type": "Brand",
                "name": "Le Dattier"
            },
            "category": cat_labels.get(p["categorie"], p["categorie"]),
            "offers": {
                "@type": "Offer",
                "url": f'{SITE_URL}/#boutique',
                "priceCurrency": "EUR",
                "price": f'{p["prix"]:.2f}',
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "Le Dattier"
                }
            }
        }
        if p["image"]:
            item["image"] = f'{SITE_URL}/{p["image"]}'
        if p["poids"]:
            item["weight"] = {
                "@type": "QuantitativeValue",
                "value": p["poids"],
                "unitCode": "GRM"
            }
        items.append(item)

    jsonld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Catalogue Le Dattier",
        "numberOfItems": len(items),
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": item
            }
            for i, item in enumerate(items)
        ]
    }

    return json.dumps(jsonld, ensure_ascii=False, indent=2)


def update_index_html(hidden_html, jsonld_str, js_hash):
    """Remplace le bloc hidden, le JSON-LD produits et le cache bust dans index.html."""
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Remplacer bloc hidden Snipcart
    pattern_hidden = r'  <!-- Produits cach.*?</div>'
    if re.search(pattern_hidden, html, re.DOTALL):
        html = re.sub(pattern_hidden, hidden_html, html, flags=re.DOTALL)
    else:
        html = html.replace(
            '<div class="products-grid" id="productsGrid"></div>',
            '<div class="products-grid" id="productsGrid"></div>\n\n' + hidden_html
        )

    # 2. Remplacer ou inserer JSON-LD produits
    jsonld_block = f'<script type="application/ld+json" id="jsonld-products">\n{jsonld_str}\n</script>'
    pattern_jsonld = r'<script type="application/ld\+json" id="jsonld-products">.*?</script>'
    if re.search(pattern_jsonld, html, re.DOTALL):
        html = re.sub(pattern_jsonld, jsonld_block, html, flags=re.DOTALL)
    else:
        html = html.replace('</head>', jsonld_block + '\n</head>')

    # 3. Cache busting : mettre a jour le hash dans l'URL de products.js
    html = re.sub(
        r'products\.js(\?v=[a-f0-9]+)?',
        f'products.js?v={js_hash}',
        html
    )

    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    print("Lecture de produits.json...")
    products = read_products()
    print(f"  {len(products)} produits trouves")

    cats = set(p["categorie"] for p in products)
    for cat in sorted(cats):
        count = sum(1 for p in products if p["categorie"] == cat)
        print(f"  > {cat}: {count} produits")

    print("\nGeneration de products.js...")
    js_content = generate_products_js(products)
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
    js_hash = hashlib.md5(js_content.encode()).hexdigest()[:8]
    print(f"  OK products.js mis a jour (hash: {js_hash})")

    print("\nGeneration du JSON-LD produits...")
    jsonld_str = generate_jsonld_products(products)
    print("  OK JSON-LD genere")

    print("\nMise a jour de index.html...")
    hidden_html = generate_hidden_html(products)
    update_index_html(hidden_html, jsonld_str, js_hash)
    print("  OK index.html mis a jour (hidden + JSON-LD + cache bust)")

    print(f"\nSynchronisation terminee -- {len(products)} produits")


if __name__ == "__main__":
    main()
