from enum import Enum
from typing import List
from .shared_model import Information
from .round_model import Round


class Tournament:
    class Status(str, Enum):
        i = "in progress"
        c = "cancelled"
        e = "ended"
        p = "paused"
    tournament_id = Information()
    name = Information()
    location = Information()
    nb_rounds = Information()
    nb_players = Information()
    current_round_id = Information()
    current_match_id = Information()
    description = Information()
    status = Information()

    def __init__(self, **kw):
        self.tournament_id = kw["tournament_id"]
        self.name = kw["name"]
        self.location = kw["location"]
        self.start_date = kw["start_date"]
        self.end_date = kw["end_date"]
        self.nb_rounds = int(kw["nb_rounds"])
        self.players_list = []
        self.nb_players = 0
        self.rounds_list: List[Round] = []
        self.current_round_id = 1
        self.current_match_id = 1
        self.description = kw["description"]
        self.status = self.Status.i

    def refresh_nb_players(self):
        self.nb_players = len(self.players_list)

    def get_tournament(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": f"{self.start_date}",
            "end_date": f"{self.end_date}",
            "nb_rounds": self.nb_rounds,
            "nb_players": self.nb_players,
            "players_list": self.players_list,
            "rounds_list": self.rounds_list,
            "current_round_id": self.current_round_id,
            "current_match_id": self.current_match_id,
            "description": self.description,
            "status": self.status,
        }

    def get_content(self):
        return {
            "tournament_id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": f"{self.start_date}",
            "end_date": f"{self.end_date}",
            "nb_rounds": self.nb_rounds,
            "nb_players": self.nb_players,
            "players_list": self.players_list,
            "rounds_list": self.rounds_list,
            "current_round_id": self.current_round_id,
            "current_match_id": self.current_match_id,
            "description": self.description,
            "status": self.status,
        }
