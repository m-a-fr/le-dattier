#!/usr/bin/env python3
"""
check-projet.py — Le Dattier
Script de validation pre-livraison.
Verifie la coherence produits + conformite SEO.

Usage : python3 check-projet.py
Retourne exit code 0 si OK, 1 si erreurs.
"""

import csv
import os
import re
import sys
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ERRORS = []
WARNINGS = []


def err(msg):
    ERRORS.append(msg)
    print(f"  ❌ {msg}")


def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠️  {msg}")


def ok(msg):
    print(f"  ✅ {msg}")


def read_file(path):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None
    with open(full, "r", encoding="utf-8-sig") as f:
        return f.read()


# ============================================================
# 1. COHERENCE BASE PRODUITS
# ============================================================
def check_products():
    print("\n═══ COHÉRENCE PRODUITS ═══")

    # --- Lire CSV ---
    csv_path = os.path.join(BASE, "produits.csv")
    if not os.path.exists(csv_path):
        err("produits.csv introuvable")
        return [], []

    csv_products = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        cols = reader.fieldnames
        expected_cols = ["id", "nom", "origine", "categorie", "description", "prix", "unite", "badge", "image", "poids"]
        if cols != expected_cols:
            err(f"Colonnes CSV incorrectes: {cols} (attendu: {expected_cols})")
        for row in reader:
            csv_products.append(row)

    csv_ids = [p["id"] for p in csv_products]
    csv_count = len(csv_products)

    # Doublons CSV
    seen = set()
    for pid in csv_ids:
        if pid in seen:
            err(f"ID dupliqué dans CSV: {pid}")
        seen.add(pid)

    ok(f"produits.csv : {csv_count} produits")

    # --- Lire products.js ---
    js_content = read_file("products.js")
    if js_content is None:
        err("products.js introuvable")
        return csv_products, []

    js_ids = re.findall(r'id:\s*"([^"]+)"', js_content)
    js_prices = re.findall(r'price:\s*([\d.]+)', js_content)
    js_count = len(js_ids)

    if js_count != csv_count:
        err(f"products.js a {js_count} produits, CSV en a {csv_count}")
    else:
        ok(f"products.js : {js_count} produits (= CSV)")

    # Comparer IDs
    csv_set = set(csv_ids)
    js_set = set(js_ids)
    missing_in_js = csv_set - js_set
    extra_in_js = js_set - csv_set
    if missing_in_js:
        err(f"Produits dans CSV mais pas dans products.js: {missing_in_js}")
    if extra_in_js:
        err(f"Produits dans products.js mais pas dans CSV: {extra_in_js}")
    if not missing_in_js and not extra_in_js:
        ok("IDs CSV ↔ products.js : cohérents")

    # --- Lire bloc hidden index.html ---
    html_content = read_file("index.html")
    if html_content is None:
        err("index.html introuvable")
        return csv_products, js_ids

    hidden_ids = re.findall(r'data-item-id="([^"]+)"', html_content)
    # Ne garder que ceux dans le bloc hidden (tous les data-item-id dans le hidden div)
    # En pratique on compare juste les sets
    hidden_set = set(hidden_ids)
    # Les IDs apparaissent aussi dans le JS rendu, donc on filtre par les uniques du hidden
    # Le hidden a exactement N boutons, le JS en crée N aussi, donc on check count
    hidden_count = html_content.count('class="snipcart-add-item"')
    # Chaque produit a 1 bouton dans hidden + le template JS en crée 1 = 2 par produit
    # Non, le hidden a N boutons, et le JS template en a 1 par produit aussi
    # Mais les hidden buttons sont dans <div hidden>, comptons ceux-la
    hidden_match = re.search(r'<div hidden>(.*?)</div>', html_content, re.DOTALL)
    if hidden_match:
        hidden_block_ids = re.findall(r'data-item-id="([^"]+)"', hidden_match.group(1))
        hidden_block_count = len(hidden_block_ids)
        if hidden_block_count != csv_count:
            err(f"Bloc hidden index.html a {hidden_block_count} produits, CSV en a {csv_count}")
        else:
            ok(f"Bloc hidden index.html : {hidden_block_count} produits (= CSV)")

        # Verifier prix hidden vs CSV
        hidden_prices = re.findall(r'data-item-price="([^"]+)"', hidden_match.group(1))
        csv_prices = {p["id"]: f'{float(p["prix"]):.2f}' for p in csv_products}
        for i, hid in enumerate(hidden_block_ids):
            if i < len(hidden_prices) and hid in csv_prices:
                if hidden_prices[i] != csv_prices[hid]:
                    err(f"Prix différent pour {hid}: hidden={hidden_prices[i]}, CSV={csv_prices[hid]}")
        ok("Prix hidden ↔ CSV : vérifiés")
    else:
        err("Bloc <div hidden> introuvable dans index.html")

    # --- Verifier JSON-LD produits ---
    jsonld_match = re.search(r'<script type="application/ld\+json" id="jsonld-products">\s*(.*?)\s*</script>', html_content, re.DOTALL)
    if jsonld_match:
        try:
            jsonld = json.loads(jsonld_match.group(1))
            jsonld_count = jsonld.get("numberOfItems", 0)
            if jsonld_count != csv_count:
                err(f"JSON-LD a {jsonld_count} produits, CSV en a {csv_count}")
            else:
                ok(f"JSON-LD produits : {jsonld_count} produits (= CSV)")
        except json.JSONDecodeError:
            err("JSON-LD produits : JSON invalide")
    else:
        err("JSON-LD produits introuvable dans index.html")

    # --- Verifier images ---
    print("\n  --- Images produits ---")
    missing_images = 0
    for p in csv_products:
        img_path = os.path.join(BASE, p["image"])
        if not os.path.exists(img_path):
            err(f"Image manquante: {p['image']} (produit: {p['id']})")
            missing_images += 1
    if missing_images == 0:
        ok(f"Toutes les images produits existent ({csv_count} fichiers)")

    # --- Verifier catégories vs filtres ---
    csv_cats = set(p["categorie"] for p in csv_products)
    filter_cats = set(re.findall(r'data-cat="([^"]+)"', html_content)) - {"all"}
    if csv_cats != filter_cats:
        missing_filters = csv_cats - filter_cats
        extra_filters = filter_cats - csv_cats
        if missing_filters:
            err(f"Catégories dans CSV sans bouton filtre: {missing_filters}")
        if extra_filters:
            warn(f"Boutons filtre sans produit: {extra_filters}")
    else:
        ok(f"Catégories CSV ↔ filtres index.html : cohérents ({csv_cats})")

    return csv_products, js_ids


