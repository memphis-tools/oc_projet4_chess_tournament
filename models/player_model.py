from abc import ABC
from enum import Enum
from .shared_model import Information

LICENCE_VALIDITY_START = "2022-09-01"
LICENCE_VALIDITY_END = "2023-08-31"
PLAYER_CATEGORIES_DICT = {
    "petit poussin": {"code": "pPo", "min": "0", "max": "7"},
    "poussin": {"code": "Po", "min": "8", "max": "9"},
    "pupille": {"code": "Pu", "min": "10", "max": "11"},
    "benjamin": {"code": "Ben", "min": "12", "max": "13"},
    "minime": {"code": "Min", "min": "14", "max": "15"},
    "cadet": {"code": "Cad", "min": "16", "max": "17"},
    "junior": {"code": "Jun", "min": "18", "max": "19"},
    "sénior": {"code": "Sen", "min": "20", "max": "49"},
    "sénior plus": {"code": "Sen+", "min": "50", "max": "64"},
    "vétéran": {"code": "Vet", "min": "65", "max": "999"},
}


class Human(ABC):
    civility = Information()
    f_name = Information()
    l_name = Information()
    birth_date = Information()

    def __init__(self, *args, **kw):
        self.civility = kw["civility"]
        self.f_name = kw["f_name"].lower()
        self.l_name = kw["l_name"].lower()
        self.birth_date = kw["birth_date"]


class LicenceType(str, Enum):
    a = "A"
    b = "B"


class Licence:
    start_date = Information()
    end_date = Information()

    def __init__(self, **kw):
        self.type = eval(f"LicenceType.{kw['type']}")
        self.start_date = LICENCE_VALIDITY_START
        self.end_date = LICENCE_VALIDITY_END

    def __str__(self):
        return f"{self.type}"


class Player(Human):
    class Status(str, Enum):
        a = "active"
        i = "inactive"
        d = "archived"
    club_id = Information()
    ine = Information()
    subscribe_date = Information()
    points = Information()
    title = Information()
    status = Information()
    fullname = Information()

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.ine = kw["ine"]
        self.club_id = kw["club_id"]
        self.licence = Licence(type="a")
        self.category = PLAYER_CATEGORIES_DICT[kw["category"]]["code"]
        self.medical_certificate = True
        self.subscribe_date = kw["subscribe_date"]
        self.points = float(0.0)
        self.title = "candidat maitre"
        self.status = self.Status.a
        self.fullname = f"{self.l_name} {self.f_name}"
        self.opponents_faced = []

    def __str__(self):
        return self.ine

    def get_player(self):
        return {
            "civility": self.civility,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "birth_date": self.birth_date,
            "club_id": self.club_id,
            "ine": self.ine,
            "licence": f"{self.licence}",
            "category": self.category,
            "medical_certificate": self.medical_certificate,
            "subscribe_date": self.subscribe_date,
            "points": self.points,
            "title": self.title,
            "status": self.status,
            "fullname": self.fullname,
            "opponents_faced": self.opponents_faced,
        }

    def get_content(self):
        return {
            "civility": self.civility,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "birth_date": self.birth_date,
            "club_id": self.club_id,
            "ine": self.ine,
            "licence": f"{self.licence}",
            "category": self.category,
            "medical_certificate": self.medical_certificate,
            "subscribe_date": self.subscribe_date,
            "points": self.points,
            "title": self.title,
            "status": self.status,
            "fullname": self.fullname,
            "opponents_faced": self.opponents_faced,
        }

    def update_full_name(self):
        self.fullname = f"{self.l_name} {self.f_name}"


class PlayerMatchModel:
    def __init__(self, *args, **kw):
        self.ine = kw["ine"]
        self.points = float(kw["points"])
        self.opponents_faced = kw["opponents_faced"]
        self.fullname = kw["fullname"]

    def add_point(self, nb_point):
        self.points += nb_point

    def add_opponent(self, ine):
        self.opponents_faced.append(ine)

    def get_opponents(self):
        return self.opponents_faced

    def get_content(self):
        return {
            "ine": self.ine,
            "points": self.points,
            "opponents_faced": self.opponents_faced,
            "fullname": self.fullname,
        }

    def __iter__(self):
        yield from {
            "ine": self.ine,
            "points": self.points,
            "opponents_faced": self.opponents_faced,
            "fullname": self.fullname
        }.items()

    def __str__(self):
        return f"{dict(self)}"

    def __repr__(self):
        return self.__str__()
