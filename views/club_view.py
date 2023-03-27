from controllers import club_controller, player_controller, tournament_controller
from models import club_model

view_on_club = club_controller.ClubController()
view_on_player = player_controller.PlayerController()
view_on_tournament = tournament_controller.TournamentController()


class ClubView:
    def create_club(self, club: club_model.Club):
        return view_on_club.create_club(club)

    def delete_club(self, club_id):
        return view_on_club.delete_club(club_id, view_on_player, view_on_club, view_on_tournament)

    def delete_clubs(self):
        return view_on_club.delete_clubs(view_on_player, view_on_club, view_on_tournament)

    def update_club(self, club_id, attribute, value):
        return view_on_club.update_club(club_id, attribute, value)

    def update_club_status(self, club_id, new_status):
        return view_on_club.update_club_status(club_id, new_status, view_on_player, view_on_club)

    def view_club(self, id, attribute=""):
        return view_on_club.get_club(id, attribute)

    def view_clubs(self, attribute=""):
        return view_on_club.get_clubs_list(attribute)
