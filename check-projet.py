#!/usr/bin/env python3
"""
check-projet.py — Le Dattier
Script de validation pre-livraison.
Verifie la coherence produits + conformite SEO + coherence README.

Usage : python3 check-projet.py
Retourne exit code 0 si OK, 1 si erreurs.
"""

import json
import os
import re
import sys

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
    with open(full, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================
# 1. COHERENCE BASE PRODUITS
# ============================================================
def check_products():
    print("\n═══ COHÉRENCE PRODUITS ═══")

    # --- Lire JSON ---
    json_path = os.path.join(BASE, "produits.json")
    if not os.path.exists(json_path):
        err("produits.json introuvable")
        return []

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        err(f"produits.json : JSON invalide ({e})")
        return []

    json_products = data.get("produits", [])
    json_count = len(json_products)
    json_ids = [p["id"] for p in json_products]

    # Vérifier champs obligatoires
    required_fields = ["id", "nom", "origine", "categorie", "description", "prix", "unite", "poids"]
    optional_fields = ["badge", "image"]
    for p in json_products:
        missing = [f for f in required_fields if f not in p]
        if missing:
            err(f"Produit {p.get('id', '???')} : champs manquants {missing}")
        missing_opt = [f for f in optional_fields if f not in p]
        if missing_opt:
            warn(f"Produit {p.get('id', '???')} : champs optionnels absents {missing_opt}")

    # Doublons
    seen = set()
    for pid in json_ids:
        if pid in seen:
            err(f"ID dupliqué dans JSON : {pid}")
        seen.add(pid)

    # Catégories valides
    valid_cats = {"dattes", "savons", "nigelle"}
    for p in json_products:
        if p.get("categorie") not in valid_cats:
            err(f"Catégorie inconnue '{p.get('categorie')}' pour {p['id']} (valides: {valid_cats})")

    # Badge valide
    valid_badges = {"", "new", "best"}
    for p in json_products:
        badge = p.get("badge", "")
        if badge is None:
            badge = ""
        if badge not in valid_badges:
            warn(f"Badge inconnu '{badge}' pour {p['id']} (valides: {valid_badges})")

    ok(f"produits.json : {json_count} produits")

    # --- Lire products.js ---
    js_content = read_file("products.js")
    if js_content is None:
        err("products.js introuvable")
        return json_products

    js_ids = re.findall(r'id:\s*"([^"]+)"', js_content)
    js_count = len(js_ids)

    if js_count != json_count:
        err(f"products.js a {js_count} produits, JSON en a {json_count}")
    else:
        ok(f"products.js : {js_count} produits (= JSON)")

    # Comparer IDs
    json_set = set(json_ids)
    js_set = set(js_ids)
    missing_in_js = json_set - js_set
    extra_in_js = js_set - json_set
    if missing_in_js:
        err(f"Produits dans JSON mais pas dans products.js : {missing_in_js}")
    if extra_in_js:
        err(f"Produits dans products.js mais pas dans JSON : {extra_in_js}")
    if not missing_in_js and not extra_in_js:
        ok("IDs JSON ↔ products.js : cohérents")

    # --- Lire bloc hidden index.html ---
    html_content = read_file("index.html")
    if html_content is None:
        err("index.html introuvable")
        return json_products

    hidden_match = re.search(r'<div hidden>(.*?)</div>', html_content, re.DOTALL)
    if hidden_match:
        hidden_block_ids = re.findall(r'data-item-id="([^"]+)"', hidden_match.group(1))
        hidden_block_count = len(hidden_block_ids)
        if hidden_block_count != json_count:
            err(f"Bloc hidden index.html a {hidden_block_count} produits, JSON en a {json_count}")
        else:
            ok(f"Bloc hidden index.html : {hidden_block_count} produits (= JSON)")

        # Vérifier prix hidden vs JSON
        hidden_prices = re.findall(r'data-item-price="([^"]+)"', hidden_match.group(1))
        json_prices = {p["id"]: f'{float(p["prix"]):.2f}' for p in json_products}
        for i, hid in enumerate(hidden_block_ids):
            if i < len(hidden_prices) and hid in json_prices:
                if hidden_prices[i] != json_prices[hid]:
                    err(f"Prix différent pour {hid} : hidden={hidden_prices[i]}, JSON={json_prices[hid]}")
        ok("Prix hidden ↔ JSON : vérifiés")
    else:
        err("Bloc <div hidden> introuvable dans index.html")

    # --- Vérifier JSON-LD produits ---
    jsonld_match = re.search(r'<script type="application/ld\+json" id="jsonld-products">\s*(.*?)\s*</script>', html_content, re.DOTALL)
    if jsonld_match:
        try:
            jsonld = json.loads(jsonld_match.group(1))
            jsonld_count = jsonld.get("numberOfItems", 0)
            if jsonld_count != json_count:
                err(f"JSON-LD a {jsonld_count} produits, JSON en a {json_count}")
            else:
                ok(f"JSON-LD produits : {jsonld_count} produits (= JSON)")
        except json.JSONDecodeError:
            err("JSON-LD produits : JSON invalide")
    else:
        err("JSON-LD produits introuvable dans index.html")

    # --- Vérifier images ---
    print("\n  --- Images produits ---")
    missing_images = 0
    no_image = 0
    for p in json_products:
        img = p.get("image", "")
        if not img:
            no_image += 1
            continue
        img_path = os.path.join(BASE, img)
        if not os.path.exists(img_path):
            err(f"Image manquante : {img} (produit: {p['id']})")
            missing_images += 1
    if missing_images == 0:
        ok(f"Images produits OK ({json_count - no_image} fichiers présents)")
    if no_image > 0:
        warn(f"{no_image} produit(s) sans image")

    # --- Vérifier catégories vs filtres ---
    json_cats = set(p["categorie"] for p in json_products)
    filter_cats = set(re.findall(r'data-cat="([^"]+)"', html_content)) - {"all"}
    if json_cats != filter_cats:
        missing_filters = json_cats - filter_cats
        extra_filters = filter_cats - json_cats
        if missing_filters:
            err(f"Catégories dans JSON sans bouton filtre : {missing_filters}")
        if extra_filters:
            warn(f"Boutons filtre sans produit : {extra_filters}")
    else:
        ok(f"Catégories JSON ↔ filtres index.html : cohérents ({json_cats})")

    return json_products


# ============================================================
# 2. AUDIT SEO
# ============================================================
def check_seo():
    print("\n═══ AUDIT SEO ═══")

    html_files = [f for f in os.listdir(BASE) if f.endswith('.html') and f != '404.html' and not f.startswith('admin')]

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
                warn(f"Title trop court ({tlen} car.) : {title.group(1)}")
            elif tlen > 70:
                warn(f"Title trop long ({tlen} car.) : {title.group(1)[:50]}...")
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

        # Heading hierarchy (ignore footer)
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

    # Vérifier sitemap cohérent avec pages HTML
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

    # Decap CMS admin
    admin_index = os.path.join(BASE, "admin", "index.html")
    admin_config = os.path.join(BASE, "admin", "config.yml")
    if os.path.exists(admin_index) and os.path.exists(admin_config):
        ok("Admin Decap CMS : index.html + config.yml présents")
    elif os.path.exists(admin_index) or os.path.exists(admin_config):
        warn("Admin Decap CMS : fichier manquant (index.html ou config.yml)")


# ============================================================
# 3. COHERENCE README
# ============================================================
def check_readme():
    print("\n═══ COHÉRENCE README ═══")

    readme = read_file("README.md")
    if readme is None:
        err("README.md introuvable")
        return

    ok("README.md présent")

    # Vérifier que le nombre de produits mentionné est correct
    json_path = os.path.join(BASE, "produits.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        json_products = data.get("produits", [])
        json_count = len(json_products)
        json_cats = set(p["categorie"] for p in json_products)

        # Vérifier le compte total
        count_match = re.search(r'(\d+)\s*produits?\s*(?:répartis|au total|dans)', readme)
        if count_match:
            readme_count = int(count_match.group(1))
            if readme_count != json_count:
                warn(f"README mentionne {readme_count} produits, JSON en a {json_count}")
            else:
                ok(f"Nombre de produits dans README ({readme_count}) = JSON")
        else:
            warn("Impossible de vérifier le nombre de produits dans README")

        # Vérifier catégories
        for cat in json_cats:
            if cat.lower() not in readme.lower():
                warn(f"Catégorie '{cat}' absente du README")

    # Vérifier fichiers clés
    key_files = ["produits.json", "sync-produits.py", "check-projet.py", "index.html",
                 "products.js", "sitemap.xml", "robots.txt", "favicon.svg"]
    missing_mentions = [f for f in key_files if f not in readme]
    if missing_mentions:
        warn(f"Fichiers non mentionnés dans README : {missing_mentions}")
    else:
        ok("Tous les fichiers clés mentionnés dans README")

    # Vérifier pages HTML
    actual_html = sorted([f for f in os.listdir(BASE) if f.endswith('.html')])
    for f in actual_html:
        if f not in readme:
            warn(f"Page {f} existe mais n'est pas dans le README")

    # Vérifier que le CSV n'est plus mentionné comme source
    if "produits.csv" in readme and "source" in readme.lower():
        warn("README mentionne encore produits.csv comme source (migré vers JSON)")


# ============================================================
# 4. RAPPORT
# ============================================================
def main():
    print("╔══════════════════════════════════════════╗")
    print("║  CHECK PROJET — LE DATTIER               ║")
    print("║  Validation pré-livraison                 ║")
    print("╚══════════════════════════════════════════╝")

    check_products()
    check_seo()
    check_readme()

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
