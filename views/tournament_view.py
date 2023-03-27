from controllers import player_controller, tournament_controller
from models import tournament_model, round_model

view_on_player = player_controller.PlayerController()
view_on_tournament = tournament_controller.TournamentController()


class TournamentView:
    def add_a_new_existing_player(self, ine, tournament: tournament_model.Tournament):
        return view_on_tournament.add_a_new_existing_player(view_on_player, ine, tournament)

    def create_tournament(self, tournament: tournament_model.Tournament):
        return view_on_tournament.create_tournament(view_on_player, tournament)

    def delete_player_from_list(self, ine, tournament: tournament_model.Tournament):
        return view_on_tournament.delete_player_from_list(view_on_player, ine, tournament)

    def delete_tournament(self, tournament_id):
        return view_on_tournament.delete_tournament(tournament_id, view_on_player)

    def delete_tournaments(self):
        return view_on_tournament.delete_tournaments(view_on_player)

    def get_player_points_from_tournament(self, tournament: tournament_model.Tournament, ine):
        return view_on_tournament.get_player_points_from_tournament(tournament, ine)

    def get_players_opponents_and_score(self, tournament_id):
        return view_on_tournament.get_players_opponents_and_score(tournament_id)

    def get_round_from_tournament(self, tournament: tournament_model.Tournament, round_in_progress):
        return view_on_tournament.get_round_from_tournament(tournament, round_in_progress)

    def get_tournament_match_id(self, tournament_id):
        return view_on_tournament.get_tournament_match_id(tournament_id)

    def update_round_in_tournament_database(self, tournament: tournament_model.Tournament, round: round_model.Round):
        return view_on_tournament.update_round_in_tournament_database(tournament, round)

    def update_tournament_database(self, tournament_id, attribute, value):
        return view_on_tournament.update_tournament_database(tournament_id, attribute, value)

    def update_tournament_database_with_matches_scores(self, tournament: tournament_model.Tournament, match):
        return view_on_tournament.update_tournament_database_with_matches_scores(tournament, match)

    def update_tournament_end_date_if_terminated(self, tournament: tournament_model.Tournament):
        return view_on_tournament.update_tournament_end_date_if_terminated(tournament)

    def update_tournament_rounds_list(self, tournament_id, round: round_model.Round):
        return view_on_tournament.update_tournament_rounds_list(tournament_id, round)

    def update_tournament_status(self, tournament_id, new_status):
        return view_on_tournament.update_tournament_status(tournament_id, new_status)

    def view_tournament(self, tournament_id, attribute=""):
        return view_on_tournament.get_tournament(tournament_id, attribute)

    def view_tournament_by_id(self, tournament_id, attribute=""):
        return view_on_tournament.get_tournament_by_id(tournament_id, attribute)

    def view_tournaments(self, attribute=""):
        return view_on_tournament.get_tournaments_list(attribute)
