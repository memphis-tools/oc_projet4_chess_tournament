from enum import Enum
from .shared_model import Information


class Round:
    class Status(str, Enum):
        p = "in progress"
        c = "cancelled"
        n = "not started"
        e = "ended"
    tournament_id = Information()
    number = Information()
    status = Information()

    def __iter__(self):
        yield from {
            "tournament_id": self.tournament_id,
            "number": self.number,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches_list": self.matches_list,
            "name": self.name,
        }.items()

    def __init__(self, **kw):
        self.tournament_id = kw["tournament_id"]
        self.number = kw["number"]
        self.status = self.Status.n
        self.start_date = ""
        self.end_date = ""
        self.matches_list = []
        self.name = f"Round {self.number}"

    def get_matches_list(self):
        return self.matches_list

    def update_status(self, new_status):
        self.status = new_status

    def __str__(self):
        return f"{dict(self)}"

    def __repr__(self):
        return self.__str__()

    def get_round(self):
        return {
            "tournament_id": self.tournament_id,
            "number": self.number,
            "name": self.name,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches_list": self.matches_list,
        }

    def get_content(self):
        temp_tupple = []
        for m in self.matches_list:
            temp_l1 = []
            temp_l2 = []
            temp_l3 = []
            temp_l4 = []
            temp_l1.append(m[0][0].get_content())
            temp_l1.append(m[0][1])
            temp_l3.append(m[1][0].get_content())
            temp_l3.append(m[1][1])
            temp_l2.append(temp_l1)
            temp_l2.append(temp_l3)
            temp_tupple.append(temp_l2)

        return {
            "tournament_id": self.tournament_id,
            "number": self.number,
            "name": self.name,
            "status": self.status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches_list": tuple(temp_tupple),
        }
