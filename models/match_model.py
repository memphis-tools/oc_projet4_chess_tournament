import json
from json import JSONEncoder
from .player_model import PlayerMatchModel


class MatchEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class Match:
    def __init__(self, tupple_match):
        self.match = tupple_match

    def __str__(self):
        return f"{self.match}"

    def __repr__(self):
        return self.__str__()

    def get_content(self):
        return MatchEncoder().encode(self.match)

    def add_player_point(self, nb_player, point):
        m = ""
        if not isinstance(self.match[nb_player - 1][0], PlayerMatchModel):
            m = PlayerMatchModel(**self.match[nb_player - 1][0])
            m.add_point(point)
            self.match[nb_player - 1][1] = point
        else:
            self.match[nb_player - 1][0].add_point(point)
            self.match[nb_player - 1][1] = point

    def delete_player_point(self, nb_player, point):
        self.match[0][nb_player - 1][0].points -= point

    def get_match_point_to_add_or_delete(self):
        p1_score = self.match[0][1]
        p2_score = self.match[1][1]
        return (p1_score, p2_score)

    def get_player_1(self):
        if isinstance(self.match, tuple):
            return self.match[0][0]
        elif isinstance(self.match, list):
            return self.match[0][0]
        else:
            return json.loads(self.match)[0][0]

    def get_player_2(self):
        if isinstance(self.match, tuple):
            return self.match[1][0]
        elif isinstance(self.match, list):
            return self.match[1][0]
        else:
            return json.loads(self.match)[1][0]

    def get_players_ine(self):
        ine_players_list = []
        p1 = self.get_player_1()
        if isinstance(p1, PlayerMatchModel):
            ine_players_list.append(self.get_player_1().ine)
            ine_players_list.append(self.get_player_2().ine)
        else:
            ine_players_list.append(self.get_player_1()['ine'])
            ine_players_list.append(self.get_player_2()['ine'])
        return ine_players_list

    def get_player_by_ine(self, ine):
        p1 = self.get_player_1()
        p2 = self.get_player_2()
        if p1['ine'] == ine:
            return p1
        elif p2['ine'] == ine:
            return p2
        return False

    def is_match_scored(self):
        players_list = self.match
        if players_list[0][1] == 0 and players_list[1][1] == 0:
            return False
        return True
