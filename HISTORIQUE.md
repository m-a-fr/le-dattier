# Le Dattier — Historique du projet

> Ce fichier permet de reprendre le travail dans une nouvelle conversation Claude.
> En cas de nouvelle session, partager ce fichier + le ZIP du projet pour avoir tout le contexte.

---

## Résumé du projet

**Le Dattier** est un site e-commerce de produits orientaux haut de gamme : dattes d'exception, savons artisanaux et huile de nigelle. Le positionnement est luxe/premium avec une charte graphique noir & or.

---

## Stack technique

| Composant | Choix | Coût |
|---|---|---|
| Hébergement | Netlify (plan gratuit, commercial autorisé) | 0 € |
| E-commerce / Panier | Snipcart v3.7.1 | ~11 €/mois (2% transactions) |
| Paiement | Stripe (via Snipcart) | 1,5% + 0,25 € / transaction |
| Code | HTML/CSS/JS statique (pas de framework) | — |
| Gestion produits | CSV (produits.csv) + script Python (sync-produits.py) | — |
| Déploiement | Git push → Netlify auto-deploy | — |
| Domaine | À acheter (pas encore fait) | ~10 €/an |

**Alternatives évaluées et écartées :**
- Medusa.js : trop complexe, nécessite serveur Node.js (~25 €/mois min)
- Vercel : plan gratuit interdit pour usage commercial
- GitHub Pages : interdit pour e-commerce (CGU GitHub)
- Cloudflare Pages : viable mais Netlify déjà configuré

---

## Architecture des fichiers

```
le-dattier-project/
├── produits.csv              <- SOURCE UNIQUE DES PRODUITS (UTF-8 BOM, séparateur ;)
├── sync-produits.py          <- Sync CSV → products.js + index.html + JSON-LD
├── check-projet.py           <- ⚠️ VALIDATION PRÉ-LIVRAISON (cohérence + SEO)
├── index.html                <- Page d'accueil (hero, boutique, histoire, engagements, newsletter)
├── faq.html                  <- 10 Q&A avec accordéon JS
├── livraison.html            <- Tarifs, retours, droit de rétractation
├── cgv.html                  <- 13 articles CGV (contient des [CROCHETS] à remplir)
├── mentions-legales.html     <- Mentions légales + RGPD (contient des [CROCHETS] à remplir)
├── style.css                 <- Charte graphique noir & or (~504 lignes)
├── snipcart-theme.css        <- Thème Snipcart assorti (~313 lignes)
├── products.js               <- AUTO-GÉNÉRÉ — ne pas modifier à la main
├── app.js                    <- Rendu produits, filtres catégorie, animations scroll, toast panier
├── netlify.toml              <- Headers sécurité + cache images/CSS/JS
├── .gitignore
├── images/
│   ├── site/                 <- hero.jpg, story.jpg, values-bg.jpg
│   └── produits/             <- Photos par catégorie
│       ├── dattes/           <- 6 images (deglet-nour, medjool, ajwa, sukari, mazafati, coffret)
│       ├── savons/           <- 4 images (alep-laurier, nigelle, rose, olive)
│       └── nigelle/          <- 4 images (pure, bio, capsules, coffret)
├── CLAUDE.md                 <- Instructions pour Claude Code
├── README.md                 <- Guide utilisateur
└── HISTORIQUE.md             <- Ce fichier
```

---

## Catalogue produits (14 produits)

### Dattes (6)
| ID | Nom | Origine | Prix | Badge |
|---|---|---|---|---|
| datte-deglet-nour | Deglet Nour Premium | Algérie | 18,90 € / 500g | best |
| datte-medjool | Medjool Royale | Palestine | 24,50 € / 500g | new |
| datte-ajwa | Ajwa de Médine | Arabie Saoudite | 32,00 € / 400g | — |
| datte-sukari | Sukari d'Al-Qassim | Arabie Saoudite | 28,00 € / 400g | — |
| datte-mazafati | Mazafati de Bam | Iran | 19,90 € / 500g | — |
| datte-coffret | Coffret Découverte Dattes | Multi-origines | 45,00 € / coffret | new |

### Savons (4)
| ID | Nom | Origine | Prix | Badge |
|---|---|---|---|---|
| savon-alep-laurier | Savon d'Alep au Laurier | Syrie | 12,90 € / 200g | best |
| savon-nigelle | Savon Noir à la Nigelle | Maroc | 9,90 € / 150g | — |
| savon-rose | Savon à la Rose de Damas | Turquie | 11,50 € / 150g | new |
| savon-olive | Savon à l'Huile d'Olive | Palestine | 8,90 € / 120g | — |

