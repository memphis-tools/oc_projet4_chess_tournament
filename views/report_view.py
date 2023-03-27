from controllers import player_controller, report_controller, tournament_controller
from models import tournament_model

view_on_player = player_controller.PlayerController()
view_on_report = report_controller.ReportController()
view_on_tournament = tournament_controller.TournamentController()


class ReportView:
    def get_sorted_players_list(self, output_type="text"):
        return view_on_report.get_sorted_players_list(view_on_player, output_type)

    def get_tournaments_list(self, output_type="text"):
        return view_on_report.get_tournaments_list(view_on_tournament, output_type)

    def get_tournament_name_and_dates(self, tournament: tournament_model.Tournament, output_type="text"):
        return view_on_report.get_tournament_name_and_dates(view_on_tournament, tournament, output_type)

    def get_tournament_rounds_and_matches(self, tournament: tournament_model.Tournament, output_type="text"):
        return view_on_report.get_tournament_rounds_and_matches(view_on_tournament, tournament, output_type)

    def get_tournament_sorted_players_list(self, tournament: tournament_model.Tournament, output_type="text"):
        return view_on_report.get_tournament_sorted_players_list(
            view_on_player,
            view_on_tournament,
            tournament,
            output_type)
