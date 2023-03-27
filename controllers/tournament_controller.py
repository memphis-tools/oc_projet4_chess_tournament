import json
from datetime import datetime
from pysondb import db
from typing import List
from models import match_model, player_model, round_model, tournament_model
from exceptions import exceptions
from .controller_shared import get_back_stringdate_into_date


class TournamentController:
    def update_tournament_rounds_list(self, tournament_id, round):
        """
        Description:
        Sert à ajouter un round avec ses matches, au tournoi en cours.
        Paramètres:
        - tournament_id: le id du tournoi
        - round: une instance de la classe Round
        """
        tournament = self.get_tournament_by_id(tournament_id)
        tournament.rounds_list.append(round)
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        jsondb_tournament = jsondb.getByQuery({"tournament_id": tournament_id})
        tournament_pysondb_id = jsondb_tournament[0]["id"]
        rounds_list = jsondb_tournament[0]["rounds_list"]
        rounds_list.append(round.get_content())
        x = tournament.get_content()['rounds_list']
        temp_list = []
        for round in x:
            temp_match = ()
            if not isinstance(round, dict):
                temp_list.append(round.get_content())
            else:
                temp_list.append(round)
        a = db.getDb("data/tournaments/tournaments_db.json")
        a.getBy({"tournament_id": tournament_id})
        a.updateByQuery({"tournament_id": tournament_id}, {"rounds_list": temp_list})
        return tournament

    def update_tournament_status(self, tournament_id, new_status):
        """
        Description:
        Sert à mettre à jour le statut d'un tournoi.
        Paramètres:
        - tournament_id: le id du tournoi
        - new_status: une chaine de caractères, dont le contenu doit correspondre à l'attente du modèle.
        """
        try:
            self.update_tournament_database(tournament_id, "status", tournament_model.Tournament.Status(new_status))
            return True
        except ValueError:
            raise exceptions.StatusDoesNotExistsException()

    def delete_player_from_list(self, view_on_player, ine, tournament: tournament_model.Tournament):
        """
        Description:
        Sert à retirer un joueur de la liste des joueurs d'un tournoi lors de sa création.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - ine: ine du joueur.Chaine de caractères.
        - tournament: une instance de classe Tournament
        """
        players_list = view_on_player.get_players_by_status("active")
        player_to_remove = view_on_player.get_player(ine)
        final_players_list = []
        if not player_to_remove:
            raise exceptions.IneDoesNotExistsException()
        else:
            for player in players_list:
                if player.ine != player_to_remove.ine:
                    final_players_list.append(player)
            tournament.players_list = final_players_list
        return tournament

    def add_a_new_existing_player(self, view_on_player, ine, tournament: tournament_model.Tournament):
        """
        Description:
        Sert à ajouter un joueur à la liste des joueurs d'un tournoi lors de sa création.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        - ine: ine du joueur.Chaine de caractères.
        - tournament: une instance de classe Tournament
        """
        player = view_on_player.get_player(ine)
        if not player:
            raise exceptions.IneDoesNotExistsException()
        else:
            if player[0]["status"] == "active":
                tournament.get_tournament()["player_list"] = player
            else:
                raise exceptions.PlayerStatusNotActiveException()
        return True

    def get_tournaments_list(self, attribute=""):
        """
        Description:
        Sert à obtenir la liste des tournois.
        Paramètres:
        - attribute: facultatif, permet de pointer un attribut de la classe Tournament
        """
        tournaments_list: List[tournament_model.Tournament] = []
        jsondb = db.getDb("./data/tournaments/tournaments_db.json")
        json_tournaments_list = jsondb.getAll()
        object_tournaments_list = []
        unused_keys = []
        for json_tournament in json_tournaments_list:
            tournament_dict = {}
            for key, value in json_tournament.items():
                if key not in unused_keys:
                    if "date" in str(key):
                        tournament_dict[key] = get_back_stringdate_into_date(value)
                    else:
                        tournament_dict[key] = value
            tournament = self.generate_tournament_from_json(tournament_dict)
            if attribute == "":
                object_tournaments_list.append(tournament)
            else:
                if attribute in tournament.get_content().keys():
                    object_tournaments_list.append(
                        {
                            "tournament_id": tournament.get_content()["tournament_id"],
                            f"{attribute}": tournament.get_content()[attribute]
                        })
                else:
                    raise exceptions.AttributeDoesNotExistsException()
        return object_tournaments_list

    def get_all_ine_from_tournaments(self):
        """
        Description:
        Sert à obtenir la liste de l'ensemble des ine connus dans les tounois.
        Paramètres:
        """
        ine_set = set({})
        for tournament in self.get_tournaments_list():
            for player_ine in tournament.players_list:
                ine_set.add(player_ine)
        return ine_set

    def get_round_from_tournament(self, tournament: tournament_model.Tournament, round_number):
        """
        Description:
        Sert à retourner une instance de classe Round d'un tournoi.
        Paramètres:
        - tournament: une instance de classe Tournament
        - round_number: numéro du round
        """
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        tournament_pysondb_id = jsondb.getByQuery({"tournament_id": tournament.tournament_id})[0]["id"]
        r1 = jsondb.getByQuery({"tournament_id": tournament.tournament_id})[0]
        t1 = tournament_model.Tournament(**r1)
        t1.rounds_list = tournament.rounds_list
        for round in t1.rounds_list:
            if isinstance(round, dict):
                r = round_model.Round(**round)
            else:
                r = round
            if r.number == int(round_number):
                return round

        return None

    def update_round_in_tournament_database(self, tournament: tournament_model.Tournament, round):
        """
        Description:
        Sert à mettre à jour la référence du round actuellement joué.
        De même la référence du match est initialisée à 1
        Paramètres:
        - tournament: une instance de classe Tournament
        - round: une instance de la classe Round
        """
        round_number = round.number
        tournament_id = tournament.tournament_id
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        json_tournament = jsondb.getByQuery({"tournament_id": tournament_id})

        new_round_id = json_tournament[0]["current_round_id"] + 1
        tournament_pyson_id = json_tournament[0]["id"]
        jsondb.updateById(tournament_pyson_id, {'current_round_id': new_round_id})
        jsondb.updateById(tournament_pyson_id, {'current_match_id': 1})

    def update_tournament_end_date_if_terminated(self, tournament: tournament_model.Tournament):
        """
        Description:
        Vérifie si le tournoi est terminé, et met à jour le statut le cas échéant.
        Paramètres:
        - tournament: une instance de classe Tournament
        """
        round_in_progress = tournament.current_round_id
        round = self.get_round_from_tournament(tournament, round_in_progress)
        if isinstance(round, dict):
            round_matches_list = round['matches_list']
        else:
            round_matches_list = round.matches_list
        nb_matches = len(round_matches_list)
        if tournament.current_round_id == int(tournament.nb_rounds) and tournament.current_match_id > nb_matches:
            self.update_tournament_database(tournament.tournament_id, "status", "ended")

    def get_player_points_from_tournament(self, tournament, ine):
        """
        Description:
        Retourne le nombre de points aquis par un joueur dans un tournoi
        Paramètres:
        - tournament: une instance de classe Tournament
        - ine: un ine au format attendu.
        """
        player_points = 0
        last_round_scored = tournament.current_round_id - 1
        if last_round_scored == 0:
            last_round_scored = 1
        for match in tournament.rounds_list[last_round_scored - 1]:
            if match[0][0].ine == ine:
                player_points = match[0][0].points
            elif match[1][0].ine == ine:
                player_points = match[1][0].points
        return player_points

    def get_player_from_round_match(self, ine, round):
        """
        Description:
        On renvoit le joueur demandé dans un round.
        Retourne une instance de PlayerMatchModel.
        Paramètres:
        - ine: un ine au format attendu.
        - round: une instance de la classe Round
        """
        for match in round["matches_list"]:
            player = match_model.Match(match).get_player_by_ine(ine)
            if player:
                return player

    def get_player_attribute_from_round(self, tournament_id, ine, attribute, round_number):
        """
        Description:
        Sert à retourner un attribut d'un joueur d'un match.
        Paramètres:
        - tournament_id: id du tournoi
        - ine: un ine au format attendu.
        - attribute: attribut demandé
        - round_number: id du round ciblé
        """
        if tournament_id == "":
            raise exceptions.BlankFieldException()
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        json_tournament = jsondb.getByQuery({"tournament_id": tournament_id})
        tournament = self.get_tournament(json_tournament[0]["tournament_id"])
        round = self.get_round_from_tournament(tournament, round_number)
        if round is not None:
            player_from_match_tupple = self.get_player_from_round_match(ine, round)
            player_content_dict = player_from_match_tupple
            if attribute not in player_content_dict.keys():
                raise exceptions.AttributeDoesNotExistsException()
            return player_content_dict[attribute]

    def delete_tournament(self, tournament_id, view_on_player):
        """
        Description:
        Sert à supprimer un tournoi. Ceci implique la mise à jour des scores des joueurs.
        Paramètres:
        - tournament_id: id du tournoi
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        """
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        tournament = jsondb.getByQuery({"tournament_id": tournament_id})
        if len(tournament) == 0:
            raise exceptions.TournamentIdDoesNotExistsException()
        tournament_pyson_id = jsondb.getByQuery({"tournament_id": f"{tournament_id}"})[0]["id"]
        if tournament[0]["status"] == "ended":
            last_round_played = tournament[0]["current_round_id"]
            rounds_list = jsondb.find(tournament_pyson_id)["rounds_list"]
            while int(last_round_played) > 1:
                matches_list = []
                for match in rounds_list:
                    if int(match["number"]) == int(last_round_played) - 1:
                        matches_list.append(match["matches_list"])
                view_on_player.update_database_players_scores(matches_list, called_method="substract")
                last_round_played -= 1
        elif tournament[0]["status"] == "in progress" and tournament[0]["current_round_id"] > 1:
            last_round_played = tournament[0]["current_round_id"]
            rounds_list = jsondb.find(tournament_pyson_id)["rounds_list"]
            while int(last_round_played) > 1:
                matches_list = []
                for match in rounds_list:
                    if int(match["number"]) == int(last_round_played) - 1:
                        matches_list.append(match["matches_list"])
                view_on_player.update_database_players_scores(matches_list, called_method="substract")
                last_round_played -= 1

        if jsondb.deleteById(tournament_pyson_id):
            return True
        return False

    def delete_tournaments(self, view_on_player):
        """
        Description:
        Sert à supprimer l'ensemble des tournois. Ceci implique la mise à jour des scores des joueurs.
        Paramètres:
        - view_on_player: vue dédiée au joueur (views/player_view.py)
        """
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        for tournament in jsondb.getAll():
            self.delete_tournament(tournament["tournament_id"], view_on_player)
        if jsondb.deleteAll():
            return True
        return False

    def get_tournament_match_id(self, tournament_id):
        """
        Description:
        Retourne l'id du match en cours, depuis la base de données du tournoi.
        Paramètres:
        - tournament_id: id du tournoi
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        current_match_id = jsondb.get()[0]['current_match_id']
        return current_match_id

    def get_players_opponents_and_score(self, tournament_id):
        """
        Description:
        Retourne une liste constituée de dictionnaires. A chaque joueur un dictionnaire.
        Le dictionnaire reprend nom du joueur, ine, ses points actuel et adversaires rencontrés.
        Paramètres:
        - tournament_id: id du tournoi
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        x = jsondb.getByQuery({"tournament_id": tournament_id})
        r_list = x[0]['rounds_list']
        current_round_id = tournament.current_round_id
        players_list_dicts = []
        if len(r_list) > 0:
            if current_round_id > 2:
                i = current_round_id - 2
            else:
                i = 0
            for match in r_list[i]['matches_list'][0]:
                players_list_dicts.append(match[0])
        return players_list_dicts

    def update_tournament_database(self, tournament_id, attribute, value):
        """
        Description:
        Sert à mettre à jour la valeur des attributs d'un tournoi.
        Paramètres:
        - tournament_id: id du tournoi
        - attribute: un attribut de la classe Tournament
        - value: une chaine de 1 ou plusieurs caractères
        """
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        tournament_pyson_id = jsondb.getByQuery({"tournament_id": tournament_id})[0]["id"]
        jsondb.updateById(tournament_pyson_id, {attribute: value})

    def get_tournament_by_id(self, tournament_id, attribute=""):
        """
        Description:
        Sert à vérifier si un tournoi existe.
        Sortie est un dictionnaire représentant les données.
        Paramètres:
        - tournament_id: id du tournoi
        """
        if tournament_id == "":
            raise exceptions.BlankFieldException()
        tournament = self.get_tournament(tournament_id)
        if not tournament:
            raise exceptions.TournamentIdDoesNotExistsException()
        return tournament

    def generate_tournament_from_json(self, tournament_dict):
        """
        Description:
        Sert à retourner une instance de classe tournoi.
        Celle-ci est basée
        Paramètres:
        - tournament_dict: représentation d'un tournoi sous forme d'un dictionnaire.
        """
        tournament = tournament_model.Tournament(**tournament_dict)
        tournament.players_list = tournament_dict["players_list"]
        tournament.refresh_nb_players()
        tournament.rounds_list = tournament_dict["rounds_list"]

        if isinstance(tournament_dict["rounds_list"], list):
            json_rounds_list = tournament_dict["rounds_list"]
        elif isinstance(tournament_dict["rounds_list"], str):
            json_rounds_list = eval(f"{tournament_dict['rounds_list']}")
        else:
            json_rounds_list = json.loads(tournament_dict["rounds_list"])

        tournament.status = tournament_dict["status"]
        tournament.current_round_id = tournament_dict["current_round_id"]
        return tournament

    def get_tournament(self, tournament_id, attribute=""):
        """
        Description:
        Sert à confectionner et retourner une instance de classe Tournament.
        Sans attribut spécifique, c'est l'instance de classe qui est retournée.
        Si attribut spécifié, alors c'est un dictionnaire représentant le joueur qui est retourné.
        Paramètres:
        - tournament_id: id du tournoi
        - attribute: facultatif, permet de pointer un attribut de la classe Tournament
        """
        if tournament_id == "":
            raise exceptions.BlankFieldException()
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        temp_dict = jsondb.getByQuery({"tournament_id": tournament_id})
        try:
            tournament_dict_from_json = temp_dict[0]
        except IndexError:
            raise exceptions.TournamentIdDoesNotExistsException()

        tournament_dict = {}
        unused_keys = ['id']
        for key, value in tournament_dict_from_json.items():
            if key not in unused_keys:
                if "date" in str(key):
                    tournament_dict[key] = get_back_stringdate_into_date(value)
                else:
                    tournament_dict[key] = value
        tournament = self.generate_tournament_from_json(tournament_dict)

        if attribute == "":
            return tournament
        else:
            if attribute in tournament.get_content().keys():
                return {"tournament_id": tournament_id, f"{attribute}": tournament.get_content()[attribute]}
            else:
                raise exceptions.AttributeDoesNotExistsException()
        return False

    def update_tournament_database_with_matches_scores(self, tournament: tournament_model.Tournament, match):
        """
        Description:
        Sert à mettre à jour la base de données Tournoi.
        On met à jour les scores des joueurs et leur adversaire.
        Si tous les matches sont joués le round est mis au statut terminé.
        Paramètres:
        - tournament: une instance de la classe Tournoi
        - match: une instance de la classe Match
        """
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        tournament_pysondb = jsondb.getByQuery({"tournament_id": tournament.tournament_id})[0]
        tournament_pysondb_id = tournament_pysondb["id"]
        current_round_id = tournament_pysondb["current_round_id"]
        round_matches_list = tournament_pysondb['rounds_list'][current_round_id - 1]['matches_list']
        for json_match in round_matches_list:
            j = match_model.Match(json_match)
            if isinstance(match[0][0], player_model.PlayerMatchModel):
                if match[0][0].ine in json_match[0][0]['ine']:
                    if match[0][1] == 1:
                        current_points = json_match[0][0]['points']
                        json_match[0][0]['points'] = current_points + 1
                        json_match[0][1] = 1
                    elif match[1][1] == 1:
                        current_points = json_match[1][0]['points']
                        json_match[1][0]['points'] = current_points + 1
                        json_match[1][1] = 1
                    else:
                        current_points = json_match[0][0]['points']
                        json_match[0][0]['points'] = current_points + 0.5
                        json_match[0][1] = 0.5
                        current_points = json_match[1][0]['points']
                        json_match[1][0]['points'] = current_points + 0.5
                        json_match[1][1] = 0.5
                    json_match[0][0]['opponents_faced'].append(match[1][0].ine)
                    json_match[1][0]['opponents_faced'].append(match[0][0].ine)
            else:
                m = ()
                p1 = player_model.PlayerMatchModel(**match[0][0])
                p1_pts = match[0][1]
                p1_list = [p1, p1_pts]
                p2 = player_model.PlayerMatchModel(**match[1][0])
                p2_pts = match[1][1]
                p2_list = [p2, p2_pts]
                m = ([p1_list], [p2_list])
                if p1.ine in json_match[0][0]['ine']:
                    if match[0][1] == 1:
                        current_points = json_match[0][0]['points']
                        json_match[0][0]['points'] = current_points + 1
                        json_match[0][1] = 1
                    else:
                        current_points = json_match[1][0]['points']
                        json_match[1][0]['points'] = current_points + 1
                        json_match[1][1] = 1
                    json_match[0][0]['opponents_faced'].append(f"{p2.ine}")
                    json_match[1][0]['opponents_faced'].append(f"{p1.ine}")

        current_match_id = tournament_pysondb['current_match_id']
        if current_match_id > len(round_matches_list) - 1:
            now = datetime.now()
            tournament_pysondb['rounds_list'][current_round_id - 1]['status'] = "ended"
            tournament_pysondb['rounds_list'][current_round_id - 1]['end_date'] = now.strftime("%Y-%m-%d %H:%M:%S")

        jsondb.updateById(tournament_pysondb_id, {'rounds_list': tournament_pysondb['rounds_list']})
        return True

    def create_tournament(self, view_on_player, new_tournament: tournament_model.Tournament):
        """
        Description:
        Fonction appelée par le biais de la vue dédiée.
        Elle récupère l'instance de classe Tournament, et met à jour de la base de données JSON correspondante.
        Paramètres:
        - new_tournament: une instance de classe Tournament
        """
        tournament_players_list = []
        if len(new_tournament.players_list) == 0:
            players_list = view_on_player.get_players_list()
        else:
            players_list = new_tournament.players_list

        for player in players_list:
            if player.status == "active":
                tournament_players_list.append(player.ine)

        if len(tournament_players_list) % 2 != 0:
            raise exceptions.OddPlayersListNumberException()
        new_tournament.players_list = tournament_players_list
        new_tournament.nb_players = len(tournament_players_list)
        jsondb = db.getDb("data/tournaments/tournaments_db.json")
        jsondb.add(new_tournament.get_tournament())
        return True
