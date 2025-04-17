import csv
import os
from rich.table import Table
from rich.console import Console


# FONCTIONS
def read_csv(p_csv_name):
    if not os.path.exists(p_csv_name):
        print(f"Le fichier {p_csv_name} n'est pas trouvé")
    else:
        work_file = []
        with open(p_csv_name, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                work_file.append(row)

    return work_file


def profit_calculation(p_actions_list):
    p_actions_list[0].append("Profit (€)")
    for row in p_actions_list[1:]:
        print(row, type(row))
        cost = float(row[1])
        percent = float(row[2].replace("%", ""))
        benefit = cost * (percent/100)
        row.append(round(benefit, 2))
    print(p_actions_list)


def table_display(p_actions_list):
    console = Console()

    # Création du tableau
    table = Table(title="Liste des actions")

    # Creation des colonnes
    table.add_column("Nom de l'action")
    table.add_column("Coût (€)")
    table.add_column("Bénéfice (%)")
    table.add_column("Profit (€)")

    # Creation des lignes
    for row in p_actions_list[1:]:
        table.add_row(row[0], row[1], row[2], str(row[3]))

    # Affichage du tableau
    console.print(table)


def generate_combinations(p_actions_list):
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
actions_file = "Liste-actions.csv"

list_actions = read_csv(actions_file)
profit_calculation(list_actions)
table_display(list_actions)
combinaisons = generate_combinations(list_actions)
# print(combinaisons)
