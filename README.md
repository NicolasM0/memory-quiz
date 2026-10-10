# Memory Game — apprendre l'anglais en jouant

Un jeu de memory dans **un seul fichier `memory.html`** (HTML + CSS + JS, aucune dépendance).
Chaque carte révélée prononce son mot anglais à voix haute (Web Speech API), pour
enrichir le vocabulaire anglais d'enfants francophones.

## Fonctionnalités

- 4 thèmes : **Animaux**, **Nourriture**, **Actions**, **Objets** (100 à 124 mots chacun).
- Chaque mot est **lu à voix haute** au retournement de la carte.
- **Niveaux** de difficulté 1/2/3, dérivés de la fréquence d'usage des mots
  (25 % les plus courants / 25 % suivants / 50 % restants).
- Bouton **« Traduction FR »** : relit et affiche la traduction française de la dernière carte.
- Mode **1 à 4 joueurs** (tour par tour, scores, annonce du vainqueur).
- Nombre de cartes (4 à 100), vitesse de la voix réglable, choix de la voix anglaise.
- Disposition et taille des cartes calculées selon la fenêtre : grandes cartes sur un
  grand écran, jouable aussi sur téléphone (recalculées à chaque nouvelle partie).
- Confettis et son de victoire.
- Les réglages sont **mémorisés** (localStorage).

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

- `THEMES` : mots de chaque thème, sous forme `{ name, emoji }`.
- `TRANSLATIONS` : dictionnaire anglais → français (une entrée par mot).
- `LEVEL_ORDER` : mots de chaque thème classés du plus courant au moins courant
  (sert à calculer les niveaux).

Invariants à respecter en modifiant les mots :

- tout `name` doit avoir une entrée dans `TRANSLATIONS` ;
- `LEVEL_ORDER[thème]` doit contenir exactement les mêmes noms que le thème ;
- `name` et `emoji` uniques au sein d'un thème.

## Licence

Publié sous **CC0 1.0 Universal** (domaine public) — voir [`LICENSE`](LICENSE).

Auteur : **Nicolas Martin**.
