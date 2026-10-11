# Memory & Quiz — apprendre l'anglais en jouant

Un jeu de memory dans **un seul fichier `memory.html`** (HTML + CSS + JS, aucune dépendance).
Chaque carte révélée prononce son mot anglais à voix haute (Web Speech API), pour
enrichir le vocabulaire anglais d'enfants francophones.

## Fonctionnalités

- **15 thèmes** : Animaux, Nourriture, Actions, Objets, Couleurs, Nombres, Corps,
  Vêtements, Nature, École, Transports, Métiers, Émotions, Formes et Verbes
  (plus de **1 290 mots** au total).
- Chaque mot est **lu à voix haute** au retournement de la carte.
- **Niveaux** de difficulté 1/2/3, dérivés de la fréquence d'usage des mots
  (25 % les plus courants / 25 % suivants / 50 % restants).
- Bouton **« Traduction FR »** : relit et affiche la traduction française de la dernière carte.
- Thème **Nombres** : la carte affiche le **chiffre en grand** (1 → 50) avec le mot anglais dessous.
- Mode **1 à 4 joueurs** (tour par tour, scores, annonce du vainqueur).
- Nombre de cartes, vitesse de la voix réglable, choix de la voix anglaise.
- Disposition et taille des cartes calculées selon la fenêtre : grandes cartes sur un
  grand écran, jouable aussi sur téléphone (recalculées à chaque nouvelle partie).
- Confettis et son de victoire.
- Les réglages sont **mémorisés** (localStorage).

## Thèmes

| Thème | Mots | Thème | Mots | Thème | Mots |
| --- | ---: | --- | ---: | --- | ---: |
| Animaux | 112 | Nourriture | 100 | Actions | 112 |
| Objets | 124 | Couleurs | 14 | Nombres | 50 |
| Corps | 102 | Vêtements | 118 | Nature | 116 |
| École | 100 | Transports | 100 | Métiers | 47 |
| Émotions | 111 | Formes | 36 | Verbes | 73 |

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

Après une modification, recharger avec **Ctrl+Shift+R** pour contourner le cache.

## Personnalisation

Tout se trouve dans le `<script>` de `memory.html` :

- `THEMES` : mots de chaque thème, sous forme `{ name, emoji, label? }`.
- `TRANSLATIONS` : dictionnaire anglais → français (exactement une entrée par mot,
  sans entrée inutilisée ni doublon).
- `LEVEL_ORDER` : mots d'un thème classés du plus courant au moins courant (sert à
  calculer les niveaux). Facultatif : un thème absent retombe sur l'ordre de ses `items`.

Invariants à respecter en modifiant les mots :

- tout `name` doit avoir une entrée dans `TRANSLATIONS` ;
- `LEVEL_ORDER[thème]`, s'il existe, doit contenir exactement les mêmes noms que le thème ;
- `name` unique au sein d'un thème ; `emoji` peut se répéter si aucune image fidèle n'existe ;
- pour le thème `numbers`, le champ `emoji` contient le chiffre à afficher.

## Licence

Publié sous **CC0 1.0 Universal** (domaine public) — voir [`LICENSE`](LICENSE).

Auteur : **Nicolas Martin**.
