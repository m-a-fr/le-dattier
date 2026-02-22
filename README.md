# Le Dattier

> Dattes d'exception, savons artisanaux & huile de nigelle — importés directement des meilleures terres d'Orient.

Site e-commerce statique avec interface d'administration intégrée.

---

## Stack technique

| Composant | Technologie |
|---|---|
| Site | HTML / CSS / JS vanilla |
| Panier & Checkout | [Snipcart](https://snipcart.com) v3.7.1 |
| Paiement | [Stripe](https://stripe.com) (via Snipcart) |
| Hébergement | [Netlify](https://netlify.com) |
| CMS | [Decap CMS](https://decapcms.org) (ex Netlify CMS) |
| Authentification | Netlify Identity |
| Gestion produits | JSON + script Python de synchronisation |

## Structure du projet

```
le-dattier-project/
├── produits.json             ← Source unique des produits
├── sync-produits.py          ← Sync JSON → products.js + HTML + JSON-LD
├── check-projet.py           ← Validation pré-livraison
│
├── admin/
│   ├── index.html            ← Interface Decap CMS
│   └── config.yml            ← Configuration des champs produits
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
├── netlify.toml              ← Config Netlify (build, headers, cache, 404)
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

## Administration des produits

### Via l'interface web (Decap CMS)

L'interface d'administration est accessible sur `/admin/`. Elle permet de modifier les produits (prix, descriptions, badges, images) sans toucher au code.

1. Aller sur `https://www.ledattier.fr/admin/`
2. Se connecter avec ses identifiants Netlify Identity
3. Modifier les produits via les formulaires
4. Cliquer "Publier"
5. Le site se met à jour automatiquement (~1 minute)

### Via le code (développeurs)

Le catalogue est stocké dans **`produits.json`**. Après modification :

```bash
python3 sync-produits.py      # Régénère products.js + HTML + JSON-LD
python3 check-projet.py       # Validation pré-livraison
git add . && git commit -m "description" && git push
```

Netlify exécute `sync-produits.py` automatiquement à chaque déploiement.

> ⚠️ Ne jamais modifier `products.js` à la main — il est auto-généré.

## Validation pré-livraison

```bash
python3 check-projet.py
```

Vérifie automatiquement la cohérence produits (JSON ↔ JS ↔ HTML ↔ JSON-LD ↔ images), la conformité SEO de chaque page, et la cohérence du README.

## Déploiement

Le site est connecté à Netlify via ce dépôt GitHub. Chaque push (ou publication via l'admin) déclenche un redéploiement automatique.

### Première mise en ligne

1. Créer le dépôt GitHub et pousser le projet
2. Connecter le dépôt dans [Netlify](https://app.netlify.com)
3. Activer **Identity** dans Netlify Dashboard
4. Activer **Git Gateway** dans Identity > Settings > Services
5. Inviter l'admin par email (Identity > Invite users)

## Configuration Snipcart

1. Créer un compte sur [snipcart.com](https://snipcart.com)
2. **Account > API Keys** : copier la clé publique
3. La clé est intégrée dans les pages HTML (`<div id="snipcart" data-api-key="...">`)
4. Dans le dashboard Snipcart, ajouter le domaine du site

## Paiements (Stripe)

Connecter Stripe dans le dashboard Snipcart.

- Frais : 1,5% + 0,25 € par transaction carte européenne
- Versements : sous 2 à 7 jours ouvrés

## SEO

Le site intègre : balises title/description/canonical, Open Graph, Twitter Card, JSON-LD (Organization, WebSite, ItemList, FAQPage), robots.txt, sitemap.xml, favicon SVG, hiérarchie headings correcte, attributs ARIA, scripts en defer, preconnect.

## Gestion avec Claude Code

Ouvrir un terminal dans le dossier projet et lancer `claude`. Exemples :

```
"Change le prix de la Deglet Nour à 21,90 euros"
"Ajoute un produit : Dattes Khudri, Arabie Saoudite, 500g, 15,90 €"
"Retire les Capsules de Nigelle du catalogue"
```

Claude Code lit `CLAUDE.md` au démarrage et applique automatiquement le workflow de validation.

## Ce qui reste à faire

- [ ] Remplacer les images placeholder par de vraies photos
- [ ] Remplir les `[CROCHETS]` dans cgv.html et mentions-legales.html
- [ ] Connecter Stripe en mode live
- [ ] Acheter et configurer le nom de domaine
- [ ] Mettre à jour les URLs (sitemap, canonical, OG) avec le domaine final
- [ ] Activer Netlify Identity + Git Gateway
- [ ] Inviter l'admin dans Netlify Identity
- [ ] Ajouter un menu burger mobile
- [ ] Brancher la newsletter
- [ ] Analytics RGPD-friendly (Plausible, Matomo…)

## Licence

Projet privé — tous droits réservés.
