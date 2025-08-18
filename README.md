# DAT201

## Titres d'atelier

* (FR) **Analyse de données et visualisation en Python**
* (EN) **Data Analysis and Visualization in Python**

## Dépendances

Python >= 3.11, `pip install ...`:

* `numpy pandas matplotlib`
* `altair vega-datasets vl-convert-python`

## Fichiers sources

* Les fichiers à éditer sont dans `src/`.

### Métadonnées des cellules

Dans Jupyter Lab, à la droite d'un notebook, il y a un bouton
de roues dentées pour faire afficher le "Property Inspector".
C'est dans "ADVANCED TOOLS" qu'il faut éditer les métadonnées.

* (Obligatoire) Langue(s) de la cellule (de code ou Markdown) :
  * Anglais:  `"lang": "en"`
  * Français: `"lang": "fr"`
  * Les deux: `"lang": "en,fr"`
* Différencier la version à remplir et le solutionnaire :
  * Exercice : `"tags": ["exer"]`
  * Solution : `"tags": ["soln"]`

## Fichiers compilés

Les fichiers compilés et à utiliser pendant un atelier sont dans :

* `en` et `fr` pour les versions à remplir;
* `solution-en` et `solution-fr` pour les solutionnaires.

### Compilation

Pour cloner l'outil de compilation des traductions :

`git submodule update --init`

Ensuite :

* Compilation des dernières modifications : `python translation/make.py`
* Recompilation complète (rebuild) : `python translation/make.py -r`
