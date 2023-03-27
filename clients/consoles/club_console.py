import pyfiglet
from models import club_model
from .console_shared import print_message
from exceptions import exceptions


def update_club_console(view, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    club_id = input(f"{print_message(message='club id: ')}")
    if not view.view_on_club.view_club(club_id):
        raise exceptions.ClubIdDoesNotExistsException()
    attribute = input("attribute: ")
    if attribute == "":
        raise exceptions.BlankFieldException()
    elif attribute == "id":
        return False

    if attribute == "status":
        value = input("nouvelle valeur (active, inactive, archived): ")
        return view.view_on_club.update_club_status(club_id, value)
    else:
        value = input("nouvelle valeur: ")
    if value == "":
        raise exceptions.BlankFieldException()
    view.view_on_club.update_club(club_id, attribute, value)


def get_club_console(view):
    club_dict = {
        "club_id": "",
        "name": "",
        "email": "",
        "website": "",
    }
    club_id_input = input("club_id: ")
    if club_id_input == "":
        raise exceptions.BlankFieldException()
    try:
        view.view_on_club.view_club(club_id_input)
    except exceptions.ClubIdDoesNotExistsException:
        pass

    for key in club_dict.keys():
        if key == "club_id":
            continue
        answer = input(f"{key}: ")
        if answer == "":
            raise exceptions.BlankFieldException()
        club_dict[key] = answer
    club = club_model.Club(
        club_id=club_id_input,
        name=club_dict["name"],
        email=club_dict["email"],
        website=club_dict["website"],
    )
    vcc = view.view_on_club.create_club(club)
    if vcc:
        print_message(message='création club réussie', type='success')
