import csv
import os
from rich.table import Table
from rich.console import Console


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


# PROGRAMME PRINCOPAL
s_actions_file = "Liste-actions.csv"

list_actions = read_csv(s_actions_file)
calculate_profits(list_actions)
table_display(list_actions)
combinaisons = generate_combinations(list_actions)
# print(combinaisons)
