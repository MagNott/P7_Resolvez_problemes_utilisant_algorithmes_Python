import csv
import os
from rich.table import Table
from rich.console import Console


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


# PROGRAMME PRINCOPAL
actions_file = "Liste-actions.csv"

list_actions = read_csv(actions_file)
profit_calculation(list_actions)
table_display(list_actions)
