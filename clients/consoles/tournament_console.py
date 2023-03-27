import pyfiglet
from models import tournament_model
from .console_shared import print_message, set_a_date
from exceptions import exceptions


def update_tournament_console(view, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    tournament_id = input(f"{print_message(message='tournament id: ')}")
    if not view.view_on_tournament.view_tournament(tournament_id):
        raise exceptions.TournamentIdDoesNotExistsException()
    attribute = input("attribute: ")
    if attribute == "":
        raise exceptions.BlankFieldException()
    elif attribute == "id":
        return False

    if attribute == "status":
        value = input("nouvelle valeur (in progress, cancelled, paused, ended): ")
        return view.view_on_tournament.update_tournament_status(tournament_id, value)
    else:
        value = input("nouvelle valeur: ")
    if value == "":
        raise exceptions.BlankFieldException()
    return view.view_on_tournament.update_tournament_database(tournament_id, attribute, value)


def add_a_new_existing_player(view, tournament):
    print_message(message='AJOUTER UN NOUVEAU JOUEUR')
    ine = input(f"{print_message(message='ine: ')}")
    if ine == "":
        raise exceptions.BlankFieldException()
    try:
        view.view_on_tournament.add_a_new_existing_player(ine, tournament)
    except exceptions.PlayerStatusNotActiveException:
        print_message(message='JOUEUR INACTIF', type='error')
        return False
    return True


def delete_player_from_list(view, tournament):
    print_message(message='SUPPRIMER UN JOUEUR PREINSCRIT')
    ine = input(f"{print_message(message='ine: ')}")
    if ine == "":
        raise exceptions.BlankFieldException()
    view.view_on_tournament.delete_player_from_list(ine, tournament)
    return True


def update_odd_players_list(view, tournament):
    print_message(message='NOMBRE IMPAIR DE JOUEURS', type='error')
    odd_tournament_players_list_menu = [
        ("0", "ANNULER TOURNOI"),
        ("1", "AJOUTER JOUEUR"),
        ("2", "RETIRER JOUEUR"),
    ]
    for item in odd_tournament_players_list_menu:
        print(f"{item[0]}: {item[1]}")
    answer = input("choix : ")

    if answer == "":
        raise exceptions.BlankFieldException()
    elif answer == "1":
        add_a_new_existing_player(view, tournament)
        create_tournament(view, tournament)
    elif answer == "2":
        delete_player_from_list(view, tournament)
        create_tournament(view, tournament)
    else:
        raise exceptions.TournamentCancelledException()


def get_tournament_console(view):
    tournament_dict = {
        "tournament_id": "",
        "name": "",
        "location": "",
        "start_date": "",
        "end_date": "",
        "nb_rounds": "",
        "description": "",
    }
    if len(view.view_on_club.view_clubs()) == 0:
        raise exceptions.NoClubsRecordedException()
    elif len(view.view_on_player.view_players()) == 0:
        raise exceptions.NoPlayersRecordedException()

    tournament_id_input = input("tournament_id: ")

    try:
        view.view_on_tournament.view_tournament_by_id(tournament_id_input)
        raise exceptions.TournamentIdAlreadyExistsException()
    except exceptions.TournamentIdDoesNotExistsException:
        pass

    answer = ""
    for key in tournament_dict.keys():
        if "date" in key:
            print(print_message(message=f'[{key}]'))
            answer = set_a_date()
        elif "id" in key:
            print(print_message(message=f'[{key}]'))
        elif "nb_rounds" in key:
            try:
                answer = int(input(f"{key}: "))
            except ValueError:
                raise exceptions.TournamentNbRoundNotDigit()
        else:
            answer = input(f"{key}: ")
            if answer == "" and "description" not in key:
                raise exceptions.BlankFieldException()
        tournament_dict[key] = answer
    tournament = tournament_model.Tournament(
        tournament_id=tournament_id_input,
        name=tournament_dict["name"],
        location=tournament_dict["location"],
        start_date=tournament_dict["start_date"],
        end_date=tournament_dict["end_date"],
        nb_rounds=tournament_dict["nb_rounds"],
        description=tournament_dict["description"],
    )
    create_tournament(view, tournament)


def create_tournament(view, tournament):
    try:
        vcc = view.view_on_tournament.create_tournament(tournament)
        if vcc:
            print_message(message='mise à jour de la liste des joueurs du tournoi réussie')
            print_message(message='création tournoi réussie', type='success')
    except exceptions.OddPlayersListNumberException:
        update_odd_players_list(view, tournament)
