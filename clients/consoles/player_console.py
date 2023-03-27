import pyfiglet
from models import player_model
from .console_shared import print_message, set_a_date
from exceptions import exceptions


def get_players_by_club_console(view, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    club_id = input(f"{print_message(message='club id: ')}")
    attribute = input(f"{print_message(message='attribut spécifique: ')}")
    if not view.view_on_club.view_club(club_id):
        raise exceptions.ClubIdDoesNotExistsException()
    return view.view_on_player.view_players_by_club_list(club_id, attribute)


def update_player_console(view, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    player_ine = input(f"{print_message(message='player ine: ')}")
    if not view.view_on_player.view_player(player_ine):
        raise exceptions.IneDoesNotExistsException()
    attribute = input("attribute: ")
    if attribute == "":
        raise exceptions.BlankFieldException()
    elif attribute == "id":
        return False

    if attribute == "status":
        value = input("nouvelle valeur (active, inactive, archived): ")
        return view.view_on_player.update_player_status(player_ine, value)
    else:
        value = input("nouvelle valeur: ")
    if value == "":
        raise exceptions.BlankFieldException()
    return view.view_on_player.update_player(player_ine, attribute, value)


def get_player_console(view):
    player_dict = {
        "civility": "",
        "f_name": "",
        "l_name": "",
        "birth_date": "",
        "ine": "",
        "licence": "",
        "subscribe_date": "",
    }

    club_id_input = input("club_id: ")
    if not view.view_on_club.view_club(club_id_input):
        raise exceptions.ClubIdDoesNotExistsException()
    for key in player_dict.keys():
        if "date" in key:
            print(print_message(message=f'[{key}]'))
            try:
                answer = set_a_date()
            except ValueError:
                raise exceptions.NotDigitException()
        elif "ine" in key:
            answer = input(f"{key}: ")
            view.view_on_player.verify_ine_input(answer)
        elif "licence" in key:
            answer = input(f"{key} (A ou B), A par défaut: ")
            answer = answer.lower()
        else:
            answer = input(f"{key}: ")
        player_dict[key] = answer
    player = player_model.Player(
        club_id=club_id_input,
        civility=player_dict["civility"],
        f_name=player_dict["f_name"],
        l_name=player_dict["l_name"],
        birth_date=player_dict["birth_date"],
        ine=player_dict["ine"],
        licence=player_dict["licence"],
        category=view.view_on_player.find_player_category(player_dict["birth_date"]),
        subscribe_date=player_dict["subscribe_date"],
    )
    vcc = view.view_on_player.create_player(player)
    if vcc:
        print_message(message='création joueur réussie', type='success')
