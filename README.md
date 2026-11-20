# All In Évent — site web

Site vitrine et catalogue de location de **All In Évent** (événementiel : casino, structures gonflables, son & lumière, team building, décoration sur mesure).

🌐 En ligne : https://allinevent.netlify.app

## Contenu

| Fichier | Rôle |
|---|---|
| `index.html` | Le site complet, prêt à publier (un seul fichier : HTML, CSS, JS, logo et catalogue inclus) |
| `src/site.html` | Structure, textes et code JavaScript du site |
| `src/base.css` | Styles de base (thème noir et or) |
| `src/produits.txt` | Catalogue : une ligne par produit `rayon\|catégorie\|nom\|prix HT par jour` (prix vide = « Sur devis ») |
| `src/photos.csv` | Photo Unsplash associée à chaque produit (même ordre que `produits.txt`, `-` = photo de la catégorie) |
| `src/logo.jpg`, `src/logo.webp` | Logo (version fond noir pour le PDF, version détourée pour le site) |
| `build.py` | Reconstruit `index.html` à partir de `src/` |

## Fonctionnalités

- Catalogue de 203 articles avec recherche, filtres par rayon et prix HT/TTC
- Sélection d'articles et estimation automatique du devis
- Formulaire de devis en 3 étapes, envoyé via **Netlify Forms** (notifications par email)
- Génération d'un **PDF de demande de devis** (logo, numéro, articles, totaux) téléchargé par le client et joint à la demande
- Vidéo de fond (Pexels) et photos d'illustration (Unsplash), libres de droits

## Modifier le site

1. Modifier les fichiers dans `src/` (par exemple un prix dans `src/produits.txt`).
2. Lancer `python3 build.py` pour régénérer `index.html`.
3. Publier : glisser `index.html` (ou le dossier) dans Netlify → projet *allinevent* → **Deploys**.

## Crédits

Photos : [Unsplash](https://unsplash.com) · Vidéo : [Pexels](https://www.pexels.com) · PDF : [jsPDF](https://github.com/parallax/jsPDF)