### Nigelle (4)
| ID | Nom | Origine | Prix | Badge |
|---|---|---|---|---|
| nigelle-pure | Huile de Nigelle Pure | Égypte | 16,90 € / 100ml | best |
| nigelle-bio | Huile de Nigelle Bio | Éthiopie | 22,50 € / 100ml | new |
| nigelle-capsules | Capsules de Nigelle | Égypte | 18,90 € / 60 caps | — |
| nigelle-coffret | Coffret Nigelle Prestige | Égypte | 39,90 € / coffret | — |

---

## Clé API Snipcart

Clé publique (test) déjà intégrée dans toutes les pages HTML :
```
MmFjNTM2NjAtMjdhMy00ZTZiLTg5NjQtYTIyM2YyMjY5YWViNjM5MDczMTc2OTEwNDg4OTAw
```

---

## Mécanisme Snipcart — Crawler & validation

Snipcart valide les prix en crawlant la page HTML. Comme les produits sont rendus en JS (app.js), le crawler ne les voit pas. Solution : un bloc `<div hidden>` dans index.html contient des `<button class="snipcart-add-item">` statiques pour chaque produit.

Le script `sync-produits.py` met à jour ce bloc automatiquement en même temps que `products.js`.

**Les deux sources (products.js et le bloc hidden) doivent avoir les mêmes prix**, sinon erreur "Le prix a changé" au checkout.

---

## Workflow gestion produits

1. Modifier `produits.csv` (Excel, LibreOffice, éditeur texte)
2. Lancer `python3 sync-produits.py`
3. `git add . && git commit -m "description" && git push`

Le CSV est encodé **UTF-8 avec BOM** pour compatibilité Excel/LibreOffice français. Le script lit avec `encoding="utf-8-sig"`.

Colonnes CSV : `id;nom;origine;categorie;description;prix;unite;badge;image;poids`

---

## Design — Charte graphique

| Variable | Valeur | Usage |
|---|---|---|
| --gold | #D4B472 | Accent principal, boutons, liens |
| --gold-light | #E8D9B5 | Hover states |
| --gold-dark | #A07D2E | — |
| --noir | #080807 | Fond principal |
| --noir-soft | #121110 | Fond sections alternées |
| --noir-card | #0E0D0B | Fond cartes produit |
| --creme | #FBF8F2 | Titres |
| --text-body | #E0D9CD | Texte courant |
| --text-light | #C4BAA9 | Texte secondaire |
| --burgundy | #8B3A50 | Badge "Best-seller" |

Typographies :
- Titres : Cormorant Garamond (serif, élégant)
- Corps : Jost (sans-serif, moderne)

---

## Workflow de livraison (OBLIGATOIRE)

Avant toute livraison (ZIP, commit, déploiement), cette séquence est obligatoire :

```bash
python3 sync-produits.py    # Régénère products.js + bloc hidden + JSON-LD
python3 check-projet.py     # Vérifie cohérence produits + conformité SEO
```

Si `check-projet.py` retourne des erreurs (❌), corriger avant de livrer.

Ce workflow s'applique **même si les modifications ne touchent pas les produits**.
Le propriétaire peut avoir modifié le CSV sans le mentionner, ou un changement
de structure HTML peut casser accidentellement le bloc hidden Snipcart ou le SEO.

---

## Décisions prises

| Date | Décision | Raison |
|---|---|---|
| 22/02 | Snipcart + Netlify | Moins cher, plus simple que Medusa |
| 22/02 | Architecture multi-fichiers | HTML/CSS/JS séparés, pas de framework |
| 22/02 | Approche mixte pages | Index.html + pages légales séparées |
| 22/02 | CSV comme source produits | Plus simple qu'éditer du JS pour le propriétaire |
| 22/02 | UTF-8 BOM pour le CSV | Compatibilité Excel/LibreOffice français |
| 22/02 | Suppression des emojis | Éviter erreurs d'encodage et oublis |
| 22/02 | Images rangées par catégorie | images/produits/[categorie]/[nom].jpg |
| 23/02 | Rester sur Netlify | Commercial autorisé (interdit Vercel gratuit et GitHub Pages) |

---

## Ce qui reste à faire

### Obligatoire avant mise en ligne
- [ ] Remplacer les images placeholder par de vraies photos produit
- [ ] Remplir les [CROCHETS] dans cgv.html (SIRET, adresse, raison sociale, médiateur)
- [ ] Remplir les [CROCHETS] dans mentions-legales.html (mêmes infos)
- [ ] Connecter Stripe en mode live dans le dashboard Snipcart
- [ ] Ajouter le domaine dans le dashboard Snipcart
- [ ] Acheter et configurer le nom de domaine
- [ ] Mettre à jour les URLs dans sitemap.xml, canonical et OG si le domaine change
- [ ] Créer le repo GitHub et faire le premier push
- [ ] Connecter le repo à Netlify

