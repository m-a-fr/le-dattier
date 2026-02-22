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
| Gestion produits | JSON (produits.json) + Decap CMS + script Python (sync-produits.py) | — |
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
├── produits.json             <- SOURCE UNIQUE DES PRODUITS
├── sync-produits.py          <- Sync JSON → products.js + index.html + JSON-LD
├── check-projet.py           <- ⚠️ VALIDATION PRÉ-LIVRAISON (cohérence + SEO + README)
├── admin/
│   ├── index.html            <- Interface Decap CMS
│   └── config.yml            <- Configuration champs/collections
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

## Catalogue produits (13 produits)

### Dattes (5)
| ID | Nom | Origine | Prix | Badge | Image |
|---|---|---|---|---|---|
| datte-deglet-nour | Deglet Nour Premium | Algérie | 5,90 € / 500g | best | vraie photo (Decap) |
| datte-medjool | Medjool Royale | Palestine | 24,50 € / 500g | new | vraie photo (Decap) |
| datte-ajwa | Ajwa de Médine | Arabie Saoudite | 32,00 € / 400g | — | vraie photo (Decap) |
| datte-sukari | Sukari d'Al-Qassim | Arabie Saoudite | 28,00 € / 400g | — | vraie photo (Decap) |
| datte-mazafati | Mazafati de Bam | Iran | 19,90 € / 500g | — | vraie photo (Decap) |

### Savons (4)
| ID | Nom | Origine | Prix | Badge | Image |
|---|---|---|---|---|---|
| savon-alep-laurier | Savon d'Alep au Laurier | Syrie | 12,90 € / 200g | best | placeholder |
| savon-nigelle | Savon Noir à la Nigelle | Maroc | 9,90 € / 150g | — | placeholder |
| savon-rose | Savon à la Rose de Damas | Turquie | 11,50 € / 150g | new | placeholder |
| savon-olive | Savon à l'Huile d'Olive | Palestine | 8,90 € / 120g | — | placeholder |

### Nigelle (4)
| ID | Nom | Origine | Prix | Badge | Image |
|---|---|---|---|---|---|
| nigelle-pure | Huile de Nigelle Pure | Égypte | 16,90 € / 100ml | best | placeholder |
| nigelle-bio | Huile de Nigelle Bio | Éthiopie | 22,50 € / 100ml | new | placeholder |
| nigelle-capsules | Capsules de Nigelle | Égypte | 18,90 € / 60 caps | — | placeholder |
| nigelle-coffret | Coffret Nigelle Prestige | Égypte | 39,90 € / coffret | — | placeholder |

### Organisation des images

- **Dattes** : 5 vraies photos uploadées via Decap CMS → stockées directement dans `images/produits/` (noms générés par Decap). Le dossier `images/produits/dattes/` contient les anciens placeholders, non utilisés.
- **Savons** : 4 placeholders dans `images/produits/savons/`
- **Nigelle** : 4 placeholders dans `images/produits/nigelle/`

⚠️ À terme : remplacer les placeholders savons/nigelle par de vraies photos, et normaliser les noms des images dattes.

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

