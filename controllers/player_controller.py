import re
from datetime import date
from pysondb import db
from typing import List
from models import match_model, player_model
from exceptions import exceptions
from .controller_shared import get_back_stringdate_into_date

# INE: Identifiant National Echec
INE_PATTERN = re.compile(r'^\w{2}[0-9]{5}$')
PLAYER_CATEGORIES_DICT = player_model.PLAYER_CATEGORIES_DICT


class PlayerController:
    def update_player_status(self, ine, new_status, view_on_club):
        """
        Description:
        Sert à mettre à jour spécifiquement le statut d'un joueur.
        Paramètres:
        - ine: ine du joueur
        - new_status: chaine de caractère conforme à l'attente du modèle
        - view_on_club: vue dédiée au club (views/club_view.py)
        """
        try:
            player_club_id = self.get_player(ine).club_id
            club = view_on_club.get_club(player_club_id)
            return self.update_player(ine, "status", player_model.Player.Status(new_status))
        except ValueError:
            raise exceptions.StatusDoesNotExistsException()

    def find_player_category(self, birth_date):
        """
        Description:
        Sert à déterminer la catégorie du joueur, en fonction de sa date de naissance.
        Paramètres:
        - birth_date: une instance de classe datetime.date
        """
        def format_digit(digit):
            if digit < 10:
                return str(f"0{digit}")
            else:
                return digit
        today = date.today()
        delta_years = today.year - birth_date.year
        pivot_date = date.fromisoformat(
            f"{today.year}-{format_digit(birth_date.month)}-{format_digit(birth_date.day)}")
        player_age = 0
        if pivot_date >= birth_date:
            player_age = delta_years
        else:
            player_age = delta_years - 1
        categories_dict = PLAYER_CATEGORIES_DICT

        for category_dict in categories_dict:
            category = categories_dict[category_dict]
            if player_age >= int(category["min"]) and player_age <= int(category["max"]):
                return category_dict

        return False

    def delete_player(self, ine, view_on_tournament, view_on_club):
        """
        Description:
        Sert à supprimer un joueur.
        Si joueur connu d'un ou plusieurs tournoi, alors il sera mis au statut archivé.
        Paramètres:
        - ine: ine du joueur
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        - view_on_club: vue dédiée au club (views/club_view.py)
        """
        if len(self.get_players_list()) == 0:
            return True
        if not self.get_player(ine):
            raise exceptions.IneDoesNotExistsException()
        jsondb = db.getDb("data/players/players_db.json")
        player_pyson_id = jsondb.getByQuery({"ine": f"{ine}"})[0]["id"]
        all_ine = view_on_tournament.get_all_ine_from_tournaments()
        if ine not in view_on_tournament.get_all_ine_from_tournaments():
            if jsondb.deleteById(player_pyson_id):
                return True
        else:
            self.update_player_status(ine, "archived", view_on_club)
            raise exceptions.IneExistsInTournamentException()
        return False

    def delete_players_from_club(self, club_id, view_on_club, view_on_player, view_on_tournament):
        """
        Description:
        Sert à supprimer l'ensemble des joueurs d'un club.
        Si joueur connu d'un ou plusieurs tournoi, alors il sera mis au statut archivé.
        Paramètres:
        - club_id: id du club
        - view_on_club: vue dédiée au club (views/club_view.py)
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        """
        jsondb = db.getDb("data/players/players_db.json")
        club_players_list = view_on_club.get_club(club_id)
        has_a_player_played_tournament = False
        for ine in view_on_club.get_club_players(club_id, view_on_player):
            try:
                if ine not in view_on_tournament.get_all_ine_from_tournaments():
                    self.delete_player(ine, view_on_tournament, view_on_club)
                else:
                    self.update_player_status(ine, "archived", view_on_club)
                    raise exceptions.IneExistsInTournamentException()
            except exceptions.IneExistsInTournamentException:
                has_a_player_played_tournament = True
                continue
        if has_a_player_played_tournament:
            raise exceptions.IneExistsInTournamentException()
        return True

    def delete_players(self, view_on_tournament, view_on_club):
        """
        Description:
        Sert à supprimer l'ensemble des joueurs de l'application.
        Si joueur connu d'un ou plusieurs tournoi, alors il sera mis au statut archivé.
        Paramètres:
        - club_id: id du club
        - view_on_club: vue dédiée au club (views/club_view.py)
        - view_on_tournament: vue dédiée au tournoi (views/tournament_view.py)
        """
        jsondb = db.getDb("data/players/players_db.json")
        players_list = jsondb.getAll()
        archived_done = False
        for player_dict in players_list:
            try:
                self.delete_player(player_dict['ine'], view_on_tournament, view_on_club)
                if jsondb.deleteAll():
                    return True
            except exceptions.IneExistsInTournamentException:
                archived_done = True
                continue
        if archived_done:
            raise exceptions.IneExistsInTournamentException()
        return False

    def verify_ine_input(self, ine):
        """
        Description:
        Sert à vérifier un ine saisi. Il doit être valide à la regex INE_PATTERN
        Paramètres:
        - ine: un ine au format attendu.
        """
        if isinstance(re.search(INE_PATTERN, ine), type(None)):
            raise exceptions.IneDoesNotRespectPatternException()

    def update_player(self, ine, attribute, value):
        """
        Description:
        Sert à mettre à jour la valeur des attributs d'un joueur.
        Il n'est pas autorisé de modifier un ine.
        Paramètres:
        - ine: ine du joueur
        - attribute: un attribut de la classe Player
        - value: une chaine de 1 ou plusieurs caractères
        """
        player = self.get_player(ine)
        if not player:
            return False
        if attribute == "":
            raise exceptions.BlankFieldException()
        if attribute not in player.get_content().keys():
            raise exceptions.IneDoesNotExistsException()

        jsondb = db.getDb("data/players/players_db.json")
        player_pysondb_id = jsondb.getByQuery({'ine': ine})[0]["id"]
        if attribute == "points":
            jsondb.updateById(player_pysondb_id, {attribute: int(value)})
        elif attribute == "f_name":
            jsondb.updateById(player_pysondb_id, {attribute: value})
            jsondb.updateById(player_pysondb_id, {"fullname": f"{player.l_name} {value}"})
        elif attribute == "l_name":
            jsondb.updateById(player_pysondb_id, {attribute: value})
            jsondb.updateById(player_pysondb_id, {"fullname": f"{value} {player.f_name}"})
        elif attribute == "ine":
            raise exceptions.IneCanNotBeUpdateException()
        else:
            jsondb.updateById(player_pysondb_id, {attribute: value})
        return True

    def update_database_player_score(self, ine, attribute, value, called_method="add"):
        """
        Description:
        Sert à mettre à jour spécifiquement le nombre de points total d'un joueur.
        Paramètres:
        - ine: ine du joueur
        - attribute: un attribut de la classe Player
        - value: une chaine de 1 ou plusieurs caractères
        - called_method: 'add' ou 'substract'
        """
        player = self.get_player(ine)
        if not player:
            return False
        if attribute == "":
            raise exceptions.BlankFieldException()
        if attribute not in player.get_content().keys():
            raise exceptions.IneDoesNotExistsException()

        jsondb = db.getDb("data/players/players_db.json")
        player = jsondb.getByQuery({"ine": ine})[0]
        if called_method == "add":
            if not isinstance(player, dict):
                new_points = player.points + value
            else:
                new_points = player["points"] + value
        elif called_method == "substract":
            if not isinstance(player, dict):
                new_points = player.points - value
            else:
                new_points = player["points"] - value
        if not isinstance(player, dict):
            player_pysondb_id = jsondb.getByQuery({"ine": player.ine})[0]["id"]
        else:
            player_pysondb_id = jsondb.getByQuery({"ine": player["ine"]})[0]["id"]
        jsondb.updateById(player_pysondb_id, {attribute: new_points})

    def update_database_players_scores(self, matches_list: List[match_model.Match], called_method="add"):
        """
        Description:
        Sert à parcourir les matches d'une liste de tour.
        On enclenche une mise à jour en ajout/retrait des points des joueurs des matches.
        Paramètres:
        - matches_list: liste d'instances de la classe Match
        - called_method: 'add' ou 'substract'
        """
        if called_method == "add":
            for matches in matches_list:
                m = match_model.Match(matches)
                player_1 = m.get_player_1()
                player_2 = m.get_player_2()
                tupple_match_score = m.get_match_point_to_add_or_delete()
                if not isinstance(player_1, dict):
                    self.update_database_player_score(player_1.ine, "points", tupple_match_score[0], called_method)
                    self.update_database_player_score(player_2.ine, "points", tupple_match_score[1], called_method)
                else:
                    self.update_database_player_score(player_1['ine'], "points", tupple_match_score[0], called_method)
                    self.update_database_player_score(player_2['ine'], "points", tupple_match_score[1], called_method)
        elif called_method == "substract":
            for matches in matches_list[0]:
                m = match_model.Match(matches)
                player_1 = m.get_player_1()
                player_2 = m.get_player_2()
                tupple_match_score = m.get_match_point_to_add_or_delete()
                if not isinstance(player_1, dict):
                    self.update_database_player_score(player_1.ine, "points", tupple_match_score[0], called_method)
                    self.update_database_player_score(player_2.ine, "points", tupple_match_score[1], called_method)
                else:
                    self.update_database_player_score(player_1['ine'], "points", tupple_match_score[0], called_method)
                    self.update_database_player_score(player_2['ine'], "points", tupple_match_score[1], called_method)

    def get_players_list(self, attribute=""):
        """
        Description:
        Sert à obtenir la liste des joueurs de l'application.
        En sortie, une liste d'instance de classe Player
        Paramètres:
        - attribute: facultatif, permet de pointer un attribut de la classe Player
        """
        jsondb = db.getDb("data/players/players_db.json")
        json_players_list = jsondb.getAll()
        object_players_list = []
        unused_keys = ['category']

        for json_player in json_players_list:
            player_dict = {}
            for key, value in json_player.items():
                if key not in unused_keys:
                    if "date" in str(key):
                        player_dict[key] = get_back_stringdate_into_date(value)
                    else:
                        player_dict[key] = value
            player_category = self.find_player_category(player_dict["birth_date"])
            player_dict['category'] = player_category
            player = player_model.Player(**player_dict)
            player.status = player_dict["status"]
            player.points = player_dict["points"]
            if attribute == "":
                object_players_list.append(player)
            else:
                if attribute in player.get_content().keys():
                    object_players_list.append(
                        {"ine": player.get_content()["ine"], f"{attribute}": player.get_content()[attribute]})
                else:
                    raise exceptions.AttributeDoesNotExistsException()
        return object_players_list

    def get_players_by_club_list(self, club_id, attribute):
        """
        Description:
        Sert à obtenir la liste des joueurs d'un club.
        En sortie, une liste de joueurs représentés par un dictionnaire.
        Paramètres:
        - club_id: id du club
        - attribute: facultatif, permet de pointer un attribut de la classe Player
        """
        jsondb = db.getDb("data/players/players_db.json")
        players_list = jsondb.getByQuery({"club_id": club_id})
        if attribute == "":
            return players_list
        else:
            if attribute in players_list[0].keys():
                temp_players_list = []
                for player in players_list:
                    temp_players_list.append({"ine": player["ine"], f"{attribute}": player[attribute]})
                return temp_players_list
            else:
                raise exceptions.AttributeDoesNotExistsException()

    def get_players_by_status(self, status):
        """
        Description:
        Sert à obtenir une liste des joueurs en fonction de leur statut.
        En sortie, une liste d'instances de classe Player.
        Paramètres:
        - status: chaine de caractère conforme l'attente du modèle Player.
        """
        jsondb = db.getDb("data/players/players_db.json")
        json_players_list = jsondb.getByQuery({"status": status})
        if len(json_players_list) == 0:
            raise exceptions.StatusDoesNotExistsException()
        object_players_list = []
        for json_player in json_players_list:
            object_players_list.append(self.get_player(json_player["ine"]))
        return object_players_list

    def get_player_by_ine(self, ine):
        """
        Description:
        Sert à obtenir une instance de classe Player correspondant à l'ine.
        Paramètres:
        - ine: un ine
        """
        jsondb = db.getDb("data/players/players_db.json")
        json_player_list = jsondb.getByQuery({"ine": ine})
        if len(json_player_list) == 0:
            raise exceptions.IneDoesNotExistsException()
        object_player_list = []
        for json_player in json_player_list:
            object_player_list.append(self.get_player(json_player["ine"]))
        return object_player_list

    def get_player(self, ine, attribute=""):
        """
        Description:
        Sert à confectionner et retourner une instance de classe Player.
        Sans attribut spécifique, c'est l'instance de classe qui est retournée.
        Si attribut spécifié, alors c'est un dictionnaire représentant le joueur qui est retourné.
        Paramètres:
        - ine: un ine
        - attribute: facultatif, permet de pointer un attribut de la classe Player
        """
        if ine == "":
            raise exceptions.BlankFieldException()
        jsondb = db.getDb("data/players/players_db.json")
        try:
            player_dict_from_json = jsondb.getByQuery({"ine": ine})[0]
        except IndexError:
            raise exceptions.IneDoesNotExistsException()
        player_dict = {}
        unused_keys = ['category']
        for key, value in player_dict_from_json.items():
            if key not in unused_keys:
                if "date" in str(key):
                    player_dict[key] = get_back_stringdate_into_date(value)
                else:
                    player_dict[key] = value
        player_category = self.find_player_category(player_dict["birth_date"])
        player_dict['category'] = player_category
        player = player_model.Player(**player_dict)
        player.status = player_dict_from_json['status']
        if attribute == "":
            return player
        else:
            if attribute in player.get_content().keys():
                return {"ine": ine, f"{attribute}": player.get_content()[attribute]}
            else:
                raise exceptions.AttributeDoesNotExistsException()
        return False

    def create_player(self, new_player: player_model.Player):
        """
        Description:
        Fonction appelée par le biais de la vue dédiée.
        Elle récupère l'instance de classe Player, et met à jour de la base de données JSON correspondante.
        Paramètres:
        - new_player: une instance de classe Player
        """
        try:
            if self.get_player_by_ine(new_player.ine):
                raise exceptions.IneAlreadyExistsException()
        except exceptions.IneDoesNotExistsException:
            pass
        jsondb = db.getDb("data/players/players_db.json")
        jsondb.add(new_player.get_player())
        return True
