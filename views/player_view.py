from controllers import club_controller, player_controller, tournament_controller
from models import player_model

view_on_club = club_controller.ClubController()
view_on_player = player_controller.PlayerController()
view_on_tournament = tournament_controller.TournamentController()


class PlayerView:
    def create_player(self, player: player_model.Player):
        return view_on_player.create_player(player)

    def delete_player(self, ine):
        return view_on_player.delete_player(ine, view_on_tournament, view_on_club)

    def delete_players(self):
        return view_on_player.delete_players(view_on_tournament, view_on_club)

    def delete_players_from_club(self, club_id):
        return view_on_player.delete_players_from_club(club_id, view_on_club, view_on_player, view_on_tournament)

    def find_player_category(self, birthdate):
        return view_on_player.find_player_category(birthdate)

    def update_database_players_scores(self, rounds_list, called_method="add"):
        return view_on_player.update_database_players_scores(rounds_list, called_method="add")

    def update_player(self, ine, attribute, value):
        return view_on_player.update_player(ine, attribute, value)

    def update_player_status(self, ine, new_status):
        return view_on_player.update_player_status(ine, new_status, view_on_club)

    def verify_ine_input(self, ine):
        return view_on_player.verify_ine_input(ine)

    def view_club_players(self, club_id):
        return view_on_player.get_club_players(club_id, view_on_player)

    def view_player(self, ine, attribute=""):
        return view_on_player.get_player(ine, attribute)

    def view_players(self, attribute=""):
        return view_on_player.get_players_list(attribute)

    def view_players_by_club_list(self, club_id, attribute=""):
        return view_on_player.get_players_by_club_list(club_id, attribute)

    def view_players_by_status(self, status):
        return view_on_player.get_players_by_status(status)