1. Modifier `produits.json` (via admin web Decap CMS ou manuellement)
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
git pull                        # Récupérer les changements distants (Decap CMS, collaborateurs)
python3 sync-produits.py    # Régénère products.js + bloc hidden + JSON-LD depuis produits.json
python3 check-projet.py     # Vérifie cohérence produits + conformité SEO + README
```

Si `check-projet.py` retourne des erreurs (❌), corriger avant de livrer.

Ce workflow s'applique **même si les modifications ne touchent pas les produits**.
Le propriétaire peut avoir modifié le JSON via l'admin web sans le mentionner.

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
- [x] ~~Remplacer les images dattes par de vraies photos~~ (fait via Decap CMS)
- [ ] Remplacer les images placeholder savons et nigelle par de vraies photos
- [ ] Normaliser les noms de fichiers des images dattes (uploadées avec noms auto par Decap)
- [ ] Remplir les [CROCHETS] dans cgv.html (SIRET, adresse, raison sociale, médiateur)
- [ ] Remplir les [CROCHETS] dans mentions-legales.html (mêmes infos)
- [ ] Connecter Stripe en mode live dans le dashboard Snipcart
- [ ] Ajouter le domaine dans le dashboard Snipcart
- [ ] Acheter et configurer le nom de domaine
- [ ] Mettre à jour les URLs dans sitemap.xml, canonical et OG si le domaine change
- [ ] Créer le repo GitHub et faire le premier push
- [ ] Connecter le repo à Netlify
- [ ] Activer Netlify Identity dans le dashboard Netlify
- [ ] Activer Git Gateway (Identity > Settings > Services)
- [ ] Inviter l'admin par email (Identity > Invite users)

### Améliorations possibles
- [ ] Flèche retour mobile dans le cart Snipcart — code en place (MutationObserver + `.snipcart-modal__close`), à valider une fois le site déployé avec la clé live (les events/classes Snipcart sont inactifs en mode test)
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
- Les images dattes sont des vraies photos, savons/nigelle restent des placeholders (~10-40 Ko)
- Les images uploadées via Decap CMS ont des noms générés automatiquement (non normalisés)

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

### Session 4 (23/02/2026)
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
- **Migration vers Decap CMS :**
  - produits.csv → produits.json (source unique)
  - CSV supprimé définitivement
  - Dossier admin/ créé (index.html + config.yml Decap CMS)
  - sync-produits.py réécrit pour lire JSON au lieu de CSV
  - check-projet.py réécrit pour valider JSON au lieu de CSV
  - netlify.toml : ajout build command `python3 sync-produits.py` (auto au deploy)
  - robots.txt : ajout Disallow /admin/
  - Widget Netlify Identity ajouté sur index.html
  - Auth : Netlify Identity (email/mdp, gratuit 5 users)
  - Workflow autonome : admin modifie via /admin/ → Decap commit → Netlify rebuild auto
  - CLAUDE.md, README.md, HISTORIQUE.md mis à jour

### Session 5 (22/02/2026)
- **Modifications produits via Decap CMS (entre sessions) :**
  - `datte-coffret` supprimé du catalogue → 13 produits
  - Prix `datte-deglet-nour` modifié : 18,90 € → 5,90 €
  - 5 vraies photos dattes uploadées via Decap CMS (stockées dans `images/produits/` racine)
- **Resynchronisation et mise à jour des docs :**
  - Incohérences détectées (products.js/hidden/JSON-LD encore à 14 produits) → sync lancé
  - `sync-produits.py` relancé → products.js + bloc hidden + JSON-LD remis à 13 produits
  - `check-projet.py` : 0 erreur, 0 warning après correction
  - README.md, HISTORIQUE.md mis à jour pour refléter l'état réel du repo

### Session 6 (22/02/2026)
- **Tentative : bouton "retour à la boutique" sur mobile dans le cart Snipcart**
  - Problème identifié : le navbar fixe (`z-index: 100`) masque l'en-tête natif Snipcart sur mobile, cachant le lien de fermeture natif
  - Approche 1 abandonnée : injection d'un bouton via `Snipcart.events.on('cart.opened')` → les events Snipcart ne se déclenchent pas sans clé live
  - Approche 2 abandonnée : abaissement du `z-index` navbar via events Snipcart → même problème
  - Approche 3 abandonnée : `html.snipcart-active` en CSS pur → la classe n'est pas ajoutée par Snipcart en mode test
  - Approche 4 en cours (non résolue) : MutationObserver sur `<html>` + clic sur `.snipcart-modal__close` → fonctionne en simulation locale mais pas en prod
  - Conclusion : les events et classes Snipcart semblent inactifs en mode test (sans clé live + domaine configuré). À tester une fois le site déployé avec la vraie clé.
  - Code en place dans `app.js` et `style.css`, prévisualisation validée (`preview-navbar-mobile.html`)
  - HISTORIQUE.md mis à jour

---

*Dernière mise à jour : 22 février 2026*
