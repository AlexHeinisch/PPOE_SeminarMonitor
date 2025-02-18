from typing import List

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pg_dsn: PostgresDsn = 'postgres://user:pass@localhost:5432/foobar'

    BASE_URL: str = 'https://app1.edoobox.com/de/ppoe/'

    locations: List[str] = [
        'Vorarlberg',
        'Tirol',
        'Salzburg',
        'Oberösterreich',
        'Niederösterreich',
        'Wien',
        'Burgenland',
        'Steiermark',
        'Bundesverband'
    ]
