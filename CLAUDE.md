# Le Dattier — Instructions Claude Code

## Structure du projet

```
le-dattier-project/
├── produits.csv          ← 🔴 SOURCE UNIQUE DES PRODUITS (modifier ici)
├── sync-produits.py      ← Script de synchronisation (lancer après modif CSV)
├── index.html            ← Page d'accueil (hero, boutique, histoire, engagements)
├── faq.html              ← Page FAQ avec accordéon
├── livraison.html        ← Livraison & Retours
├── cgv.html              ← Conditions Générales de Vente
├── mentions-legales.html ← Mentions légales + Politique de confidentialité
├── style.css             ← Styles CSS (charte noir & or, partagés)
├── snipcart-theme.css    ← Thème Snipcart (noir & or)
├── products.js           ← ⚠️ AUTO-GÉNÉRÉ par sync-produits.py
├── app.js                ← Logique JS (filtres, panier, animations)
├── netlify.toml          ← Configuration Netlify
├── .gitignore            ← Fichiers exclus de Git
├── images/               ← Photos produits (à remplacer par vraies photos)
├── CLAUDE.md             ← Ce fichier (instructions pour Claude Code)
└── README.md             ← Guide utilisateur
```

## Où modifier les produits

FICHIER SOURCE : produits.csv (seul fichier à modifier pour les produits)
SCRIPT : sync-produits.py (génère products.js + bloc hidden index.html)

Le fichier produits.csv est un CSV avec séparateur point-virgule (;).
Colonnes : id;nom;origine;categorie;emoji;description;prix;unite;badge;image;poids

Après toute modification de produits.csv, lancer :
  python3 sync-produits.py

Ce script met à jour automatiquement :
1. products.js → catalogue JS pour l'affichage client
2. index.html → bloc <div hidden> pour la validation Snipcart

⚠️ NE JAMAIS modifier products.js à la main, il sera écrasé par le script.

Règles pour produits.csv :
- Encodage : UTF-8 avec BOM (compatible Excel/LibreOffice français)
- Séparateur : point-virgule (;)
- id : texte unique en kebab-case (ex: datte-medjool)
- categorie : "dattes", "savons" ou "nigelle"
- prix : nombre décimal avec point (ex: 18.90)
- badge : "new", "best" ou vide
- poids : entier en grammes
- image : chemin relatif (ex: images/prod-medjool.jpg)
- Colonnes : id;nom;origine;categorie;description;prix;unite;badge;image;poids

Chaque produit a cette structure :

```javascript
{
  id: "datte-deglet-nour",   // ID unique (texte, pas de doublons)
  name: "Deglet Nour Premium",
  origin: "Algérie",
  cat: "dattes",             // "dattes", "savons" ou "nigelle"
  emoji: "🌴",
  desc: "Description courte.",
  price: 18.90,              // Prix en euros
  unit: "500g",
  badge: "best",             // "best", "new" ou ""
  img: "images/prod-deglet.jpg",
  weight: 520                // Poids en grammes (pour livraison)
}
```

## Snipcart (e-commerce)

- La clé API est dans index.html, balise `<div id="snipcart">`
- Remplacer YOUR_API_KEY par la clé publique Snipcart
- Chaque bouton "+" est un bouton Snipcart avec attributs data-item-*
- Les attributs Snipcart sont générés automatiquement depuis products.js
- Le compteur panier dans la nav utilise la classe `snipcart-items-count`
- Le bouton panier utilise la classe `snipcart-checkout`

## Catégories

Définies à deux endroits (garder synchronisés) :
1. Boutons filtres dans index.html (data-cat="...")
2. Propriété `cat` de chaque produit dans products.js

Catégories actuelles : "dattes", "savons", "nigelle"

## Commandes fréquentes

Modifier un prix :
  Modifier la colonne prix dans produits.csv, puis lancer python3 sync-produits.py

Ajouter un produit :
  Ajouter une ligne dans produits.csv, puis lancer python3 sync-produits.py
  L'id doit être unique et en kebab-case

Retirer un produit :
  Supprimer la ligne dans produits.csv, puis lancer python3 sync-produits.py

Ajouter une catégorie :
  1. Utiliser le nouveau nom de catégorie dans produits.csv
  2. Ajouter un bouton filter-btn dans index.html
  3. Lancer python3 sync-produits.py

## Images

- Produits : 600x600px recommandé, format carré
- Hero : 1600x900px
- Story : 800x1067px (portrait 3:4)
- Formats : JPG, PNG, WebP

## Déploiement (via GitHub)

```bash
git add .
git commit -m "description de la modification"
git push
```

Netlify détecte automatiquement le push et déploie le site.

## Pages intérieures

Les pages FAQ, Livraison, CGV et Mentions légales partagent :
- Le même style.css
- La même nav (avec liens vers index.html#section)
- Le même footer (avec liens vers toutes les pages)
- Snipcart (le panier fonctionne sur toutes les pages)

Classes CSS pour les pages intérieures :
- .page-header : en-tête avec titre et lien retour
- .page-content : contenu principal (max-width 820px)
- .faq-item / .faq-question / .faq-answer : accordéon FAQ
- .back-home : lien "← Retour à l'accueil"

Les CGV et Mentions légales contiennent des [CROCHETS] à remplacer
par les vraies informations de l'entreprise.

## Notes

- Snipcart valide les prix en crawlant la page HTML
- Les prix dans products.js sont la source de vérité
- data-item-url="/" dans app.js pointe vers la page d'accueil
- Le site est responsive (breakpoint à 900px)
