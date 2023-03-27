import pyfiglet
import sys
import view
from .consoles import club_console, console_menus, player_console, round_console, tournament_console
from .consoles.console_shared import print_message
from exceptions import exceptions

BANNEER = pyfiglet.figlet_format("OPEN CLASS ROOM CHESS")


class Console:
    def __init__(self, view):
        self.view = view
        self.menu = console_menus.ConsoleMenu()

    def get_quit_menu(self, name_menu, front_caption="", back_caption=""):
        figlet_appearance = pyfiglet.figlet_format(f"{back_caption} ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu("quit_menu")
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "0":
            self.get_root_menu()

    def get_root_menu(self):
        print(print_message(message=f'{BANNEER}'))
        self.menu.display_menu("root_menu")
        answer = input(f"{print_message(message='choix: ')}")
        if answer in ["1", "2", "3"]:
            self.get_cruda_menu(
                "cruda_menu",
                self.menu.get_caption(answer),
                self.menu.get_caption(answer, caption_type="computer"),
            )
        elif answer == "4":
            self.get_report_menu("report_menu", "REPORT", "REPORT")
        else:
            self.get_quit_menu("quit", "QUIT", "QUIT")
            print_message(message="FIN DE L'APPLICATION", type="success")
            sys.exit(0)

    def get_cruda_menu(self, name_menu, front_caption="", back_caption=""):
        figlet_appearance = pyfiglet.figlet_format(f"{back_caption.upper()} ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu(name_menu)
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            print(f"VOIR {front_caption}")
            self.get_one_or_many_menu_get(name_menu, back_caption)
        elif answer == "2":
            print(f"CREER {front_caption}")
            if back_caption == "club":
                club_console.get_console_console(view)
            elif back_caption == "tournament":
                tournament_console.get_tournament_console(view)
            else:
                eval(f"{back_caption.lower()}_console.get_{back_caption.lower()}_console(view)")
        elif answer == "3":
            print(f"SUPPRIMER {front_caption}")
            if front_caption == "CLUB":
                (front_caption, back_caption) = ["club"] * 2
            elif front_caption == "JOUEUR":
                (front_caption, back_caption) = ["player", "joueur"]
            elif front_caption == "TOURNOI":
                (front_caption, back_caption) = ["tournament", "tournoi"]
            self.get_one_or_many_menu_delete(name_menu, front_caption, back_caption)
        elif answer == "4":
            print(f"MODIFIER {front_caption}")
            if "tournoi" in front_caption.lower():
                self.get_update_tournament_menu(front_caption, back_caption)
            else:
                eval(f"{back_caption.lower()}_console.update_{back_caption.lower()}_console(view, front_caption)")
        else:
            self.get_root_menu()

    def get_update_tournament_menu(self, front_caption, back_caption):
        figlet_appearance = pyfiglet.figlet_format("TOURNAMENT ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu("update_tournament_menu")
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            tournament_console.update_tournament_console(view, front_caption)
        elif answer == "2":
            print_message(message='ACTUALISER TOURS/MATCHS', type='explore')
            tournament_id = input(f"{print_message(message='tournament id: ')}")
            tournament = view.view_on_tournament.view_tournament(tournament_id)
            if tournament is None:
                raise exceptions.TournamentIdDoesNotExistsException()
            round_console.get_round_menu(view, tournament, "ROUND")
        else:
            self.get_cruda_menu(
                "cruda_menu",
                "TOURNAMENT",
                "TOURNAMENT",
            )

    def get_one_or_many_presentation(self, obj_collection):
        if isinstance(obj_collection, dict):
            for key, value in obj_collection.items():
                print_message(message=f'{key}: ', option='end')
                print_message(message=f'{value}', type='explore')
            print("")
        elif isinstance(obj_collection, list):
            for obj in obj_collection:
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        print_message(message=f'{key}: ', option='end')
                        print_message(message=f'{value}', type='explore')
                    print("")
                else:
                    for key, value in obj.get_content().items():
                        print_message(message=f'{key}: ', option='end')
                        print_message(message=f'{value}', type='explore')
                    print("")
        elif len(obj_collection.get_content()) > 0:
            for key, value in obj_collection.get_content().items():
                print_message(message=f'{key}: ', option='end')
                print_message(message=f'{value}', type='explore')
            print("")

    def get_one_or_many_menu_get(self, name_menu, front_caption="", back_caption=""):
        figlet_appearance = pyfiglet.figlet_format(f"{front_caption.upper()} ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        if "player" in front_caption.lower():
            self.menu.display_menu("one_or_many_player_menu_get")
        else:
            self.menu.display_menu("one_or_many_menu_get")
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            print_message(message=f'{front_caption}', type='explore')
            an_id_input = input(f"{print_message(message='identifiant: ')}")
            attribute = input(f"{print_message(message='attribut spécifique: ')}")
            answer_dict = eval(
                f"view.view_on_{front_caption.lower()}.view_{front_caption.lower()}(an_id_input, attribute)")
            self.get_one_or_many_presentation(answer_dict)
        elif answer == "2":
            print_message(message=f'{front_caption}S', type='explore')
            attribute = input(f"{print_message(message='attribut spécifique: ')}")
            answers_list = eval(f"view.view_on_{front_caption.lower()}.view_{front_caption.lower()}s(attribute)")
            for answer_dict in answers_list:
                self.get_one_or_many_presentation([answer_dict])
        elif answer == "3" and "player" in front_caption.lower():
            players_list = player_console.get_players_by_club_console(view, front_caption)
            for player in players_list:
                for key, value in player.items():
                    print_message(message=f'{key}: ', option='end')
                    print_message(message=f'{value}', type='explore')
                print("")
        else:
            self.get_cruda_menu(
                "cruda_menu",
                front_caption,
                front_caption,
            )

    def get_one_or_many_menu_delete(self, name_menu, front_caption="", back_caption=""):
        figlet_appearance = pyfiglet.figlet_format(f"{front_caption.upper()} ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu("one_or_many_menu_delete")
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            print_message(message=f'{front_caption}', type='explore')
            an_identifiant_input = input(f"{print_message(message='identifiant: ')}")
            eval(f"view.view_on_{front_caption.lower()}.delete_{front_caption.lower()}(an_identifiant_input)")
            return True
        elif answer == "2":
            print_message(message=f'{front_caption}S', type='explore')
            answer = input(
                print_message(message=f"confirmer suppression de tous les {back_caption.lower()}s (o/n) ? "))
            if answer == "o" or answer == "oui":
                if "player" in front_caption.lower():
                    self.view.view_on_player.delete_players()
                elif "club" in front_caption.lower():
                    self.view.view_on_club.delete_clubs()
                elif "tournament" in front_caption.lower():
                    self.view.view_on_tournament.delete_tournaments()
                return True
        else:
            self.get_cruda_menu(
                "cruda_menu",
                front_caption,
                front_caption,
            )

    def get_output_format_menu(self, report_number):
        figlet_appearance = pyfiglet.figlet_format("REPORT ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu("report_output_format")
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            if report_number == "1":
                view.view_on_report.get_sorted_players_list()
            elif report_number == "2":
                view.view_on_report.get_tournaments_list()
            elif report_number == "3":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_name_and_dates(tournament)
            elif report_number == "4":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_sorted_players_list(tournament)
            elif report_number == "5":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_rounds_and_matches(tournament)
            print_message(message='édition rapport format .txt réussie', type='success')
        elif answer == "2":
            if report_number == "1":
                view.view_on_report.get_sorted_players_list(output_type="html")
            elif report_number == "2":
                view.view_on_report.get_tournaments_list(output_type="html")
            elif report_number == "3":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_name_and_dates(tournament, output_type="html")
            elif report_number == "4":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_sorted_players_list(tournament, output_type="html")
            elif report_number == "5":
                tournament_id = input(f"{print_message(message='id tournoi: ')}")
                tournament = view.view_on_tournament.view_tournament(tournament_id)
                view.view_on_report.get_tournament_rounds_and_matches(tournament, output_type="html")
            print_message(message='édition rapport format .html réussie', type='success')
        else:
            self.get_report_menu(
                "report_menu",
                "REPORT",
                "REPORT",
            )

    def get_report_menu(self, name_menu, front_caption="", back_caption=""):
        figlet_appearance = pyfiglet.figlet_format(f"{back_caption.upper()} ROOM")
        print(print_message(message=f'{figlet_appearance}'))
        self.menu.display_menu(name_menu)
        answer = input(f"{print_message(message='choix: ')}")
        if answer == "1":
            self.get_output_format_menu("1")
        elif answer == "2":
            self.get_output_format_menu("2")
        elif answer == "3":
            self.get_output_format_menu("3")
        elif answer == "4":
            self.get_output_format_menu("4")
        elif answer == "5":
            self.get_output_format_menu("5")
        else:
            self.get_root_menu()
