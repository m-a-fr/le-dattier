# Le Dattier — Instructions Claude Code

## Structure du projet

```
le-dattier-project/
├── produits.csv              <- SOURCE UNIQUE DES PRODUITS (modifier ici)
├── sync-produits.py          <- Script de synchronisation (lancer apres modif CSV)
├── index.html                <- Page d'accueil
├── faq.html                  <- FAQ avec accordéon
├── livraison.html            <- Livraison & Retours
├── cgv.html                  <- Conditions Générales de Vente
├── mentions-legales.html     <- Mentions légales + Confidentialité
├── style.css                 <- Styles CSS (charte noir & or)
├── snipcart-theme.css        <- Thème Snipcart (noir & or)
├── products.js               <- AUTO-GENERE par sync-produits.py
├── app.js                    <- Logique JS (filtres, panier, animations)
├── netlify.toml              <- Configuration Netlify
├── .gitignore
├── images/
│   ├── site/                 <- Images du site (hero, histoire, etc.)
│   │   ├── hero.jpg
│   │   ├── story.jpg
│   │   └── values-bg.jpg
│   └── produits/             <- Photos produits (classées par catégorie)
│       ├── dattes/
│       │   ├── deglet-nour.jpg
│       │   ├── medjool.jpg
│       │   └── ...
│       ├── savons/
│       │   ├── alep-laurier.jpg
│       │   └── ...
│       └── nigelle/
│           ├── pure.jpg
│           └── ...
├── CLAUDE.md                 <- Ce fichier
└── README.md                 <- Guide utilisateur
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
- image : chemin relatif vers images/produits/[categorie]/[nom].jpg
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

### Modifier un prix ou une description
1. Ouvrir produits.csv (Excel, LibreOffice ou éditeur de texte)
2. Modifier la valeur souhaitée
3. Sauvegarder le fichier
4. Lancer : python3 sync-produits.py
5. Déployer : git add . && git commit -m "maj prix" && git push

### Ajouter un nouveau produit
1. Placer la photo dans images/produits/[categorie]/[nom].jpg
   Nommer le fichier en kebab-case, sans accents (ex: miel-sidr.jpg)
   Format recommandé : JPG, 600x600px minimum, fond neutre
2. Ajouter une ligne dans produits.csv avec le chemin de l'image
   Exemple : nouveau-produit;Mon Produit;France;dattes;Description;15.90;250g;new;images/produits/dattes/miel-sidr.jpg;300
3. Lancer : python3 sync-produits.py
4. Déployer : git add . && git commit -m "ajout produit" && git push

### Retirer un produit
1. Supprimer la ligne dans produits.csv
2. Optionnel : supprimer l'image dans images/produits/[categorie]/
3. Lancer : python3 sync-produits.py
4. Déployer : git add . && git commit -m "retrait produit" && git push

### Remplacer une photo produit
1. Remplacer le fichier dans images/produits/[categorie]/ (garder le même nom)
2. Déployer : git add . && git commit -m "maj photo" && git push
   Pas besoin de lancer sync-produits.py si le nom du fichier ne change pas

### Ajouter une catégorie
1. Créer le sous-dossier : images/produits/[nouvelle-categorie]/
2. Y placer les photos
3. Ajouter les produits dans produits.csv avec la nouvelle catégorie
4. Ajouter un bouton filter-btn dans index.html
5. Lancer : python3 sync-produits.py
6. Déployer

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
