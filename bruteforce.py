import csv
import os
from rich.table import Table
from rich.console import Console
from rich import print


# FONCTIONS
def read_csv(p_csv_name: str) -> list[list[str]]:
    """
    Lit un fichier CSV et retourne son contenu sous forme de liste de lignes.

    Paramètres :
    ----------
    p_csv_name : str
        Nom du fichier CSV à lire (avec le chemin si nécessaire).

    Retour :
    -------
    l_work_file : list[list[str]]
        Liste contenant toutes les lignes du fichier CSV,
        chaque ligne étant une liste de chaînes représentant les colonnes.

    Remarques :
    ----------
    - Si le fichier n'existe pas, affiche un message d'erreur.
    - Le fichier est lu sans modification des types (tout reste en chaîne).
    """
    if not os.path.exists(p_csv_name):
        print(f"Le fichier {p_csv_name} n'est pas trouvé")
    else:
        l_work_file = []
        with open(p_csv_name, newline='', encoding='utf-8') as f:
            o_reader = csv.reader(f)
            for l_row in o_reader:
                l_work_file.append(l_row)
    return l_work_file


def calculate_profits(p_actions_list: list[list[str]]):
    """
    Calcule le bénéfice en euros pour chaque action et l'ajoute à la liste.

    Paramètres :
    ----------
    p_actions_list : list[list[str]]
        Liste contenant les données d'actions. Chaque sous-liste représente une ligne :
        [nom de l'action, coût en euros (str), pourcentage de profit (str, ex. "5%")].

    Effets de bord :
    ---------------
    - Ajoute une nouvelle colonne "Profit (€)" à l'en-tête.
    - Ajoute le bénéfice calculé (float) à chaque ligne.
    - Affiche les lignes modifiées pour vérification.

    Remarques :
    ----------
    - Les champs numériques sont convertis en float pour le calcul.
    - Le bénéfice est arrondi à 2 décimales.
    """
    p_actions_list[0].append("Profit (€)")
    for l_row in p_actions_list[1:]:
        f_cost = float(l_row[1])
        f_percent = float(l_row[2].replace("%", ""))
        f_benefit = f_cost * (f_percent/100)
        l_row.append(round(f_benefit, 2))


def table_display(p_actions_list: list[list[str]]):
    """
    Affiche un tableau formaté contenant les actions, leurs coûts, bénéfices et profits.

    La fonction utilise la bibliothèque `rich` pour créer une table esthétique et lisible
    dans la console. 
    `p_actions_list` est une liste de listes où :
    - La première ligne contient les en-têtes (noms des colonnes).
    - Chaque ligne suivante contient : nom de l'action (str), coût (str), bénéfice (str), profit (float).

    Paramètres :
    ----------
    p_actions_list : list[list]
        Liste de listes contenant les données des actions à afficher.
        Exemple d'entrée :
        [
            ['Nom', 'Coût', 'Bénéfice', 'Profit'],
            ['Action-1', '100', '10%', 10.0],
            ...
        ]

    Retour :
    -------
    None
        La fonction affiche le tableau dans la console, mais ne retourne rien.
    """
    o_console = Console()

    # Création du tableau
    o_table = Table(title="Liste des actions")

    # Creation des colonnes
    o_table.add_column("Nom de l'action")
    o_table.add_column("Coût (€)")
    o_table.add_column("Bénéfice (%)")
    o_table.add_column("Profit (€)")

    # Creation des lignes
    for l_row in p_actions_list[1:]:
        o_table.add_row(l_row[0], l_row[1], l_row[2], str(l_row[3]))

    # Affichage du tableau
    o_console.print(o_table)


def generate_combinations(p_actions_list: list[list[str]]) -> list[list]:
    """
    Génère toutes les combinaisons possibles d'actions à partir d'une liste donnée.

    La fonction explore récursivement toutes les combinaisons de sous-ensembles
    possibles (panier d'actions) en utilisant un algorithme de type "arbre binaire de décisions".
    Chaque action peut être incluse ou non dans une combinaison donnée.

    Paramètres :
    ----------
    p_actions_list : list
        Liste des actions disponibles. Chaque action peut être représentée
        par une structure (ex. : liste ou tuple contenant le nom, le coût, etc.).

    Retour :
    -------
    list[list]
        Liste de toutes les combinaisons possibles. Chaque combinaison est elle-même
        une liste d'actions.
    """
    # Initialise une liste vide
    # Elle contiendra toutes les combinaisons possibles d'actions
    l_all_combos_list = []
    l_current_combo = []

    # Fonction interne (récursive) qui explore toutes les combinaisons
    # possibles
    # remaining = les actions qu'on n'a pas encore traitées
    # current_combo = la combinaison en cours de construction
    def explore(p_remaining_list, p_current_combo_list):
        # Cas de base : s'il n'y a plus d'actions à traiter
        if not p_remaining_list:
            # Ajoute la combinaison actuelle à la liste des combinaisons
            # finales
            l_all_combos_list.append(p_current_combo_list)
            return

        # Récupère la première action restante
        s_current_action = p_remaining_list[0]

        # Prépare une nouvelle liste avec le reste des actions
        # (sans la première)
        l_rest = p_remaining_list[1:]

        # Continue l'exploration sans ajouter l'action à la combinaison
        # actuelle
        explore(l_rest, p_current_combo_list.copy())

        # Continue l'exploration en ajoutant cette action à la combinaison
        explore(l_rest, p_current_combo_list + [s_current_action])

    # Appel de la fonction pour démarrer la récursivité avec la liste d'action
    # et une liste vide (current_combo)
    explore(p_actions_list, l_current_combo)

    # Retourne la liste finale contenant toutes les combinaisons possibles
    return l_all_combos_list


