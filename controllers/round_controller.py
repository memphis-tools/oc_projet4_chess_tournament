from typing import List
import random
from datetime import datetime
from models import match_model, player_model, round_model, tournament_model
from exceptions import exceptions


class RoundController:
    def set_a_match_score(self, match: match_model.Match, winner_code):
        """
        Description:
        Sert à affecter les points aux joueurs d'un matche.
        Le gagnant obtient 1 point, le perdant 0.
        0.5 point si matche nul.
        Paramètre:
        - match: une instance de classe Match
        - winner_code: 1 pour le 1er joueur, 2 pour le second, et 0 pour le match nul.
        """
        if winner_code == "":
            raise exceptions.BlankFieldException()
        if not winner_code.isdigit():
            raise exceptions.NotDigitException()
        if int(winner_code) == 0:
            match_model.Match(match).add_player_point(1, 0.5)
            match_model.Match(match).add_player_point(2, 0.5)
        else:
            match_model.Match(match).add_player_point(int(winner_code), 1)
        return match

    def get_tournament_players_list(self, tournament: tournament_model.Tournament):
        """
        Description:
        Permet d'obtenir la liste des joueurs du tournoi, triée ou non.
        Pour le Round 1 la liste va être mélangée.
        Pour les rounds suivants, inutile de mélanger, on utilisera la même "players_list" déclarée dans le tournoi.
        Paramètres:
        - tournament: une instance de classe Tournament
        """
        round_in_progress = tournament.current_round_id
        ine_players_list = ""
        if round_in_progress == 1:
            ine_players_list = self.mix_players_list(tournament.players_list)
        else:
            ine_players_list = tournament.players_list
        return ine_players_list

    def get_tournament_player_score(
            self,
            ine,
            tournament,
            round_in_progress,
            view_on_player,
            view_on_tournament):
        """
        Description:
        Sert à récupérer les points d'un joueur dans un tournoi.
        Paramètres:
        - ine: la référence ine du joueur
        - tournament: une instance de classe Tournament
        - round_in_progress: numéro de round
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/view_on_tournament_view.py)
        """
        player = view_on_player.get_player(ine)
        if round_in_progress == 1:
            player.score = view_on_tournament.get_player_attribute_from_round(
                tournament.tournament_id,
                ine,
                "points",
                round_in_progress)
            player_opponents = []
        else:
            player.score = view_on_tournament.get_player_attribute_from_round(
                tournament.tournament_id,
                ine,
                "points",
                round_in_progress - 1)
            player.opponents_faced = view_on_tournament.get_player_attribute_from_round(
                tournament.tournament_id,
                ine,
                "opponents_faced",
                round_in_progress - 1)

        if isinstance(player.score, type(None)):
            player.score = 0
        return player

    def get_filtered_players_list(
            self, tournament, round_in_progress, view_on_player, view_on_tournament):
        """
        Description:
        Sert la liste des joueurs limitée à certains attributs.
        Paramètres:
        - tournament: une instance de classe Tournament
        - round_in_progress: numéro de round
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/view_on_tournament_view.py)
        """
        filtered_players_list = []
        ine_players_list = self.get_tournament_players_list(tournament)
        for ine in ine_players_list:
            player = self.get_tournament_player_score(
                ine, tournament, round_in_progress, view_on_player, view_on_tournament)
            player_fullname = player.fullname
            filtered_players_list.append({
                "ine": ine,
                "points": player.score,
                "opponents_faced": player.opponents_faced,
                "fullname": player_fullname})
        return filtered_players_list

    def get_sorted_players_scores_list(self, tournament, view_on_player, view_on_tournament):
        """
        Description:
        Sert la liste des joueurs d'un tournoi triés par leurs points.
        Paramètres:
        - tournament: une instance de classe Tournament
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/view_on_tournament_view.py)
        """
        round_in_progress = tournament.current_round_id
        players_list = self.get_filtered_players_list(
            tournament, round_in_progress, view_on_player, view_on_tournament)
        sorted_mixed_players_list = self.sort_players_list_by_points(view_on_player, players_list)
        return sorted_mixed_players_list

    def create_new_round(
            self, tournament: tournament_model.Tournament, view_on_player, view_on_round, view_on_tournament):
        """
        Description:
        Sert à créér un nouveau round avec sa liste de matches.
        Paramètres:
        - tournament: une instance de classe Tournament
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_round: vue dédiée au round (views/round_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/view_on_tournament_view.py)
        """
        if tournament.status != tournament_model.Tournament.Status("in progress"):
            raise exceptions.TournamentStatusNotInProgressException()
        round_in_progress = tournament.current_round_id
        tournament_id = tournament.tournament_id
        sorted_mixed_players_list = self.get_sorted_players_scores_list(tournament, view_on_player, view_on_tournament)
        round_matches_list = []
        i = tournament.current_round_id
        round = round_model.Round(tournament_id=tournament_id, number=i)
        round_matches_list = []
        temp_sorted_mixed_players_list = sorted_mixed_players_list.copy()
        round_matches_list = self.round_matches_generator(temp_sorted_mixed_players_list)
        round.status = "in progress"
        now = datetime.now()
        round.start_date = now.strftime("%Y-%m-%d %H:%M:%S")
        round.matches_list = round_matches_list
        return round

    def do_all_round_matches_scored(self, round_matches_list):
        """
        Description:
        Sert à vérifier si tous les matches d'un round sont notés joués /ont un score.
        Paramètre:
        - round_matches_list: une liste d'instances de classes Match
        """
        all_matches_scored = True
        for match in round_matches_list:
            if not match_model.Match(match).is_match_scored():
                all_matches_scored = False
                break
        return all_matches_scored

    def mix_players_list(self, ine_players_list):
        """
        Description: sert à mélanger une liste de joueur
        Paramètres:
        - players_list: liste des ine des joueurs du tournoi
        """
        temp_players_list = ine_players_list.copy()
        total_players = len(temp_players_list)
        mixed_players_list = []
        for _ in range(1, len(ine_players_list) + 1):
            random_indice = random.randint(0, total_players - 1)
            mixed_players_list.append(temp_players_list.pop(random_indice))
            total_players -= 1
        return mixed_players_list

    def player_score(self, player: player_model.PlayerMatchModel):
        """
        Description:
        Sert à permettre d'avoir une liste de joueurs classés par points dans tournoi.
        Paramètres:
        - player: une instance de la classe PlayerMatchModel
        """
        return player["points"]

    def sort_players_list_by_points(self, view_on_player, mixed_players_list):
        """
        Description:
        Retourne une liste des joueurs classés sur la base des points.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - mixed_players_list: une liste mélangée de joueurs
        """
        sorted_mixed_players_list = mixed_players_list.copy()
        sorted_mixed_players_list.sort(key=self.player_score, reverse=True)
        return sorted_mixed_players_list

    def choose_opponent(self, player: player_model.Player, tournament_players_list):
        """
        Description:
        Sert à choisir un adversaire dans une liste de joueurs.
        La liste des joueurs du tournois est une liste d'ine.
        Paramètres:
        - player: une instance de classe Player
        - tournament_players_list: liste des ine des joeurs du tournoi
        """
        i = 1
        candidate = tournament_players_list[len(tournament_players_list) - i]
        while candidate["ine"] in player.opponents_faced:
            i += 1
            if player.ine == candidate["ine"]:
                continue
            if (len(tournament_players_list) - i) > 0:
                candidate = tournament_players_list[len(tournament_players_list) - i]
            else:
                break
        indice_to_remove = len(tournament_players_list) - i
        candidate = tournament_players_list[indice_to_remove]
        del tournament_players_list[indice_to_remove]
        return candidate

    def round_matches_generator(self, tournament_players_list):
        """
        Description:
        Sert à générer les matches d'un round.
        La liste des joueurs du tournois est une liste d'ine.
        Paramètres:
        - tournament_players_list: liste des ine des joeurs du tournoi
        """

        iterations = int(len(tournament_players_list) / 2)
        round_matches_list = []
        for _ in range(0, iterations):
            temp_player_1 = tournament_players_list.pop()
            player_1 = player_model.PlayerMatchModel(**temp_player_1)
            temp_player_2 = self.choose_opponent(player_1, tournament_players_list)
            player_2 = player_model.PlayerMatchModel(**temp_player_2)
            temp_tuple = ()
            if random.randint(1, 2) == 1:
                temp_tuple = ([player_1, 0], [player_2, 0])
            else:
                temp_tuple = ([player_2, 0], [player_1, 0])
            match = match_model.Match(temp_tuple)

            round_matches_list.append(temp_tuple)
        return round_matches_list

    def update_tournament_score(
            self,
            tournament: tournament_model.Tournament,
            view_on_tournament,
            round_matches_list: List[match_model.Match]):
        """
        Description:
        Sert à mettre à jour les scores d'un tournoi.
        La liste des joueurs du tournois est une liste d'ine.
        Paramètres:
        - tournament: une instance de classe Tournament
        - view_on_tournament: vue dédiée au tournoi ((views/tournament_view.py))
        - round_matches_list: liste des matches du round en cours
        """

        for match in round_matches_list:
            match_tuple = match.get_content()
            player_1_tuple = match_tuple[0][0]
            player_2_tuple = match_tuple[1][0]
            current_round = tournament.current_round_id
            tournament_id = tournament.tournament_id
            if current_round > 1:
                player_1_tuple.add_point(match_tuple[0][1])
                player_2_tuple.add_point(match_tuple[1][1])
            else:
                player_1_tuple.add_point(match_tuple[0][1])
                player_2_tuple.add_point(match_tuple[1][1])

    def update_match_scores(
            self,
            tournament: tournament_model.Tournament,
            view_on_player,
            view_on_round,
            view_on_tournament,
            view):
        """
        Description:
        Sert à présenter les matches sans score.
        Paramètres:
        - tournament: une instance de classe Tournament
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_round: vue dédiée au round (views/round_view.py)
        - view_on_tournament: vue dédiée au tournoi ((views/tournament_view.py))
        """
        round_in_progress = tournament.current_round_id
        round = view_on_tournament.get_round_from_tournament(tournament, round_in_progress)
        if isinstance(round, dict):
            current_round = round_model.Round(**round)
            current_round.matches_list = round['matches_list']
            round = current_round
        match_in_progress = tournament.current_match_id
        current_players_scores_to_update = []
        i = 1
        for match in round.matches_list:
            if i >= match_in_progress:
                current_players_scores_to_update.append(match)
            i += 1
        view_on_player.update_database_players_scores(current_players_scores_to_update)
        tournament.current_match_id += 1

        return tournament
