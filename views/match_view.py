from controllers import match_controller, player_controller, tournament_controller, round_controller
from models import match_model

view_on_player = player_controller.PlayerController()
view_on_tournament = tournament_controller.TournamentController()
view_on_round = round_controller.RoundController()
view_on_match = match_controller.MatchController()


class MatchView:
    def view_match(self, match: match_model.Match):
        return view_on_match.view_match(match)