def calculate_profit_and_costs(p_combinaisons: list[list[list]]) -> list[dict]:
    """
    Calcule le coût total et le bénéfice total pour chaque combinaison d’actions.

    Chaque combinaison est une liste d’actions, où chaque action est une liste contenant :
    - le nom de l'action (str)
    - le coût par action (str convertible en float)
    - le pourcentage de profit (str, déjà transformé en float ailleurs)
    - le profit en euros (float)

    Paramètres
    ----------
    p_combinaisons : list[list[list]]
        Liste contenant toutes les combinaisons possibles d’actions.

    Retour
    ------
    list[dict]
        Une liste de dictionnaires. Chaque dictionnaire contient :
        - "combinaison" : la liste des actions de la combinaison
        - "cout" : le coût total de cette combinaison (float, arrondi à 2 décimales)
        - "profit" : le bénéfice total de cette combinaison (float, arrondi à 2 décimales)
    """
    # Initialisation de la liste a construire
    l_results_dictionary = []

    # 1er niveau de boucle pour initailiser les variables permettant de faire les calculs
    for l_combo in p_combinaisons:
        f_total_cost = 0.0
        f_total_profit = 0.0

        # 2eme niveau de boucle pour faire les calculs
        for l_action in l_combo:
            f_cost = float(l_action[1])
            f_profit = float(l_action[3])
            f_total_cost += f_cost
            f_total_profit += f_profit

        # Construction de la structure de sortie
        l_results_dictionary.append({
            "combinaison": l_combo,
            "cout": round(f_total_cost, 2),
            "profit": round(f_total_profit, 2)
        })

    return l_results_dictionary


def filter_valid_combinations(p_combos_profit_cost_list: list[dict]) -> list[dict]:
    """
    Filtre les combinaisons valides dont le coût total est inférieur ou égal à 500 €.

    Paramètres :
    ------------
    p_combos_profit_cost_list : list[dict]
        Liste de dictionnaires représentant des combinaisons d'actions,
        avec les clés : "combinaison", "cout" et "profit".

    Retour :
    --------
    list[dict]
        Liste filtrée contenant uniquement les combinaisons valides,
        c’est-à-dire celles dont le coût total est ≤ 500 €.
    """
    # Initialisation de la liste des combinaisons valides
    l_valid_combos = []

    # Parcourt chaque combinaison pour vérifier le coût et ajoute la combinaison à la liste des combinaisons valides
    for d_combo in p_combos_profit_cost_list:
        if d_combo["cout"] <= 500:
            l_valid_combos.append(d_combo)

    # Retourne la liste filtrée
    return l_valid_combos


def sort_combos_by_profit(p_valid_combos: list[dict]) -> list[dict]:
    """
    Trie les combinaisons valides par ordre décroissant de profit.

    Paramètres :
    ------------
    p_valid_combos : list[dict]
        Liste de dictionnaires représentant des combinaisons valides d'actions.
        Chaque dictionnaire contient au moins la clé "profit".

    Retour :
    --------
    list[dict]
        Nouvelle liste triée par profit décroissant (du plus rentable au moins rentable).
    """

    l_sorted_combos = sorted(p_valid_combos, key=lambda d_combo: d_combo["profit"], reverse=True)
    # key=lambda d_combo: d_combo["profit"] utilise une fonction lambda
    # pour extraire la valeur associée à la clé "profit" de chaque dictionnaire.
    # Cette valeur est utilisée comme critère de tri.

    # Retourne la liste triée
    return l_sorted_combos


# PROGRAMME PRINCOPAL
s_actions_file = "Liste-actions.csv"

# Chargement des données CSv dans le programme
list_actions = read_csv(s_actions_file)

# Calcule des profits pour chaque action
calculate_profits(list_actions)

# Affichage de la liste des actions 
table_display(list_actions)

# Création des combinaisons d'action possibles
# Le [1:] créé un slice sans l'en-tête sinon l'entete serait considéré comme une ligne lambda*
# Et cela disperserait des chaines de caractères dans pleins de combinaison comme s'il s'agissait d'actions
print("[bold cyan] Génération des combinaisons...")
l_combinaisons = generate_combinations(list_actions[1:])
print("[bold green]✅ Les combinaisons sont créées")
# print(l_combinaisons)

# print(l_combinaisons[15])

# Calcul du cout total et du profit total pour chaque combinaison d'action
print("[bold cyan] Calcul du coût total et du profit total de chaque combinaison...")
l_combos_profit_cost_list = calculate_profit_and_costs(l_combinaisons)
print("[bold green]✅ Les calculs de couts et profits sont établis")
# print(l_combos_profit_cost_list[15])

print("[bold cyan] Filtre des combinaisons coutant + de 500€...")
l_valid_combinaison = filter_valid_combinations(l_combos_profit_cost_list)
print("[bold green]✅ Les combinaisons coutant plus de 500€ sont exclues")

print("[bold cyan] Trie des combinaisons en fonction du meilleur profit...")
l_valid_combinaison_sorted = sort_combos_by_profit(l_valid_combinaison)
print("[bold green]✅ Les combinaisons sont triés de celle qui rapporte le meilleur profit à celle qui rapporte le moins")

print(f"La meilleure combinaison est {l_valid_combinaison_sorted[0]}")
print(l_valid_combinaison_sorted[1])
print(l_valid_combinaison_sorted[2])
print(l_valid_combinaison_sorted[3])
print(l_valid_combinaison_sorted[4])
print(l_valid_combinaison_sorted[5])