### Améliorations possibles
- [ ] Ajouter un menu burger pour mobile (actuellement les liens nav sont cachés sous 900px)
- [ ] Brancher la newsletter (Mailchimp, Brevo, ou autre)
- [x] ~~Ajouter des métadonnées Open Graph / Twitter Cards~~ (fait)
- [ ] Optimiser les images (compression, format WebP, lazy loading déjà en place)
- [x] ~~Ajouter un favicon~~ (fait)
- [x] ~~SEO : sitemap.xml, robots.txt~~ (fait)
- [x] ~~JSON-LD données structurées~~ (fait)
- [x] ~~Page 404 personnalisée~~ (fait)
- [x] ~~ARIA / accessibilité de base~~ (fait)
- [ ] Analytics (Plausible ou Matomo pour rester RGPD-friendly)
- [ ] Bannière cookies si ajout d'analytics

### Notes techniques
- Le site est responsive (breakpoint 900px) mais le menu mobile n'a pas de burger menu
- Les pages légales sont des modèles — faire valider par un juriste
- Snipcart est en mode test tant que Stripe n'est pas connecté en live
- Les images actuelles sont des placeholders de ~10-40 Ko chacune

---

## Historique des sessions

### Session 1 (22/02/2026 — matin)
- Choix de la stack technique (Snipcart vs Medusa, analyse des coûts)
- Création du design UI/UX et de la maquette visuelle
- Génération des images placeholder produits
- Architecture du projet et premiers fichiers

### Session 2 (22/02/2026 — après-midi)
- Implémentation complète du site multi-fichiers
- Intégration Snipcart avec clé API
- Déploiement GitHub + Netlify configuré
- 14 produits dans 3 catégories

### Session 3 (22/02/2026 — soir)
- Création des 4 pages légales (FAQ, livraison, CGV, mentions légales)
- Audit des liens et correction des chemins
- Fix du crawler Snipcart (bloc hidden statique)
- Création du thème Snipcart noir & or (snipcart-theme.css)
- Mise en place du système CSV + sync-produits.py
- Test d'intégration de vraie photo produit (savon d'Alep)

### Session 4 (23/02/2026 — actuelle)
- Suppression de la colonne emoji du CSV et de tout le code associé
- Encodage UTF-8 avec BOM pour compatibilité Excel/LibreOffice français
- Réorganisation des images : images/site/ et images/produits/[categorie]/
- Mise à jour de CLAUDE.md avec les procédures détaillées
- Comparaison Netlify vs Vercel → Netlify confirmé (commercial gratuit)
- Vérification GitHub Pages → interdit pour e-commerce
- Création de HISTORIQUE.md pour la continuité inter-sessions
- **Audit SEO complet + implémentation des 15 optimisations :**
  1. robots.txt créé (allow all, lien sitemap)
  2. sitemap.xml créé (5 pages, priorités pondérées)
  3. Balises canonical sur les 5 pages principales
  4. JSON-LD : Organization + WebSite + ItemList (14 produits) + FAQPage (8 Q&A)
  5. Données structurées produits auto-générées par sync-produits.py
  6. Open Graph + Twitter Card sur les 5 pages
  7. Favicon SVG (D doré sur fond noir)
  8. Preconnect pour Google Fonts, Gstatic, Snipcart CDN
  9. Hiérarchie headings corrigée (h1 → h2 au lieu de h1 → h3) + CSS mis à jour
  10. Scripts products.js et app.js chargés en defer
  11. Chargement Google Fonts optimisé
  12. Meta descriptions allongées et enrichies en mots-clés
  13. Attributs ARIA ajoutés (nav, filtres, newsletter, boutons panier, accordéon)
  14. Page 404 personnalisée + redirection dans netlify.toml
  15. h1 de l'accueil optimisé SEO ("Dattes d'exception, savons & nigelle")
- **Création du workflow de pré-livraison :**
  - check-projet.py : script de validation automatique (cohérence produits + audit SEO)
  - CLAUDE.md réécrit avec la règle absolue de pré-livraison en tête de fichier
  - HISTORIQUE.md mis à jour avec le workflow
  - Le workflow s'applique systématiquement, même si le propriétaire ne le demande pas

---

*Dernière mise à jour : 23 février 2026*
