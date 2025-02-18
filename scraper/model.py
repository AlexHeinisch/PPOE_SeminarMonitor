from enum import Enum

from pydantic import BaseModel, HttpUrl

class SeminarOrganisation(str, Enum):
    WIEN = "Wien"
    VORARLBERG = "Vorarlberg"
    TIROL = "Tirol"
    SALZBURG = "Salzburg"
    OBEROESTERREICH = "Oberösterreich"
    NIEDEROESTERREICH = "Niederösterreich"
    BURGENLAND = "Burgenland"
    STEIERMARK = "Steiermark"
    BUNDESVERBAND = "Bundesverband"

class SeminarCategory(str, Enum):
    JUGENDLEITUNG_EINSTIEGSPHASE = "Jugendleitung/Einstiegsphase"
    JUGENDLEITUNG_ERFAHRUNGSPHASE = "Jugendleitung/Erfahrungsphase"
    JUGENDLEITUNG_VERTIEFUNGSPHASE = "Jugendleitung/Vertiefungsphase"
    TEAMLEITUNG = "Teamleitung"
    WEITERBILDUNG = "Weiterbildung"
    GRUPPENLEITUNG = "Gruppenleitung"
    WOODBADGE = "Woodbadge"
    TRAINERINNEN = "TrainerInnen"

class SeminarStatus(str, Enum):
    OPEN_UNCERTAIN = "OPEN_UNCERTAIN"
    FULL_WAITING_LIST_OPEN = "FULL_WAITING_LIST_OPEN"
    OPEN_GUARANTEED = "OPEN_GUARANTEED"
    FULL_REGISTRATION_OVER = "FULL_REGISTRATION_OVER"
    UNKNOWN = "UNKNOWN"

class ScrapedSeminar(BaseModel):
    title: str
    event_url: HttpUrl
    date: str
    location: str
    price: str
    registration_deadline: str
    available_slots: int
    details_url: HttpUrl
    status: SeminarStatus
    organisation: SeminarOrganisation
    category: SeminarCategory