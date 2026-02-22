# Le Dattier — Instructions Claude Code

> **Contexte complet du projet :** consulter `HISTORIQUE.md` pour l'historique des décisions,
> la charte graphique, le catalogue produits détaillé, et la liste des tâches restantes.

---

## ⚠️ RÈGLE ABSOLUE — CHECKLIST PRÉ-LIVRAISON

**Avant TOUTE livraison au propriétaire** (ZIP, commit, déploiement), exécuter :

```bash
python3 sync-produits.py    # Sync JSON → JS + HTML + JSON-LD
python3 check-projet.py     # Validation cohérence + SEO + README
```

**Ne jamais livrer si `check-projet.py` retourne des erreurs (❌).**

Les warnings (⚠️) sont tolérables mais doivent être signalés au propriétaire.

### Quand lancer la checklist ?

**TOUJOURS.** Même si la modification semble anodine. Même si le propriétaire
ne demande pas de vérification. Même si la modification ne touche pas les produits.

### Que vérifie check-projet.py ?

**Cohérence produits :**
- produits.json valide (JSON parseable, champs obligatoires, types corrects)
- produits.json ↔ products.js (même nombre, mêmes IDs)
- produits.json ↔ bloc hidden index.html (même nombre, mêmes prix)
- produits.json ↔ JSON-LD (même nombre)
- Images produits existent
- Catégories JSON ↔ boutons filtres index.html
- Pas de doublons d'ID

**Conformité SEO :**
- Chaque page : title (20-70 car.), meta description (80-165 car.), canonical, h1 unique, Open Graph, favicon, preconnect, ARIA, lang="fr"
- Hiérarchie headings correcte
- Fichiers globaux : robots.txt, sitemap.xml, favicon.svg, 404.html
- JSON-LD Organization + WebSite + ItemList + FAQPage
- Scripts locaux en defer
- Admin Decap CMS : index.html + config.yml présents

**Cohérence README :**
- Nombre de produits correspond au JSON
- Catégories mentionnées
- Fichiers clés listés
- Pages HTML documentées

### Workflow complet de livraison

```
1. Effectuer les modifications demandées
2. Si produits touchés → python3 sync-produits.py
3. Si structure du projet modifiée → mettre à jour README.md
4. python3 check-projet.py
5. Si erreurs → corriger et recommencer à l'étape 4
6. Livrer (ZIP ou git add . && git commit && git push)
```

### Quand mettre à jour README.md ?

Le README est la vitrine du projet sur GitHub. Il doit rester synchronisé :
- Ajout/suppression de fichier, page ou catégorie → mettre à jour la structure
- Changement de nombre de produits → mettre à jour le tableau catalogue
- Changement de stack ou outil → mettre à jour la section correspondante
- Complétion d'une tâche → la cocher dans la todo list

---

## Architecture

```
le-dattier-project/
├── produits.json             <- SOURCE UNIQUE DES PRODUITS
├── sync-produits.py          <- Sync JSON → products.js + index.html + JSON-LD
├── check-projet.py           <- Validation pré-livraison
├── admin/
│   ├── index.html            <- Interface Decap CMS
│   └── config.yml            <- Configuration champs/collections
├── index.html                <- Page d'accueil
├── faq.html                  <- FAQ + JSON-LD FAQPage
├── livraison.html            <- Livraison & Retours
├── cgv.html                  <- CGV
├── mentions-legales.html     <- Mentions légales + RGPD
├── 404.html                  <- Page 404 personnalisée
├── style.css                 <- Charte graphique (noir & or)
├── snipcart-theme.css        <- Thème Snipcart
├── products.js               <- AUTO-GÉNÉRÉ par sync-produits.py
├── app.js                    <- Filtres, animations, panier
├── favicon.svg
├── robots.txt
├── sitemap.xml
├── netlify.toml              <- Build command + headers + cache + 404
├── images/
│   ├── site/
│   └── produits/{dattes,savons,nigelle}/
├── CLAUDE.md, HISTORIQUE.md, README.md
└── .gitignore
```

---

## Gestion des produits

### Source unique : produits.json

Deux façons de modifier les produits :

**Via l'admin web (Decap CMS) — méthode principale :**
1. Aller sur `https://www.ledattier.fr/admin/`
2. Se connecter (Netlify Identity)
3. Modifier les produits via l'interface
4. Cliquer "Publier"
5. Decap CMS commit dans GitHub → Netlify rebuild avec `sync-produits.py` automatique

