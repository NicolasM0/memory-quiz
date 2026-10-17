# Memory & Quiz — apprendre l'anglais en jouant

Deux jeux dans **un seul fichier `memory.html`** (HTML + CSS + JS + données, aucune
dépendance) :

- un **Memory** : retrouve les paires et écoute le mot anglais ;
- un **Quiz** : écoute un mot, choisis la bonne icône parmi 10.

Chaque mot est prononcé à voix haute (Web Speech API), pour enrichir le vocabulaire
anglais d'enfants francophones. Un menu d'accueil (`#home`) permet de passer d'un jeu à
l'autre ; tout se fait par ancres internes (`#memory`, `#quiz`), sans rechargement.

## Fonctionnalités

### Commun

- **15 thèmes** : Animaux, Nourriture, Actions, Objets, Couleurs, Nombres, Corps,
  Vêtements, Nature, École, Transports, Métiers, Émotions, Formes et Verbes
  (**925 mots** au total).
- Chaque mot est **lu à voix haute**.
- **Niveaux** de difficulté 1/2/3, dérivés de la fréquence d'usage des mots
  (25 % les plus courants / 25 % suivants / 50 % restants).
- Thème **Nombres** : la carte affiche le **chiffre en grand** (1 → 50) avec le mot anglais dessous.
- Choix de la **voix anglaise** (les 5 meilleures voix détectées).
- Réglages **mémorisés** (localStorage).

### Memory

- Bouton **« Traduction FR »** : relit et affiche la traduction française de la dernière carte.
- Mode **1 à 4 joueurs** (tour par tour, scores, annonce du vainqueur).
- Nombre de cartes et vitesse de la voix réglables.
- Disposition et taille des cartes calculées selon la fenêtre : grandes cartes sur un
  grand écran, jouable aussi sur téléphone (recalculées à chaque nouvelle partie).
- Confettis et son de victoire.

### Quiz

- **Sélection des catégories** (tout sélectionner / tout désélectionner) et du **niveau**.
- **Nombre de questions** configurable (5 → tout le pool), texte des cartes affichable ou non.
- Écoute du mot, choix parmi 10 icônes, bouton **« Répéter »**.
- Score (bonnes réponses / erreurs / pourcentage) et son de fin.

## Thèmes

| Thème | Mots | Thème | Mots | Thème | Mots |
| --- | ---: | --- | ---: | --- | ---: |
| Animaux | 112 | Nourriture | 98 | Actions | 109 |
| Objets | 119 | Couleurs | 14 | Nombres | 50 |
| Corps | 49 | Vêtements | 1 | Nature | 62 |
| École | 47 | Transports | 53 | Métiers | 44 |
| Émotions | 77 | Formes | 32 | Verbes | 58 |

Certains thèmes (Couleurs, Formes, Métiers, Verbes, Nombres) sont volontairement plus
courts : on ne garde que les mots dont l'emoji représente clairement le sens, plutôt que
d'utiliser une image trompeuse. Le menu des cartes n'affiche alors que les nombres de
cartes compatibles avec le thème choisi.

## Prérequis

- **Firefox** (le mieux pris en charge pour `speechSynthesis` sous Linux).
- Un moteur de synthèse vocale (sous Ubuntu : `speech-dispatcher` + `espeak-ng`).
  Pour des voix plus naturelles : `rhvoice`, `rhvoice-english`, `speech-dispatcher-rhvoice`,
  et pour le français `rhvoice-french`.
- Police emoji couleur : `fonts-noto-color-emoji` (les emojis plus récents que la
  version installée s'affichent en « tofu »).

## Utilisation

Ouvrir `memory.html` dans Firefox, ou depuis un terminal :

```bash
firefox memory.html
```

Choisir **Memory** ou **Quiz** sur l'accueil. Après une modification, recharger avec
**Ctrl+Shift+R** pour contourner le cache.

## Installation (PWA / hors-ligne)

L'application est aussi une **PWA** : elle s'installe et fonctionne hors-ligne.

- `manifest.json` : métadonnées d'installation (nom, icônes, mode `standalone`) ;
- `sw.js` : service worker (mise en cache des fichiers) ;
- `icon.png`, `icon-192.png`, `icon-512.png` : icônes de l'application, **créées pour
  ce projet** (elles sont regénérables avec `python3 tools/make-icons.py`, qui ne
  dépend d'aucune ressource externe).

Le service worker ne s'active que sur une origine sécurisée (`https://` ou
`http://localhost`) — **pas** en ouvrant le fichier en `file://`. Pour tester
l'installation, servir le dossier localement, par exemple :

```bash
python3 -m http.server 8000
```

puis ouvrir <http://localhost:8000/memory.html>. Le service worker est **versionné**
(`CACHE_VERSION` dans `sw.js`) : après une modification de `memory.html`, incrémenter
cette version pour que les navigateurs abandonnent l'ancien cache.

## Personnalisation

Tout se trouve dans `memory.html` :

- le premier `<script>` définit les données (`window.THEMES` = dictionnaire thème →
  `{ label, items:[…] }`, et `window.TRANSLATIONS` = dictionnaire anglais → français) ;
- les deux `<script>` suivants sont les jeux (Memory puis Quiz), chacun isolé dans une
  IIFE ; le dernier `<script>` est le petit routeur d'écrans (`#home` / `#memory` / `#quiz`).

Invariants à respecter en modifiant les mots :

- tout `name` doit avoir une entrée dans `TRANSLATIONS` ;
- chaque item doit porter un `level` (1, 2 ou 3), cohérent avec son ordre dans `items` ;
- `name` unique au sein d'un thème ; `emoji` peut se répéter si aucune image fidèle n'existe ;
- pour le thème `numbers`, le champ `emoji` contient le chiffre à afficher.

## Licence et crédits

Publié sous **CC0 1.0 Universal** (domaine public) — voir [`LICENSE`](LICENSE).

Auteur : **Nicolas Martin**.

Tout le contenu de ce dépôt est original et couvert par cette licence :

- **code** (`memory.html`, `sw.js`, `index.html`, `tools/make-icons.py`) ;
- **données** : les 925 mots anglais et leurs traductions françaises ;
- **icônes** (`icon*.png`) : dessins géométriques générés par `tools/make-icons.py`,
  sans utiliser aucune image tierce.

Aucune ressource externe n'est intégrée : les **emojis** sont rendus par la police
couleur du système (`fonts-noto-color-emoji`) et les **voix** proviennent de la
synthèse vocale du navigateur (Web Speech API).
