from enum import Enum
from .shared_model import Information


class Club:
    class Status(str, Enum):
        a = "active"
        i = "inactive"
        d = "archived"
    club_id: Information()
    name = Information()
    email = Information()
    website = Information()
    status = Information()

    def __init__(self, **kw):
        self.club_id = kw["club_id"]
        self.name = kw["name"]
        self.email = kw["email"]
        self.website = kw["website"]
        self.status = self.Status.a

    def get_club(self):
        return {
            "club_id": self.club_id,
            "name": self.name,
            "email": self.email,
            "website": self.website,
            "status": self.status,
        }

    def get_content(self):
        return {
            "club_id": self.club_id,
            "name": self.name,
            "email": self.email,
            "website": self.website,
            "status": self.status,
        }
