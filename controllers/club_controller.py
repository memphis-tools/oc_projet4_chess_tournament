from pysondb import db
from models import club_model, player_model
from exceptions import exceptions
from .controller_shared import get_back_stringdate_into_date


class ClubController:
    def update_club_status(self, club_id, new_status, view_on_player, view_on_club):
        """
        Description:
        Sert à mettre à jour spécifiquement le statut d'un club.
        Paramètres:
        - club_id: id du club
        - new_status: chaine de caractère conforme à l'attente du modèle
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_club: vue dédiée au club (views/club_view.py)
        """
        try:
            club_player_list = self.get_club_players(club_id, view_on_player)
            self.update_club(club_id, "status", club_model.Club.Status(new_status))
            for ine in club_player_list:
                player = view_on_player.get_player(ine)
                if player.status != player_model.Player.Status("archived"):
                    view_on_player.update_player_status(ine, new_status, view_on_club)

            return True
        except ValueError:
            raise exceptions.StatusDoesNotExistsException()

    def delete_club(self, club_id, view_on_player, view_on_club, view_on_tournament):
        """
        Description:
        Sert à supprimer un club.
        Si club a 1 ou plusieurs joueur connus d'un ou plusieurs tournoi, alors il sera mis au statut archivé.
        Paramètres:
        - club_id: id du club
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_club: vue dédiée au club (views/club_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        """
        jsondb = db.getDb("data/clubs/clubs_db.json")
        club = self.get_club(club_id)
        if len(self.get_clubs_list()) == 0:
            return True
        if not club:
            raise exceptions.ClubIdDoesNotExistsException()
        club_pyson_id = jsondb.getByQuery({"club_id": f"{club_id}"})[0]["id"]
        try:
            view_on_player.delete_players_from_club(club_id, view_on_club, view_on_player, view_on_tournament)
            if jsondb.deleteById(club_pyson_id):
                return True
        except exceptions.IneExistsInTournamentException:
            self.update_club(club_id, "status", club_model.Club.Status("archived"))
            raise exceptions.ClubIdExistsInTournamentException()
        return False

    def delete_clubs(self, view_on_player, view_on_club, view_on_tournament):
        """
        Description:
        Sert à supprimer les clubs.
        Si club a 1 ou plusieurs joueur connus d'un ou plusieurs tournoi, alors il sera mis au statut archivé.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_club: vue dédiée au club (views/club_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        """
        jsondb = db.getDb("data/clubs/clubs_db.json")
        clubs_list = self.get_clubs_list()
        any_ine_in_tournament = False
        i = 1
        for club in clubs_list:
            try:
                self.delete_club(club.club_id, view_on_player, view_on_club, view_on_tournament)
                if i == len(clubs_list):
                    if jsondb.deleteAll():
                        return True
                i += 1
            except exceptions.ClubIdExistsInTournamentException:
                any_ine_in_tournament = True
                self.update_club(club.club_id, "status", club_model.Club.Status("archived"))
                continue
        if any_ine_in_tournament:
            raise exceptions.ClubIdExistsInTournamentException()
        return False

    def update_club(self, club_id, attribute, value):
        """
        Description:
        Sert à mettre à jour la valeur des attributs d'un club.
        Paramètres:
        - club_id: id du club
        - attribute: un attribut de la classe Player
        - value: une chaine de 1 ou plusieurs caractères
        """
        club = self.get_club(club_id)
        if not club:
            return False
        if attribute == "":
            raise exceptions.BlankFieldException()
        if attribute not in club.get_content().keys():
            raise exceptions.AttributeDoesNotExistsException()
        jsondb = db.getDb("data/clubs/clubs_db.json")
        club_pysondb_id = jsondb.getByQuery({'club_id': club_id})[0]["id"]
        jsondb.updateById(club_pysondb_id, {attribute: value})

    def get_club_players(self, club_id, view_on_player):
        """
        Description:
        Sert à obtenir une liste des ine des joueurs inscrits au club.
        Paramètres:
        - club_id: id du club
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        """
        jsondb = db.getDb("data/clubs/clubs_db.json")
        club = jsondb.getByQuery({"club_id": club_id})
        club_players_ine_list = []
        for player in view_on_player.get_players_list():
            if player.club_id == club_id:
                club_players_ine_list.append(player.ine)
        return club_players_ine_list

    def get_clubs_list(self, attribute=""):
        """
        Description:
        Sert à obtenir la liste des clubs.
        Paramètres:
        - attribute: facultatif. Il permet de cibler un attribut en particulier.
        """
        json_clubs_list = []
        jsondb = db.getDb("./data/clubs/clubs_db.json")
        json_clubs_list = jsondb.getAll()
        objects_club_list = []
        for json_club in json_clubs_list:
            club = club_model.Club(**json_club)
            club.status = player_model.Player.Status(json_club["status"])
            if attribute == "":
                objects_club_list.append(club)
            else:
                if attribute in club.get_content().keys():
                    objects_club_list.append(
                        {"club_id": club.get_content()["club_id"], f"{attribute}": club.get_content()[attribute]})
                else:
                    raise exceptions.AttributeDoesNotExistsException()
        return objects_club_list

    def get_club(self, club_id, attribute=""):
        """
        Description:
        Sert à obtenir une liste des ine des joueurs inscrits au club.
        Paramètres:
        - club_id: id du club
        - attribute: facultatif. Il permet de cibler un attribut en particulier.
        """
        if club_id == "":
            raise exceptions.BlankFieldException()
        jsondb = db.getDb("data/clubs/clubs_db.json")
        if len(self.get_clubs_list()) > 0:
            try:
                club_dict_from_json = jsondb.getByQuery({"club_id": club_id})[0]
            except IndexError:
                raise exceptions.ClubIdDoesNotExistsException()
            club_dict = {}
            unused_keys = []
            for key, value in club_dict_from_json.items():
                if key not in unused_keys:
                    if "date" in str(key):
                        club_dict[key] = get_back_stringdate_into_date(value)
                    else:
                        club_dict[key] = value
            club = club_model.Club(**club_dict)
            club.status = player_model.Player.Status(club_dict_from_json["status"])
            if attribute == "":
                return club
            else:
                if attribute in club.get_content().keys():
                    return {"club_id": club_id, f"{attribute}": club.get_content()[attribute]}
                else:
                    raise exceptions.AttributeDoesNotExistsException()
        return False

    def create_club(self, new_club: club_model.Club):
        """
        Description:
        Fonction appelée par le biais de la vue dédiée.
        Elle récupère l'instance de classe club, et met à jour de la base de données JSON correspondante.
        Paramètres:
        - new_club: une instance de classe club
        """
        try:
            if self.get_club(new_club.club_id):
                raise exceptions.ClubIdAlreadyExistsException()
        except exceptions.ClubIdDoesNotExistsException:
            pass
        jsondb = db.getDb("data/clubs/clubs_db.json")
        jsondb.add(new_club.get_club())
        return True
