
import csv
import os
from rich.table import Table
from rich.console import Console
from rich import print
import time
from rich.panel import Panel
import math


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

     Retour :
    -------
    list[list]
        Liste contenant toutes les lignes du fichier CSV,
        chaque ligne étant une liste de chaînes représentant les colonnes.
    """
    try:
        if not os.path.exists(p_csv_name):
            raise FileNotFoundError(f"Le fichier {p_csv_name} n'est pas trouvé.")
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


def calculate_profits(p_actions_list: list[list[str]]) -> None:
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


def table_display(p_actions_list: list[list[str]]) -> None:
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


def display_best_combo(p_best_actions_list: dict) -> None:
    """
    Affiche joliment la meilleure combinaison d’actions à acheter,
    en utilisant la bibliothèque `rich`.

    Paramètre :
    -----------
    p_best_actions_list : dict
        Un dictionnaire contenant :
         - "actions" : liste des actions sélectionnées
        - "profit" : profit total
    """
    o_console = Console()

    l_best_combo = p_best_actions_list["actions"]

    # Prépare une liste vide pour mettre les phrases
    l_phrases_actions = []
    cout = 0

    # Fait une boucle pour chaque action
    for action in l_best_combo:
        s_phrase = f" {action['nom']} - pour un coût de : {action['cout']}€ et un bénéfice de : {action['benefice']})"
        l_phrases_actions.append(s_phrase)
        cout += float(action["cout"])

    # Crée une seule chaîne avec toutes les phrases séparées par des retours à la ligne
    s_action_lines = "\n".join(l_phrases_actions)

# Suppresion de l'indentation de {s_action_lines} pour l'affichage sans espace devant chaque option
    o_console.print(Panel.fit(f"""
    [bold yellow]- Coût Total : {cout}  €
    - Profit Total : {p_best_actions_list['profit']:.2f} €[/bold yellow]
    - Les actions à acheter :
{s_action_lines}
    """, title="Meilleure combinaison d'action à acheter", border_style="bright_magenta"))
    o_console.print("")


def transform_to_dict(p_actions_list: list[list]) -> list[dict]:
    """
    Transforme une liste d'actions en une liste de dictionnaires, avec des clés explicites.

    La fonction :
    - Ignore la première ligne de l'entrée (considérée comme l'en-tête),
    - Associe chaque valeur à une clé parmi ["Nom", "cout", "benefice", "profit"],
    - Retourne une liste de dictionnaires représentant chaque action.

    Args:
        p_actions_list (list[list]): Liste contenant toutes les actions.

    Returns:
        list[dict]: Liste de dictionnaires contenant les données des actions avec leurs attributs nommés.
    """

    l_header = ["nom", "cout", "benefice", "profit"]

    # Suppression de la première ligne (l'en-tête initial du fichier), on garde seulement les données
    l_rows = p_actions_list[1:]

    l_actions_dict = []
    for l_action in l_rows:
        d_action = dict(zip(l_header, l_action))
        l_actions_dict.append(d_action)

    return l_actions_dict


def generate_matrix(p_list_actions_dict: list[dict]) -> list[list[dict]]:
    """
    Génère une matrice 2D vide pour initialiser la résolution du problème d'optimisation des actions.

    La fonction crée une matrice :
    - Chaque ligne correspond à une action disponible.
    - Chaque colonne correspond à un budget de 0€ à 500€.
    - Chaque cellule est initialisée avec un dictionnaire {"profit": 0, "actions": []}.

    Args:
        p_list_actions_dict (list[dict]): Liste de dictionnaires représentant les actions disponibles.

    Returns:
        list: Matrice 2D initialisée avec des profits à 0 et des listes d'actions vides.
    """

    l_matrix = []
    i_budget_max = 500

    for i in range(len(p_list_actions_dict)):
        row = []
        for j in range(i_budget_max + 1):  # de 0 à 500 inclus
            row.append({"profit": 0, "actions": []})
        l_matrix.append(row)
    return l_matrix


def fill_matrix(p_list_matrix_init: list[list[dict]], p_list_actions_dict: list[dict]) -> None:
    """
    Remplit une matrice pour trouver les meilleures actions à acheter sans dépasser un budget maximal
    et en maximisant le profit total.

    La fonction construit une matrice 2D :
    - Chaque ligne représente une action disponible.
    - Chaque colonne représente un budget de 0€ à 500€.
    - Chaque cellule contient un dictionnaire {"profit": float, "actions": list[dict]} :
        - "profit" : le meilleur profit réalisable avec ce budget et ces actions.
        - "actions" : la liste des actions choisies pour atteindre ce profit.

    Si le coût d'une action dépasse le budget courant, la cellule copie la valeur de la ligne précédente.
    Sinon, la fonction choisit entre :
        - Prendre l'action actuelle, ajouter son profit au meilleur profit calculé précédemment pour le budget
          disponible après achat, et compléter la liste des actions en conséquence dans la cellule.
        - Ne pas prendre l'action actuelle (et conserver le meilleur profit précédent).

    Args:
        p_list_matrix_init (list): Matrice 2D initialisée, contenant des dictionnaires {"profit": 0, "actions": []}.
        p_list_actions_dict (list[dict]): Liste de dictionnaires contenant les informations des actions,
        avec les clés "cout" et "profit".

    Returns:
        None: La matrice est modifiée directement.
    """
    # paramétrage du budget maximum
    i_budget_max = 500

    # Remplissage d'une matrice qui va contenir 501 colonnes, chacune d'elle représente un budget max

    # Cas particulier pour remplir la première ligne (action) sans la comparer à la ligne précédente dans la matrice
    for column in range(i_budget_max + 1):
        d_action = p_list_actions_dict[0]  # action de l'index 0
        f_cost = float(d_action["cout"])
        f_profit = float(d_action["profit"])

        # Comparaison du coût par rapport à la colonne (index de la colonne représente le coût)
        if f_cost <= column:
            # Création du dictionnaire comportant le profit "total" et la liste de dictionnaire d'actions
            p_list_matrix_init[0][column] = {
                "profit": f_profit,
                "actions": [d_action]
            }
        else:
            # Remplissage par défaut à 0 et liste d'action à vide
            p_list_matrix_init[0][column] = {
                "profit": 0.0,
                "actions": []
            }

    # Remplissage de la matrice à partir de la 2eme ligne (action) avec comparaison de la ligne précédente
    for row in range(1, len(p_list_matrix_init)):  # Première boucle, l'action en cours (ligne)
        for column in range(i_budget_max + 1):  # Deuxième boucle imbriquée, le budget en cours (colonne)
            # ici accès à la cellule correspondant au budget courant
            d_action = p_list_actions_dict[row]
            f_cost = math.ceil(float(d_action["cout"]))
            f_profit = float(d_action["profit"])

            # Cas où le coût de l'action est supérieur à la colonne (budget )
            if f_cost > column:
                # Pas assez d'argent → report du contenu de la cellule de la ligne précédente, même colonne
                p_list_matrix_init[row][column] = p_list_matrix_init[row-1][column]
                # [row][column] correspond aux coordonnées de la cellule
            else:
                # Cas où le coût de l'action est inférieure ou égal à la colonne budget

                # Variable représentant le buget restant, donc là où on va regarder pour récupérer les données et les
                # ajouter à l'action courante
                i_remaining_budget_column = column - int(f_cost)

                # Profit total si on inclut l'action courante
                f_total_profit = f_profit + p_list_matrix_init[row-1][i_remaining_budget_column]["profit"]

                # Profit si sans l'action courante càd recopiage des données de la cellule de la ligne précédente,
                # même colonne
                f_profit_without_current_action = p_list_matrix_init[row-1][column]["profit"]

                # Comparaison entre les deux profits, on garde le plus gros profit
                if f_total_profit > f_profit_without_current_action:
                    # A la cellule courante on prend le profit total et on ajoute dans la liste de dictionnaire,
                    # l'action courante
                    p_list_matrix_init[row][column] = {
                        "profit": f_total_profit,
                        "actions": p_list_matrix_init[row-1][i_remaining_budget_column]["actions"] + [d_action]
                    }
                else:
                    # Si le profit sans l'action courante est meilleur, on recopie la cellule précédente, même colonne
                    p_list_matrix_init[row][column] = p_list_matrix_init[row-1][column]


def filter_actions(p_actions_list: list[list]) -> list[list]:
    """
    Filtre les actions en supprimant celles dont le prix ou le profit est nul ou négatif.

    Paramètres :
    -----------
    p_actions_list : List[List]
        Liste contenant toutes les actions, y compris l'en-tête.
        Chaque ligne représente une action : [nom, prix (str), profit (str)].

    Retour :
    -------
    List[List]
        Liste des actions valides : celles avec un prix > 0 et un profit > 0.
        L'en-tête n'est pas inclus dans la liste retournée.
    """
    l_filtered_actions = []
    for action in p_actions_list[1:]:
        price = float(action[1])
        profit = float(action[2])
        if price > 0 and profit > 0:
            l_filtered_actions.append(action)
    return l_filtered_actions


# PROGRAMME PRINCIPAL

# Travail sur le fichier avec 20 actions

# mesure du temps d'exécution
start_time = time.time()

o_console = Console()

o_console.print("")
o_console.print("")

o_console.rule("[bold cyan]Travail sur la liste de 20 actions[/bold cyan]", style="cyan")

s_actions_file = "Liste-actions.csv"

# Chargement des données CSV dans le programme
list_actions = read_csv(s_actions_file)

# Vérifie si le fichier est vide ou incorrect, si c'est le cas, ça stoppe l'exécution
if not list_actions:
    o_console.print("[bold red]Chargement annulé, le fichier est vide ou incorrect[/bold red]")
    exit()

# Calcule des profits pour chaque action
calculate_profits(list_actions)

# Affichage de la liste des actions
table_display(list_actions)

# Transformation de la liste des actions en liste de dictionnaire d'actions
l_dict_actions = transform_to_dict(list_actions)

# Génération de la matrice avec une valeur par défaut
l_matrix_init = generate_matrix(l_dict_actions)

# Remplissage de la matrice avec les calculs pour chaque action
fill_matrix(l_matrix_init, l_dict_actions)

# Isoler la meilleure combinaison d'actions
l_dict_final_row = l_matrix_init[-1]
best_actions_list = l_dict_final_row[500]

display_best_combo(best_actions_list)

end_time = time.time()

print(f"⏱️ Temps d'exécution de optimized avec 20 actions : {end_time - start_time:.2f} secondes")

# -----------------------------------------------------------------------------------------------------

# Travail sur le Dataset 1
# mesure du temps d'exécution
start_time = time.time()

o_console = Console()

o_console.print("")
o_console.print("")

o_console.rule("[bold cyan]Travail sur dataset - 1[/bold cyan]", style="cyan")

# Chargement des données CSV dans le programme
list_actions = read_csv("dataset1.csv")


# Vérifie si le fichier est vide ou incorrect, si c'est le cas, ça stoppe l'exécution
if not list_actions:
    o_console.print("[bold red]Chargement annulé, le fichier est vide ou incorrect[/bold red]")
    exit()


l_filtered_actions = filter_actions(list_actions)

# Calcule des profits pour chaque action
calculate_profits(l_filtered_actions)

# # Affichage de la liste des actions
# table_display(l_filtered_actions)

# Transformation de la liste des actions en liste de dictionnaire d'actions
l_dict_actions = transform_to_dict(l_filtered_actions)

# Génération de la matrice avec une valeur par défaut
l_matrix_init = generate_matrix(l_dict_actions)

# Remplissage de la matrice avec les calculs pour chaque action
fill_matrix(l_matrix_init, l_dict_actions)

# Isoler la meilleure combinaison d'actions
l_dict_final_row = l_matrix_init[-1]
best_actions_list = l_dict_final_row[500]

display_best_combo(best_actions_list)

end_time = time.time()

print(f"⏱️ Temps d'exécution de optimized pour dataset 1 : {end_time - start_time:.2f} secondes")

# -----------------------------------------------------------------------------------------------------

# Travail sur le Dataset 2
# mesure du temps d'exécution
start_time = time.time()

o_console = Console()

o_console.print("")
o_console.print("")

o_console.rule("[bold cyan]Travail sur dataset - 2[/bold cyan]", style="cyan")

# Chargement des données CSV dans le programme
list_actions = read_csv("dataset2.csv")


# Vérifie si le fichier est vide ou incorrect, si c'est le cas, ça stoppe l'exécution
if not list_actions:
    o_console.print("[bold red]Chargement annulé, le fichier est vide ou incorrect[/bold red]")
    exit()

l_filtered_actions = filter_actions(list_actions)

# Calcule des profits pour chaque action
calculate_profits(l_filtered_actions)

# # Affichage de la liste des actions
# table_display(l_filtered_actions)

# Transformation de la liste des actions en liste de dictionnaire d'actions
l_dict_actions = transform_to_dict(l_filtered_actions)

# Génération de la matrice avec une valeur par défaut
l_matrix_init = generate_matrix(l_dict_actions)

# Remplissage de la matrice avec les calculs pour chaque action
fill_matrix(l_matrix_init, l_dict_actions)

# Isoler la meilleure combinaison d'actions
l_dict_final_row = l_matrix_init[-1]
best_actions_list = l_dict_final_row[500]

display_best_combo(best_actions_list)

end_time = time.time()

print(f"⏱️ Temps d'exécution de optimized pour dataset 2 : {end_time - start_time:.2f} secondes")
