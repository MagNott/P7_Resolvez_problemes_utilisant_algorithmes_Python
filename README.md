# Résolvez des problèmes en utilisant des algorithmes en Python



## Description
### Sélection optimisée d'actions en Python
Ce projet consiste à identifier **la combinaison d'actions la plus rentable** à acheter avec un budget limité (500 €), en maximisant le **profit total**.  
Il met en lumière l’importance du **choix d’un algorithme** au regard de la **rapidité d’exécution** et la **justesse des résultats**.

Deux algorithmes sont comparés :
- Un **brute-force** utilisant une **fonction récursive** qui teste toutes les combinaisons possibles.
- Un **optimisé**, basé sur la **programmation dynamique**.


## Installation et Prérequis
### Prérequis
Python 3.10+ (Vérifiez votre version avec python --version) Il faut que le gestionnaire de paquets python soit installé (pip)

### Installation
Clonez le projet

```
git clone https://github.com/MagNott/P7_Resolvez_problemes_utilisant_algorithmes_Python
cd P7_Resolvez_problemes_utilisant_algorithmes_Python
Installez les dépendances pip install -r requirements.txt
```

Installez les dépendances avec :

```bash
pip install rich
```

## Instructions d’utilisation

Pour tester les algorithmes avec les fichiers CSV fournis, vous pouvez exécuter les scripts suivants :
- **bruteforce.py** : exécute l’algorithme exhaustif.
- **optimized.py** : exécute l’algorithme rapide optimisé.

### Pour les lancer :
```
python bruteforce.py
python optimized.py
```

>Les fichiers de données doivent être au format CSV et comporter trois colonnes :
>- name : le nom de l'action
>- price : le coût de l'action (en euros, peut être négatif dans certains cas)
>- profit : le bénéfice attendu (en pourcentage)


### Les résultats s’affichent dans la console avec :
- La liste des actions sélectionnées
- Leur coût total
- Leur profit total
- Un temps d’exécution

# Qualité de code
## Convention de nommage
Utilisation de la notation hongroise

- Les paramètres de fonctions sont préfixés avec p_
- Les objets sont préfixés par o_
- Les entiers sont préfixés par i_
- Les chaines de caractères sont préfixés par s_
- Les listes sont préfixées par l_
- Les dictionnaires sont préfixés par d_

# Choix des algorithmes, performance et vérification
Dans ce projet, **deux méthodes ont été développées** pour résoudre le problème de sélection d’actions : 
- une **version brute force**, qui explore toutes les combinaisons possibles,
- une **version optimisée**, basée sur la **programmation dynamique**.

La première garantit une solution exacte mais devient rapidement très lente lorsque le volume de données augmente. La seconde donne également un résultat exact, tout en réduisant drastiquement le temps de calcul.

> L'approche brute force montre ses limites lorsqu'il s'agit de traiter un grand volume de données, en raison de son coût élevé en temps et en mémoire. Il n'est pas conseillé de l'utiliser sur de grandes quantités de données.

Des tests ont été menés sur plusieurs jeux de données afin d’observer les performances en temps et en mémoire. Ces tests ont montré que **l’approche optimisée est bien plus adaptée dès que la taille du dataset devient significative**.

Enfin, un backtesting a permis de valider la fiabilité des résultats : les actions sélectionnées par l’algorithme optimisé respectent bien les contraintes et permettent de maximiser le bénéfice dans la limite du budget.

# Auteur
Projet réalisé par MagNott dans le cadre du parcours développeur d'application Python chez OpenClassrooms.

