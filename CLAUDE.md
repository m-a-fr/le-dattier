# Le Dattier — Instructions Claude Code

> **Contexte complet du projet :** consulter `HISTORIQUE.md` pour l'historique des décisions,
> la charte graphique, le catalogue produits détaillé, et la liste des tâches restantes.

---

## ⚠️ RÈGLE ABSOLUE — CHECKLIST PRÉ-LIVRAISON

**Avant TOUTE livraison au propriétaire** (ZIP, commit, déploiement), exécuter :

```bash
python3 sync-produits.py    # Sync CSV → JS + HTML + JSON-LD
python3 check-projet.py     # Validation cohérence + SEO
```

**Ne jamais livrer si `check-projet.py` retourne des erreurs (❌).**

Les warnings (⚠️) sont tolérables mais doivent être signalés au propriétaire.

### Quand lancer la checklist ?

**TOUJOURS.** Même si la modification semble anodine. Même si le propriétaire
ne demande pas de vérification. Même si la modification ne touche pas les produits.

Cas typiques où un oubli peut casser le site :
- Le propriétaire modifie le CSV mais oublie de le mentionner
- Un changement de texte dans index.html écrase accidentellement le bloc hidden
- Un ajout de page sans canonical / OG / favicon
- Un produit ajouté sans image
- Une catégorie ajoutée sans bouton filtre

### Que vérifie check-projet.py ?

**Cohérence produits :**
- produits.csv ↔ products.js (même nombre, mêmes IDs)
- produits.csv ↔ bloc hidden index.html (même nombre, mêmes prix)
- produits.csv ↔ JSON-LD (même nombre)
- Images produits existent (chaque chemin du CSV pointe vers un fichier réel)
- Catégories CSV ↔ boutons filtres index.html
- Pas de doublons d'ID dans le CSV

**Conformité SEO :**
- Chaque page HTML a : title (20-70 car.), meta description (80-165 car.), canonical, h1 unique, Open Graph, favicon, preconnect, ARIA, lang="fr"
- Hiérarchie des headings correcte (pas de saut h1→h3)
- Fichiers globaux présents : robots.txt, sitemap.xml, favicon.svg, 404.html
- JSON-LD Organization + WebSite + ItemList dans index.html
- JSON-LD FAQPage dans faq.html
- Scripts locaux en defer

### Workflow complet de livraison

```
1. Effectuer les modifications demandées
2. Si produits touchés → python3 sync-produits.py
3. python3 check-projet.py
4. Si erreurs → corriger et recommencer à l'étape 3
5. Livrer (ZIP ou git add . && git commit && git push)
```

---

## Structure du projet

```
le-dattier-project/
├── produits.csv              <- SOURCE UNIQUE DES PRODUITS (modifier ici)
├── sync-produits.py          <- Sync CSV → products.js + index.html + JSON-LD
├── check-projet.py           <- Validation pré-livraison (cohérence + SEO)
├── index.html                <- Page d'accueil
├── faq.html                  <- FAQ avec accordéon + JSON-LD FAQPage
├── livraison.html            <- Livraison & Retours
├── cgv.html                  <- Conditions Générales de Vente
├── mentions-legales.html     <- Mentions légales + Confidentialité
├── 404.html                  <- Page 404 personnalisée
├── style.css                 <- Styles CSS (charte noir & or)
├── snipcart-theme.css        <- Thème Snipcart (noir & or)
├── products.js               <- AUTO-GÉNÉRÉ par sync-produits.py
├── app.js                    <- Logique JS (filtres, panier, animations)
├── favicon.svg               <- Favicon (D doré sur fond noir)
├── robots.txt                <- Instructions crawlers
├── sitemap.xml               <- Plan du site (5 pages)
├── netlify.toml              <- Config Netlify (headers, cache, 404)
├── .gitignore
├── images/
│   ├── site/                 <- Images du site (hero, histoire, valeurs)
│   └── produits/             <- Photos produits (classées par catégorie)
│       ├── dattes/
│       ├── savons/
│       └── nigelle/
├── CLAUDE.md                 <- Ce fichier (lu au démarrage par Claude Code)
├── HISTORIQUE.md             <- Historique complet pour continuité inter-sessions
└── README.md                 <- Guide utilisateur
```

---

## Gestion des produits

### Source unique : produits.csv

Seul fichier à modifier pour les produits. Tout le reste est auto-généré.

**Format :** UTF-8 avec BOM, séparateur point-virgule (;)
**Colonnes :** id;nom;origine;categorie;description;prix;unite;badge;image;poids

Règles :
- id : texte unique en kebab-case (ex: datte-medjool)
- categorie : "dattes", "savons" ou "nigelle"
- prix : nombre décimal avec point (ex: 18.90)
- badge : "new", "best" ou vide
- poids : entier en grammes
- image : chemin relatif vers images/produits/[categorie]/[nom].jpg

### sync-produits.py

