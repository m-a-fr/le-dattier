# Le Dattier — Guide Claude Code

## Structure du projet

```
le-dattier-project/
├── index.html        ← Page principale
├── style.css         ← Styles (charte noir et or)
├── products.js       ← CATALOGUE PRODUITS (fichier à modifier)
├── app.js            ← Logique du site
├── netlify.toml      ← Config Netlify
├── images/           ← Photos produits
└── README.md         ← Ce guide
```

## Mise en ligne sur Netlify (via GitHub)

Le site est connecté à GitHub. Chaque push déclenche un déploiement automatique.

Première fois :
1. Créer un repo GitHub et pousser le projet
2. Dans Netlify, connecter le repo (déjà fait)
3. Netlify déploie automatiquement à chaque push

Pour chaque mise à jour :
```
git add .
git commit -m "description"
git push
```

Le site est mis à jour en 30 secondes environ.

## Configuration Snipcart

1. Créer un compte sur https://snipcart.com
2. Account puis API Keys
3. Copier la clé publique (ST_ en test, SL_ en production)
4. Dans index.html, remplacer YOUR_API_KEY par votre clé
5. Dans Snipcart Dashboard, ajouter votre domaine Netlify

## Commandes Claude Code

Modifier un prix :
  "Change le prix de la Deglet Nour à 21,90 euros"

Ajouter un produit :
  "Ajoute un produit : Dattes Khudri, Arabie Saoudite, 500g, 15,90 euros"

Retirer un produit :
  "Retire les Capsules de Nigelle du catalogue"

Changer une description :
  "Change la description du Savon d Alep"

Ajouter un badge :
  "Mets le badge Nouveau sur l Huile de Nigelle Pure"

Créer une promotion :
  "Ajoute une bannière promo -10% avec le code BIENVENUE"

## Paiements (Stripe)

Dans Snipcart Dashboard, connecter Stripe.
Frais : 1,5% + 0,25 euro par transaction carte européenne.
Les fonds arrivent sous 2-7 jours.

## Livraison

Dans Snipcart Dashboard, configurer les tarifs.
Chaque produit a un poids (weight) dans products.js.

## Workflow quotidien

1. Ouvrir le terminal dans le dossier projet
2. Lancer claude
3. Demander les modifications en français
4. Vérifier localement (ouvrir index.html)
5. Déployer :
```
git add .
git commit -m "mise à jour produits"
git push
```
