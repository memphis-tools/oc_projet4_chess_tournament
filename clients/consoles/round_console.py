import json
import pyfiglet
from exceptions import exceptions
from . import console_menus
from clients import console
from .console_shared import print_message
from models import match_model, round_model
from datetime import datetime


def get_static_vars():
    """
    Description:
    Sert à charger un fichier format JSON "./vars/vars.json" à la racine du projet.
    Celui-ci indique si le mode debug est ou non activé.
    """
    static_vars_file = "./vars/vars.json"
    static_vars = ""
    with open(static_vars_file, "r") as fd:
        static_vars = json.loads(fd.read())
    return static_vars["data"][0]


def get_round_menu(view, tournament, front_caption="ROUND"):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    if tournament.status == "ended":
        raise exceptions.TournamentEndedException()
    print(print_message(f"Saisir scores du round {tournament.current_round_id} ? "))
    console_menus.ConsoleMenu().display_menu("yes_no_menu")
    answer = input(f"{print_message(message='choix: ')}")
    if answer == "1":
        create_round(view, tournament, front_caption="ROUND")
    else:
        console.Console(view).get_root_menu()


def validate_match_scores_input(round_number, match):
    players_ine_list = match_model.Match(match).get_players_ine()
    score_match = input(
        print_message(
            message=f"[ROUND {round_number}] {players_ine_list[0]} VS {players_ine_list[1]} Set score (o/n) ? "))
    if score_match == "o" or score_match == "oui":
        return True
    return False


def validate_round_scores_input(round_number):
    answer = input(print_message(message=f"Valider saisie des scores du round {round_number} (o/oui, n/non) ? "))
    if answer == "o" or answer == "oui":
        return True
    return False


def check_if_all_round_matches_scored(view, tournament, round):
    round_in_progress = tournament.current_round_id
    if view.view_on_round.do_all_round_matches_scored(round.matches_list):
        if validate_round_scores_input(round_in_progress):
            now = datetime.now()
            round.end_date = now.strftime("%Y-%m-%d %H:%M:%S")
            round.status = "ended"
            view.view_on_tournament.update_round_in_tournament_database(tournament, round)


def create_round(view, tournament, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    max_iteration = int(tournament.nb_rounds)
    round_in_progress = tournament.current_round_id
    if round_in_progress <= max_iteration:
        current_round = view.view_on_tournament.get_round_from_tournament(tournament, round_in_progress)

        print_message(message=f"ROUND {round_in_progress}", type='explore')
        if current_round is None:
            round = view.view_on_round.create_new_round(tournament)
            tournament = view.view_on_tournament.update_tournament_rounds_list(tournament.tournament_id, round)
            static_vars = get_static_vars()
            if static_vars['debug'] and tournament.current_match_id == 1:
                sorted_mixed_players_list = view.view_on_round.get_sorted_players_scores_list(tournament)
                get_debug_infos_for_evaluation(
                    sorted_mixed_players_list, round.matches_list, tournament.tournament_id, view.view_on_tournament)
            r = validate_round_score(view, tournament, round, front_caption=front_caption)
        else:
            round = round_model.Round(**current_round)
            round.status = current_round['status']
            round.start_date = current_round['start_date']
            round.matches_list = current_round['matches_list']
            r = validate_round_score(view, tournament, round, front_caption=front_caption)
        round_matches_list = r.get_matches_list()

        check_if_all_round_matches_scored(view, tournament, round)


def validate_round_score(view, tournament, round, front_caption=""):
    figlet_appearance = pyfiglet.figlet_format(f"{front_caption} ROOM")
    print(print_message(message=f'{figlet_appearance}'))
    if isinstance(round, dict):
        round_matches_list = round['matches_list']
    else:
        round_matches_list = round.get_matches_list()
    match_updated = ""
    round_number = tournament.current_round_id
    for match in round_matches_list:
        if not match_model.Match(match).is_match_scored():
            if validate_match_scores_input(round_number, match):
                players_ine_list = match_model.Match(match).get_players_ine()
                p1_ine = players_ine_list[0]
                p2_ine = players_ine_list[1]
                winner_code = input(
                    f"[ROUND {round_number}] {p1_ine} VS {p2_ine} Gagnant (0=match nul, 1=joueur 1, 2=joueur 2) ? ")
                view.view_on_round.set_a_match_score(match, winner_code)
                tournament = view.view_on_round.update_match_scores(tournament)
                view.view_on_tournament.update_tournament_database(
                    tournament.tournament_id, "current_match_id", tournament.current_match_id)
                view.view_on_tournament.update_tournament_database_with_matches_scores(tournament, match)
                round = view.view_on_round.create_new_round(tournament)
                static_vars = get_static_vars()
                if static_vars['debug'] and tournament.current_match_id == 1:
                    sorted_mxd_players_list = view.view_on_round.get_sorted_players_scores_list(tournament)
                    get_debug_infos_for_evaluation(
                        sorted_mxd_players_list, round.matches_list, tournament.tournament_id, view.view_on_tournament)
                view.view_on_tournament.update_tournament_end_date_if_terminated(tournament)
            else:
                raise exceptions.ScoreSetupStoppedException()
    return round


def get_player_info_from_dict(ine, tournament_id, view_on_tournament):
    players_list_dicts = view_on_tournament.get_players_opponents_and_score(tournament_id)
    for player in players_list_dicts:
        if player["ine"] == ine:
            return player
    return False


def get_debug_infos_for_evaluation(
        sorted_mixed_players_list,
        round_matches_list,
        tournament_id,
        view_on_tournament):
    """
    Description:
    Fonction mise en place pour illustrer visuellement le déroulé de la création des matches.
    N'est utilisée que si le mode debug est activé. Voir fonction "get_static_vars".
    Paramètres:
    - sorted_mixed_players_list: une liste de joueurs
    """

    current_match_id = view_on_tournament.get_tournament_match_id(tournament_id)
    print_message(
        message="[DEBUG] on génère une liste de matches sur la base de cette liste", type='debug')

    for player in sorted_mixed_players_list:
        p = get_player_info_from_dict(player['ine'], tournament_id, view_on_tournament)
        # si p est faux alors on est avant intialisation du round, pas de matches créées (pas d'opposants)
        if p:
            p_ine = player['ine']
            p_points = player['points']
            p_opponents = p['opponents_faced']
        else:
            p_ine = player['ine']
            p_points = player['points']
            p_opponents = player['opponents_faced']
        print(f"ine: {p_ine} - points: {p_points} - faced_opponents: {p_opponents}")
    print("")
    for match in round_matches_list:
        m = match_model.Match(match).get_content()
        ine_players_list = match_model.Match(m).get_players_ine()
        p1 = match_model.Match(m).get_player_by_ine(ine_players_list[0])
        p2 = match_model.Match(m).get_player_by_ine(ine_players_list[1])

        print(f"{p1['ine']} - {p1['fullname']} VS {p2['ine']} - {p2['fullname']}")
    print("")
