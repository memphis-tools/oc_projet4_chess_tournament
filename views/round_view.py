from controllers import player_controller, tournament_controller, round_controller
from models import match_model, tournament_model

view_on_player = player_controller.PlayerController()
view_on_tournament = tournament_controller.TournamentController()
view_on_round = round_controller.RoundController()


class RoundView:
    def create_new_round(self, tournament: tournament_model.Tournament):
        return view_on_round.create_new_round(tournament, view_on_player, view_on_round, view_on_tournament)

    def do_all_round_matches_scored(self, round_matches_list):
        return view_on_round.do_all_round_matches_scored(round_matches_list)

    def get_debug_infos_for_evaluation(
            sorted_mixed_players_list,
            round_matches_list,
            tournament_id):
        return view_on_round.get_debug_infos_for_evaluation(
            sorted_mixed_players_list,
            round_matches_list,
            tournament_id,
            view_on_tournament)

    def get_sorted_players_scores_list(self, tournament: tournament_model.Tournament):
        return view_on_round.get_sorted_players_scores_list(tournament, view_on_player, view_on_tournament)

    def set_a_match_score(self, match: match_model.Match, winner_code):
        return view_on_round.set_a_match_score(match, winner_code)

    def update_match_scores(self, tournament: tournament_model.Tournament):
        return view_on_round.update_match_scores(tournament, view_on_player, view_on_round, view_on_tournament, self)

    def update_rounds(self, tournament: tournament_model.Tournament):
        return view_on_round.update_rounds(tournament, view_on_player, view_on_tournament)