# ============================================================
# 2. AUDIT SEO
# ============================================================
def check_seo():
    print("\n═══ AUDIT SEO ═══")

    html_files = [f for f in os.listdir(BASE) if f.endswith('.html') and f != '404.html']

    for f in sorted(html_files):
        print(f"\n  --- {f} ---")
        content = read_file(f)
        if content is None:
            err(f"{f} introuvable")
            continue

        # Title
        title = re.search(r'<title>(.*?)</title>', content)
        if title:
            tlen = len(title.group(1))
            if tlen < 20:
                warn(f"Title trop court ({tlen} car.): {title.group(1)}")
            elif tlen > 70:
                warn(f"Title trop long ({tlen} car.): {title.group(1)[:50]}...")
            else:
                ok(f"Title OK ({tlen} car.)")
        else:
            err("Pas de <title>")

        # Meta description
        desc = re.search(r'meta name="description" content="([^"]*)"', content)
        if desc:
            dlen = len(desc.group(1))
            if dlen < 80:
                warn(f"Meta description courte ({dlen} car., idéal 120-160)")
            elif dlen > 165:
                warn(f"Meta description longue ({dlen} car., sera tronquée)")
            else:
                ok(f"Meta description OK ({dlen} car.)")
        else:
            err("Pas de meta description")

        # Canonical
        if 'rel="canonical"' in content:
            ok("Canonical présent")
        else:
            err("Pas de balise canonical")

        # H1 count
        h1_count = len(re.findall(r'<h1', content))
        if h1_count == 0:
            err("Aucun <h1>")
        elif h1_count > 1:
            warn(f"{h1_count} balises <h1> (devrait être 1)")
        else:
            ok("1 seul <h1>")

        # Heading hierarchy (ignore footer headings)
        # Split content at <footer> to check only main content
        main_content = content.split('<footer>')[0] if '<footer>' in content else content
        headings = re.findall(r'<h(\d)', main_content)
        if headings:
            prev = 0
            gap_found = False
            for h in headings:
                level = int(h)
                if prev > 0 and level > prev + 1:
                    gap_found = True
                prev = level
            if gap_found:
                warn("Saut dans la hiérarchie des headings (ex: h1 → h3 sans h2)")
            else:
                ok("Hiérarchie headings correcte")

        # Open Graph
        og_count = len(re.findall(r'property="og:', content))
        if og_count >= 4:
            ok(f"Open Graph : {og_count} balises")
        elif og_count > 0:
            warn(f"Open Graph incomplet ({og_count} balises, idéal >= 4)")
        else:
            err("Aucune balise Open Graph")

        # Favicon
        if 'favicon' in content:
            ok("Favicon référencé")
        else:
            warn("Pas de lien favicon")

        # Preconnect
        if 'preconnect' in content:
            ok("Preconnect présent")
        else:
            warn("Pas de preconnect (perf)")

        # ARIA
        aria_count = len(re.findall(r'aria-', content))
        if aria_count > 0:
            ok(f"ARIA : {aria_count} attributs")
        else:
            warn("Aucun attribut ARIA")

        # lang
        if 'lang="fr"' in content:
            ok('lang="fr" présent')
        else:
            err("Attribut lang manquant")

    # --- Fichiers globaux ---
    print("\n  --- Fichiers SEO globaux ---")

    for f in ["robots.txt", "sitemap.xml", "favicon.svg", "404.html"]:
        path = os.path.join(BASE, f)
        if os.path.exists(path):
            ok(f"{f} présent")
        else:
            err(f"{f} manquant")

    # Verifier sitemap cohérent avec pages HTML
    sitemap = read_file("sitemap.xml")
    if sitemap:
        sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap)
        for f in html_files:
            if f == "index.html":
                expected = "https://www.ledattier.fr/"
            else:
                expected = f"https://www.ledattier.fr/{f}"
            if expected not in sitemap_urls:
                warn(f"{f} absent du sitemap.xml")

    # JSON-LD
    html_index = read_file("index.html")
    if html_index:
        jsonld_count = len(re.findall(r'application/ld\+json', html_index))
        if jsonld_count >= 2:
            ok(f"JSON-LD : {jsonld_count} blocs dans index.html")
        else:
            warn(f"JSON-LD : seulement {jsonld_count} bloc(s)")

    faq_content = read_file("faq.html")
    if faq_content and "FAQPage" in faq_content:
        ok("JSON-LD FAQPage dans faq.html")
    elif faq_content:
        warn("Pas de JSON-LD FAQPage dans faq.html")

    # Scripts defer
    if html_index:
        blocking_scripts = re.findall(r'<script src="(?!.*snipcart)([^"]+)"(?!.*defer)(?!.*async)', html_index)
        if blocking_scripts:
            warn(f"Scripts bloquants (sans defer) : {blocking_scripts}")
        else:
            ok("Scripts locaux en defer")


# ============================================================
# 3. RAPPORT
# ============================================================
def main():
    print("╔══════════════════════════════════════════╗")
    print("║  CHECK PROJET — LE DATTIER               ║")
    print("║  Validation pré-livraison                 ║")
    print("╚══════════════════════════════════════════╝")

    check_products()
    check_seo()

    print("\n" + "═" * 44)
    print(f"  Erreurs  : {len(ERRORS)}")
    print(f"  Warnings : {len(WARNINGS)}")
    print("═" * 44)

    if ERRORS:
        print("\n🚫 LIVRAISON BLOQUÉE — corriger les erreurs ci-dessus.")
        print("   Lancer sync-produits.py si la base produit a changé.")
        sys.exit(1)
    elif WARNINGS:
        print("\n⚠️  LIVRAISON POSSIBLE — mais vérifier les warnings.")
        sys.exit(0)
    else:
        print("\n✅ TOUT EST BON — prêt à livrer.")
        sys.exit(0)


if __name__ == "__main__":
    main()