**Via le code (Claude Code / manuellement) :**
1. Modifier `produits.json`
2. `python3 sync-produits.py` → régénère products.js + bloc hidden + JSON-LD
3. `python3 check-projet.py` → validation
4. `git push` → Netlify rebuild

### Ce que sync-produits.py régénère

1. **products.js** → catalogue JS pour l'affichage client
2. **index.html bloc hidden** → validation prix par le crawler Snipcart
3. **index.html JSON-LD** → données structurées produits pour Google

⚠️ NE JAMAIS modifier products.js à la main — il sera écrasé.

### Format de produits.json

```json
{
  "produits": [
    {
      "id": "datte-medjool",
      "nom": "Medjool Royale",
      "origine": "Palestine",
      "categorie": "dattes",
      "description": "Charnue et généreuse, aux saveurs de caramel beurré.",
      "prix": 24.50,
      "unite": "500g",
      "badge": "new",
      "image": "images/produits/dattes/medjool.jpg",
      "poids": 520
    }
  ]
}
```

Règles :
- id : texte unique en kebab-case
- categorie : "dattes", "savons" ou "nigelle"
- prix : nombre décimal (ex: 18.90)
- badge : "new", "best" ou "" (vide)
- poids : entier en grammes
- image : chemin relatif vers images/produits/[categorie]/[nom].jpg

### Commandes fréquentes

**Modifier un prix :** produits.json → sync → check → git push
**Ajouter un produit :** photo + produits.json → sync → check → git push
**Retirer un produit :** supprimer dans produits.json → sync → check → git push
**Ajouter une catégorie :** dossier image + produits.json + bouton filtre dans index.html + option dans admin/config.yml → sync → check → git push
**Ajouter une page HTML :** créer avec même head SEO + ajouter dans sitemap.xml → check → git push

---

## Admin Decap CMS

### Fonctionnement

- **Interface :** `/admin/` (Decap CMS hébergé côté client, pas de backend)
- **Auth :** Netlify Identity (email/mot de passe)
- **Storage :** Git Gateway (Decap commit directement dans le repo GitHub)
- **Build :** Chaque commit déclenche Netlify → `python3 sync-produits.py` → déploiement

### Configuration initiale (à faire une fois)

1. Dans Netlify Dashboard → **Identity** → Activer
2. Aller dans **Identity > Settings > Services > Git Gateway** → Activer
3. Inviter l'admin par email (Identity > Invite users)
4. L'admin reçoit un email, crée son mot de passe
5. Se connecter sur `https://www.ledattier.fr/admin/`

### Ajouter une catégorie dans l'admin

Modifier `admin/config.yml`, section `categorie` :
```yaml
- name: "categorie"
  widget: "select"
  options:
    - { label: "Dattes", value: "dattes" }
    - { label: "Savons", value: "savons" }
    - { label: "Huile de Nigelle", value: "nigelle" }
    - { label: "Nouvelle catégorie", value: "nouveau" }  # ← ajouter ici
```
Et ajouter un bouton filtre dans index.html.

---

## SEO — Règles à respecter

### Pour chaque page HTML
- `<title>` : 20-70 caractères, mots-clés pertinents
- `<meta name="description">` : 80-165 caractères
- `<link rel="canonical">` : URL absolue
- Favicon, preconnect, Open Graph, lang="fr", 1 seul h1, hiérarchie correcte, ARIA

### Pour le site global
- robots.txt, sitemap.xml, favicon.svg, 404.html
- JSON-LD (Organization, WebSite, ItemList, FAQPage)
- Scripts en defer
- Admin non indexé (robots.txt Disallow + meta noindex)

---

## Snipcart

- Clé API dans les pages HTML : `<div id="snipcart" data-api-key="...">`
- Validation prix via bloc `<div hidden>` (généré par sync-produits.py)
- Compteur panier : `.snipcart-items-count` / Bouton : `.snipcart-checkout`

## Catégories

Définies à **quatre** endroits (sync gère 2/4 automatiquement) :
1. ✅ produits.json → source
2. ✅ products.js → auto-généré
3. ⚠️ Boutons filtres dans index.html → manuel si nouvelle catégorie
4. ⚠️ Options dans admin/config.yml → manuel si nouvelle catégorie

## Déploiement

```bash
git push
```

Netlify exécute automatiquement `python3 sync-produits.py` puis déploie.

## Notes techniques

- Snipcart valide les prix en crawlant le bloc hidden
- data-item-url="/" dans app.js pointe vers index.html
- Le site est responsive (breakpoint 900px)
- Les h4 du footer sont hors hiérarchie SEO
- Netlify Identity widget chargé sur index.html pour la redirection admin
