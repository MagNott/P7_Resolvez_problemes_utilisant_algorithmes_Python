
import csv
import os
from rich.table import Table
from rich.console import Console
from rich import print
# from rich.panel import Panel


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
    try:
        if not os.path.exists(p_csv_name):
            raise FileNotFoundError(f"Le fichier {p_csv_name} n'est pas trouvé.")
            print(f"Le fichier {p_csv_name} n'est pas trouvé")
        else:
            l_work_file = []
            with open(p_csv_name, newline='', encoding='utf-8') as f:
                o_reader = csv.reader(f)
                for l_row in o_reader:
                    if len(l_row) < 3:  # protection minimale
                        raise ValueError("Une ligne du fichier CSV est incomplète.")
                    l_work_file.append(l_row)
        return l_work_file

    except FileNotFoundError as e:
        print(f"[bold red]{e}[/bold red]")
        return []
    except Exception as e:
        print(f"[bold red]Erreur lors de la lecture du CSV : {e}[/bold red]")
        return []


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
    try:
        p_actions_list[0].append("Profit (€)")
        for l_row in p_actions_list[1:]:
            try:
                f_cost = float(l_row[1])
                f_percent = float(l_row[2].replace("%", ""))
                f_benefit = f_cost * (f_percent/100)
                l_row.append(round(f_benefit, 2))
            except ValueError:
                print(f"[bold red]Erreur dans la ligne : {l_row}[/bold red]")
                continue
    except Exception as e:
        print(f"[bold red]Erreur lors du calcul des profits : {e}[/bold red]")


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
    border_style = "blue"

    # Création du tableau
    o_table = Table(title="Liste des actions qui peuvent être achetées", border_style=border_style)

    # Creation des colonnes
    o_table.add_column("Nom de l'action")
    o_table.add_column("Coût (€)")
    o_table.add_column("Bénéfice (%)")
    o_table.add_column("Profit (€)")

    # Creation des lignes
    for l_row in p_actions_list[1:]:
        o_table.add_row(l_row[0], l_row[1], l_row[2], str(l_row[3]))

    # Affichage du tableau
    o_console.print("")
    o_console.print(o_table)
    o_console.print("")


# def display_best_combo(p_list_best_combo: list[dict]):
#     """
#     Affiche joliment la meilleure combinaison d’actions à acheter,
#     en utilisant la bibliothèque `rich`.

#     Paramètre :
#     -----------
#     p_best_combo : dict
#         Un dictionnaire contenant :
#         - "combinaison" : liste des actions sélectionnées
#         - "cout" : coût total
#         - "profit" : profit total
#     """
#     o_console = Console()

#     # Prend la meilleure combinaison
#     l_best_combo = p_list_best_combo[0]["combinaison"]

#     # Prépare une liste vide pour mettre les phrases
#     l_phrases_actions = []

#     # Fait une boucle pour chaque action
#     for action in l_best_combo:
#         # a[0] = nom, a[1] = coût, a[2] = bénéfice
#         s_phrase = f" • {action[0]} - pour un coût de : {action[1]}€ et un bénéfice de : {action[2]})"
#         l_phrases_actions.append(s_phrase)

#     # Crée une seule chaîne avec toutes les phrases séparées par des retours à la ligne
#     s_action_lines = "\n".join(l_phrases_actions)

# # Suppresion de l'indentation pour l'affichage sans espace devant chaque option
#     o_console.print(Panel.fit(f"""
#     [bold yellow]- Coût Total : {l_valid_combinaison_sorted[0]['cout']}  €
#     - Profit Total : {l_valid_combinaison_sorted[0]['profit']} €[/bold yellow]
#     - Les actions à acheter :
# {s_action_lines}
#     """, title="Meilleure combinaison d'action à acheter", border_style="bright_magenta"))
#     o_console.print("")


# PROGRAMME PRINCIPAL
o_console = Console()

s_actions_file = "Liste-actions.csv"

# Chargement des données CSv dans le programme
list_actions = read_csv(s_actions_file)

# Vérifie si le fichier est vide ou incorrect, si c'est le cas, ça stoppe l'execution
if not list_actions:
    o_console.print("[bold red]Chargement annulé, le fichier est vide ou incorrect[/bold red]")
    exit()

# Calcule des profits pour chaque action
calculate_profits(list_actions)

# Affichage de la liste des actions
table_display(list_actions)
