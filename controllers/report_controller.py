from datetime import date
from jinja2 import Environment, FileSystemLoader
from exceptions import exceptions


class ReportController:
    def write_report(self, output_filename, mode, content):
        """
        Description:
        Sert à écrire dans un fichier un contenu
        Paramètres:
        - output_filename: nom du fichier où écrire
        - mode: w pour remplacer ou a pour ajouter
        - content: contenu à écrire
        """
        with open(output_filename, mode, encoding="utf-8") as fd:
            fd.write(f"{content}")
        return True

    def make_html_report_players_list(self, environment, report_header, players_sorted_list):
        """
        Description:
        Sert à écrire le rapport au format html de la 'liste de tous les joueurs par ordre alphabétique'.
        Paramètres:
        - environment: dossier où se trouve le template ou fichier à atteindre.
        - report_header: intitulé du rapport
        - players_sorted_list: liste des joueurs classés par ordre alpha (sur la base du fullname)
        """
        today = date.today()
        template = environment.get_template("index.j2")
        output_filename = f"./reports/players/sorted_players_list_report_{today}.html"
        content = template.render(report_name=report_header, players_list=players_sorted_list)
        self.write_report(output_filename, "w", content)

    def make_text_report_players_list(self, environment, report_header, players_sorted_list):
        """
        Description:
        Sert à écrire le rapport au format txt de la 'liste de tous les joueurs par ordre alphabétique'.
        Paramètres:
        - environment: dossier où se trouve le template ou fichier à atteindre.
        - report_header: intitulé du rapport
        - players_sorted_list: liste des joueurs classés par ordre alpha (sur la base du fullname)
        """
        today = date.today()
        template = environment.get_template("report.j2")
        output_filename = f"./reports/players/sorted_players_list_report_{today}.txt"
        content = ""
        content = template.render(players_list=players_sorted_list)
        self.write_report(output_filename, "w", report_header)
        self.write_report(output_filename, "a", content)

    def get_sorted_players_list(self, view_on_player, output_type="text"):
        """
        Description:
        Sert à présenter une liste des joueurs triée par ordre alphabétique.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - output_type: format de la sortie. En txt par défaut.
        """
        players = view_on_player.get_players_list()
        players_sorted_list = []
        players_sorted_list = sorted(players, key=lambda x: x.fullname)
        environment = Environment(loader=FileSystemLoader("./templates/players"))
        report_header = 'nom rapport: liste de tous les joueurs par ordre alphabétique\n'
        if output_type == "text":
            report_header += f'nombre de joueurs (actifs, inactifs, archivés): {len(players_sorted_list)}'
            self.make_text_report_players_list(environment, report_header, players_sorted_list)
        elif output_type == "html":
            self.make_html_report_players_list(environment, report_header, players_sorted_list)
        return True

    def make_html_report_tournaments_list(
            self,
            environment,
            report_header,
            tournaments_list,
            element_to_list="tournoi",
            filename=""):
        """
        Description:
        Sert à écrire le rapport au format html de la 'liste de tous les tournois'.
        Paramètres:
        - environment: dossier où se trouve le template ou fichier à atteindre.
        - report_header: intitulé du rapport
        - tournaments_list: liste des tournois
        - element_to_list: libellé qui indique s'il s'agit de tournoi, joueur ou round.
        """
        today = date.today()
        template = environment.get_template("index.j2")
        if filename == "":
            output_filename = f"./reports/tournaments/tournaments_list_report_{today}.html"
        else:
            output_filename = filename
        content = template.render(
            element_to_list=element_to_list,
            report_name=report_header,
            tournaments_list=tournaments_list)
        self.write_report(output_filename, "w", content)

    def make_text_report_tournaments_list(self, environment, report_header, tournaments_list, filename=""):
        """
        Description:
        Sert à écrire au format txt de la 'liste de tous les tournois'.
        Paramètres:
        - environment: dossier où se trouve le template ou fichier à atteindre.
        - report_header: intitulé du rapport
        - tournaments_list: liste des tournois
        - filename: permet de préciser le fichier de sortie.
        """
        today = date.today()
        template = environment.get_template("report.j2")
        if filename == "":
            output_filename = f"./reports/tournaments/tournaments_list_report_{today}.txt"
        else:
            output_filename = filename
        content = template.render(tournaments_list=tournaments_list)
        self.write_report(output_filename, "w", report_header)
        self.write_report(output_filename, "a", content)

    def get_tournaments_list(self, view_on_tournament, output_type="text"):
        """
        Description:
        Sert à présenter la liste de tous les tournois
        Paramètres:
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        - output_type: format de la sortie. En txt par défaut.
        """
        tournaments_list = []
        temp_tournaments_list = view_on_tournament.get_tournaments_list()
        environment = Environment(loader=FileSystemLoader("./templates/tournaments"))
        report_header = 'nom rapport: liste de tous les tournois\n'
        for tournament in temp_tournaments_list:
            tournaments_list.append(tournament.get_content())
        if output_type == "text":
            report_header += f'nombre de tournois: {len(tournaments_list)}\n'
            self.make_text_report_tournaments_list(environment, report_header, tournaments_list)
        elif output_type == "html":
            self.make_html_report_tournaments_list(environment, report_header, tournaments_list)
        return True

    def get_tournament_name_and_dates(self, view_on_tournament, tournament, output_type="text"):
        """
        Description:
        Sert à présenter la liste de tous les tournois avec noms et dates.
        Paramètres:
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        - tournament: une instance de la classe Tournament
        - output_type: format de la sortie. En txt par défaut.
        """
        filtered_tournament = {}
        today = date.today()
        environment = Environment(loader=FileSystemLoader("./templates/tournaments"))
        report_header = 'nom rapport: nom et dates d’un tournoi donné'
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()

        for key in tournament.get_content():
            if key in ["name", "start_date", "end_date"]:
                filtered_tournament[key] = tournament.get_content()[key]
        if output_type == "text":
            filename = f"./reports/tournaments/tournament_by_name_and_date_report_{today}.txt"
            self.make_text_report_tournaments_list(environment, report_header, [filtered_tournament], filename)
        elif output_type == "html":
            filename = f"./reports/tournaments/tournament_by_name_and_date_report_{today}.html"
            element_to_list = 'tournois'
            self.make_html_report_tournaments_list(
                environment,
                report_header,
                [filtered_tournament],
                element_to_list,
                filename)
        return True

    def get_tournament_sorted_players_list(self, view_on_player, view_on_tournament, tournament, output_type):
        """
        Description:
        Sert à écrire au format txt de la 'liste des joueurs du tournoi par ordre alphabétique'.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        - tournament: une instance de la classe Tournament
        - output_type: permet de préciser le fichier de sortie.
        """
        today = date.today()
        environment = Environment(loader=FileSystemLoader("./templates/tournaments"))
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()
        players_list = []
        tournament_id = tournament.tournament_id
        report_header = f"nom rapport: liste des joueurs du tournoi {tournament_id} par ordre alphabétique\n"
        for ine in tournament.players_list:
            player_dict = {}
            player = view_on_player.get_player(ine)
            for key in player.get_content().keys():
                if key in ["f_name", "l_name", "fullname", "ine"]:
                    player_dict[key] = player.get_content()[key]
            last_round_played = ""
            player_points = ""
            if tournament.status == "ended":
                last_round_played = tournament.nb_rounds
            elif tournament.status == "in progress":
                last_round_played = tournament.current_round_id - 1
            player_points = view_on_tournament.get_player_attribute_from_round(
                tournament_id,
                ine,
                'points',
                last_round_played)
            player_dict["points"] = player_points
            players_list.append(player_dict)
        sorted_players_list = sorted(players_list, key=lambda x: x["fullname"])
        if output_type == "text":
            report_header += f'nombre de joueurs du tournoi: {len(sorted_players_list)}\n'
            filename = f"./reports/tournaments/tournament_players_sorted_list_report_{today}.txt"
            self.make_text_report_tournaments_list(environment, report_header, sorted_players_list, filename)
        elif output_type == "html":
            filename = f"./reports/tournaments/tournament_players_sorted_list_report_{today}.html"
            element_to_list = 'joueurs'
            self.make_html_report_tournaments_list(
                environment,
                report_header,
                sorted_players_list,
                element_to_list,
                filename)
        return True

    def get_tournament_rounds_and_matches(self, view_on_tournament, tournament, output_type):
        """
        Description:
        Sert à écrire au format txt de la 'liste de tous les tours du tournoi et de tous les matchs du tour.
        Paramètres:
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        - tournament: une instance de la classe Tournament
        - output_type: permet de préciser le fichier de sortie.
        """
        filtered_tournament = {}
        today = date.today()
        environment = Environment(loader=FileSystemLoader("./templates/tournaments"))
        tournament_id = tournament.tournament_id
        report_header = f"nom rapport: liste de tous les tours du tournoi {tournament_id} avec les matchs\n"
        for key in tournament.get_content():
            if key in ["name", "rounds_list", "tournament_id"]:
                filtered_tournament[key] = tournament.get_content()[key]
        if output_type == "text":
            report_header += f'nombre de rounds du tournoi: {len(filtered_tournament["rounds_list"])}\n'
            filename = f"./reports/tournaments/tournament_rounds_and_matches_report_{today}.txt"
            self.make_text_report_tournaments_list(environment, report_header, [filtered_tournament], filename)
        elif output_type == "html":
            filename = f"./reports/tournaments/tournament_rounds_and_matches_report_{today}.html"
            element_to_list = 'rounds'
            self.make_html_report_tournaments_list(
                environment,
                report_header,
                [filtered_tournament],
                element_to_list,
                filename)
        return True