Après toute modification de produits.csv, lancer : `python3 sync-produits.py`

Ce script met à jour automatiquement :
1. **products.js** → catalogue JS pour l'affichage client
2. **index.html bloc hidden** → validation prix par le crawler Snipcart
3. **index.html JSON-LD** → données structurées produits pour Google

⚠️ NE JAMAIS modifier products.js à la main — il sera écrasé par le script.

### Commandes fréquentes

**Modifier un prix ou une description :**
1. Modifier produits.csv → 2. sync-produits.py → 3. check-projet.py → 4. git push

**Ajouter un produit :**
1. Photo dans images/produits/[categorie]/[nom].jpg (kebab-case, 600x600px min)
2. Nouvelle ligne dans produits.csv
3. sync-produits.py → check-projet.py → git push

**Retirer un produit :**
1. Supprimer la ligne dans produits.csv
2. sync-produits.py → check-projet.py → git push

**Ajouter une catégorie :**
1. Créer images/produits/[nouvelle-categorie]/
2. Ajouter les produits dans produits.csv
3. Ajouter un bouton filter-btn dans index.html (data-cat="...")
4. sync-produits.py → check-projet.py → git push

**Ajouter une page HTML :**
1. Créer le fichier avec le même head que les autres pages (canonical, OG, favicon, preconnect, ARIA)
2. Ajouter l'URL dans sitemap.xml
3. check-projet.py → git push

---

## SEO — Règles à respecter

### Pour chaque page HTML
- `<title>` : 20-70 caractères, mots-clés pertinents
- `<meta name="description">` : 80-165 caractères, descriptif et accrocheur
- `<link rel="canonical">` : URL absolue de la page
- `<link rel="icon">` : favicon.svg
- `<link rel="preconnect">` : fonts.googleapis.com, fonts.gstatic.com, cdn.snipcart.com
- Open Graph : og:type, og:title, og:description, og:url, og:locale (+ og:image sur index)
- `<html lang="fr">`
- 1 seul `<h1>` par page
- Hiérarchie headings : h1 → h2 → h3 (jamais de saut)
- Au moins 1 attribut `aria-label` sur la navigation

### Pour le site global
- robots.txt : existe et pointe vers sitemap
- sitemap.xml : contient toutes les pages publiques
- favicon.svg : existe
- 404.html : existe + redirect dans netlify.toml
- JSON-LD Organization + WebSite + ItemList dans index.html
- JSON-LD FAQPage dans faq.html
- Scripts locaux en defer (pas de render-blocking)

### Quand modifier le SEO ?
- Ajout/suppression de page → mettre à jour sitemap.xml
- Changement de produit → sync-produits.py régénère le JSON-LD automatiquement
- Changement de contenu textuel → vérifier title et meta description
- Ajout de FAQ → mettre à jour le JSON-LD FAQPage dans faq.html

---

## Snipcart (e-commerce)

- Clé API dans toutes les pages HTML : `<div id="snipcart" data-api-key="...">`
- Le crawler Snipcart valide les prix via le bloc `<div hidden>` dans index.html
- Les prix dans products.js, le bloc hidden ET le JSON-LD doivent être identiques
- sync-produits.py gère cette synchronisation automatiquement
- Le compteur panier : `.snipcart-items-count`
- Le bouton panier : `.snipcart-checkout`

---

## Catégories

Définies à **trois** endroits (sync-produits.py gère 2 sur 3 automatiquement) :
1. ✅ produits.csv → source
2. ✅ products.js → auto-généré
3. ⚠️ Boutons filtres dans index.html → **à ajouter manuellement** si nouvelle catégorie

---

## Déploiement

```bash
git add .
git commit -m "description de la modification"
git push
```

Netlify détecte automatiquement le push et déploie en ~30 secondes.

---

## Pages intérieures

Toutes partagent : style.css, snipcart-theme.css, même nav, même footer, Snipcart.

Classes CSS :
- `.page-header` : en-tête avec titre et lien retour
- `.page-content` : contenu principal (max-width 820px)
- `.page-content h2` : sous-titres de section
- `.faq-item / .faq-question / .faq-answer` : accordéon FAQ
- `.back-home` : lien "← Retour à l'accueil"

Les CGV et Mentions légales contiennent des [CROCHETS] à remplacer
par les vraies informations de l'entreprise.

---

## Images

- Produits : 600x600px recommandé, format carré
- Hero : 1600x900px
- Story : 800x1067px (portrait 3:4)
- Formats : JPG, PNG, WebP
- Nommage : kebab-case, sans accents (ex: savon-alep-laurier.jpg)
- Emplacement : images/produits/[categorie]/[nom].jpg

---

## Notes techniques

- Snipcart valide les prix en crawlant la page HTML → bloc hidden obligatoire
- data-item-url="/" dans app.js pointe vers la page d'accueil
- Le site est responsive (breakpoint à 900px)
- Les h4 du footer sont acceptables (hors hiérarchie du contenu principal)
