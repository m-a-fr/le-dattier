# Le Dattier

> Dattes d'exception, savons artisanaux & huile de nigelle — importés directement des meilleures terres d'Orient.

Site e-commerce statique déployé sur Netlify avec Snipcart comme solution de panier et Stripe pour les paiements.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Site | HTML / CSS / JS (vanilla, sans framework) |
| Panier & Checkout | [Snipcart](https://snipcart.com) v3.7.1 |
| Paiement | [Stripe](https://stripe.com) (via Snipcart) |
| Hébergement | [Netlify](https://netlify.com) |
| Gestion produits | CSV + script Python de synchronisation |

## Structure du projet

```
le-dattier-project/
├── produits.csv              ← Source unique des produits
├── sync-produits.py          ← Sync CSV → products.js + HTML + JSON-LD
├── check-projet.py           ← Validation pré-livraison
│
├── index.html                ← Accueil (hero, boutique, histoire, engagements)
├── faq.html                  ← FAQ (10 questions, accordéon)
├── livraison.html            ← Livraison & Retours
├── cgv.html                  ← Conditions Générales de Vente
├── mentions-legales.html     ← Mentions légales & Confidentialité
├── 404.html                  ← Page d'erreur personnalisée
│
├── style.css                 ← Charte graphique (noir & or)
├── snipcart-theme.css        ← Thème Snipcart assorti
├── products.js               ← Catalogue JS (auto-généré, ne pas modifier)
├── app.js                    ← Filtres, animations, panier
│
├── favicon.svg               ← Favicon
├── robots.txt                ← Instructions crawlers
├── sitemap.xml               ← Plan du site (5 pages)
├── netlify.toml              ← Config Netlify (headers, cache, 404)
│
├── images/
│   ├── site/                 ← hero.jpg, story.jpg, values-bg.jpg
│   └── produits/
│       ├── dattes/           ← 6 photos produits
│       ├── savons/           ← 4 photos produits
│       └── nigelle/          ← 4 photos produits
│
├── CLAUDE.md                 ← Instructions Claude Code
├── HISTORIQUE.md             ← Historique complet du projet
└── README.md                 ← Ce fichier
```

## Catalogue

14 produits répartis en 3 catégories :

| Catégorie | Produits | Prix |
|---|---|---|
| Dattes | Deglet Nour, Medjool, Ajwa, Sukari, Mazafati, Coffret | 18,90 – 45,00 € |
| Savons | Alep Laurier, Nigelle, Rose de Damas, Olive | 8,90 – 12,90 € |
| Nigelle | Huile Pure, Huile Bio, Capsules, Coffret Prestige | 16,90 – 39,90 € |

## Gestion des produits

Le catalogue est géré via un seul fichier : **`produits.csv`**.

Après toute modification du CSV, lancer :

```bash
python3 sync-produits.py
```

Ce script régénère automatiquement :
- `products.js` — catalogue JavaScript
- Bloc `<div hidden>` dans `index.html` — validation Snipcart
- Données structurées JSON-LD dans `index.html` — SEO Google

> ⚠️ Ne jamais modifier `products.js` à la main — il sera écrasé.

### Format du CSV

Encodage UTF-8 avec BOM, séparateur `;`.

```
id;nom;origine;categorie;description;prix;unite;badge;image;poids
datte-medjool;Medjool Royale;Palestine;dattes;Description...;24.50;500g;new;images/produits/dattes/medjool.jpg;520
```

## Validation pré-livraison

Avant tout déploiement, lancer :

```bash
python3 check-projet.py
```

Ce script vérifie :
- Cohérence entre CSV, products.js, bloc hidden, JSON-LD et images
- Conformité SEO de chaque page (title, description, canonical, OG, headings, ARIA)
- Présence des fichiers SEO (robots.txt, sitemap.xml, favicon, 404)

## Déploiement

Le site est connecté à Netlify via ce dépôt GitHub. Chaque push déclenche un déploiement automatique (~30 secondes).

```bash
python3 sync-produits.py          # Si le catalogue a changé
python3 check-projet.py           # Toujours vérifier avant de déployer
git add .
git commit -m "description"
git push
```

### Première mise en ligne

1. Créer le dépôt GitHub et pousser le projet
2. Connecter le dépôt dans [Netlify](https://app.netlify.com)
3. Le site se déploie automatiquement

## Configuration Snipcart

1. Créer un compte sur [snipcart.com](https://snipcart.com)
2. **Account > API Keys** : copier la clé publique
3. La clé est déjà intégrée dans les pages HTML (`<div id="snipcart" data-api-key="...">`)
4. Dans le dashboard Snipcart, ajouter le domaine du site

## Paiements (Stripe)

Connecter Stripe dans le dashboard Snipcart.

- Frais : 1,5% + 0,25 € par transaction carte européenne
- Versements : sous 2 à 7 jours ouvrés
- Devises : EUR

## Gestion avec Claude Code

Ouvrir un terminal dans le dossier projet et lancer `claude`. Exemples :

```
"Change le prix de la Deglet Nour à 21,90 euros"
"Ajoute un produit : Dattes Khudri, Arabie Saoudite, 500g, 15,90 €"
"Retire les Capsules de Nigelle du catalogue"
"Mets le badge Nouveau sur l'Huile de Nigelle Pure"
```

Claude Code lit automatiquement `CLAUDE.md` au démarrage et applique le workflow de validation avant chaque livraison.

## SEO

Le site intègre :
- Balises `<title>`, `<meta description>`, `<link rel="canonical">` sur chaque page
- Open Graph + Twitter Card pour le partage social
- Données structurées JSON-LD (Organization, WebSite, ItemList, FAQPage)
- `robots.txt` + `sitemap.xml`
- Favicon SVG
- Hiérarchie des headings correcte (h1 → h2 → h3)
- Attributs ARIA pour l'accessibilité
- Scripts en `defer`, `preconnect` pour les ressources externes

## Ce qui reste à faire

- [ ] Remplacer les images placeholder par de vraies photos
- [ ] Remplir les `[CROCHETS]` dans cgv.html et mentions-legales.html
- [ ] Connecter Stripe en mode live
- [ ] Acheter et configurer le nom de domaine
- [ ] Mettre à jour les URLs (sitemap, canonical, OG) avec le domaine final
- [ ] Ajouter un menu burger mobile
- [ ] Brancher la newsletter (Mailchimp, Brevo…)
- [ ] Analytics RGPD-friendly (Plausible, Matomo…)

## Licence

Projet privé — tous droits réservés.
