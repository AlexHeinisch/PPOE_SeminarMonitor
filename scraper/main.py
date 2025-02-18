import asyncio
from typing import List

import aiohttp
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from config import Settings
from model import ScrapedSeminar, SeminarStatus, SeminarOrganisation, SeminarCategory
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, Boolean

settings = Settings()

# Create Async Engine and Session
engine = create_async_engine(settings.pg_dsn.__str__(), echo=False, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base model for SQLAlchemy
Base = declarative_base()


class Seminar(Base):
    __tablename__ = "seminars"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    event_url = Column(String, unique=True, nullable=False)  # Unique to prevent duplicates
    date = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price = Column(String, nullable=False)
    registration_deadline = Column(String, nullable=False)
    available_slots = Column(Integer, nullable=False)
    details_url = Column(String, unique=True, nullable=False)  # Unique to prevent duplicates
    status = Column(SQLEnum(SeminarStatus), nullable=False)
    organisation = Column(SQLEnum(SeminarOrganisation), nullable=False)
    category = Column(SQLEnum(SeminarCategory), nullable=False)
    active = Column(Boolean, default=True, nullable=False)


def parse_status(column) -> SeminarStatus:
    icon = column.find("span")
    if icon:
        class_list = icon.get("class", [])
        if "glyphicon-ok-circle" in class_list:
            return SeminarStatus.OPEN_UNCERTAIN
        elif "glyphicon-hourglass" in class_list:
            return SeminarStatus.FULL_WAITING_LIST_OPEN
        elif "glyphicon-ok-sign" in class_list:
            return SeminarStatus.OPEN_GUARANTEED
        elif "glyphicon-ban-circle" in class_list:
            return SeminarStatus.FULL_REGISTRATION_OVER
    return SeminarStatus.UNKNOWN


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Run database initialization
asyncio.run(init_db())


async def fetch_page(session, url: str) -> str:
    try:
        async with session.get(url) as response:
            if response.status == 404:
                print(f"Page not found: {url}")
                return ""
            elif response.status != 200:
                print(f"Error {response.status} while fetching {url}")
                return ""
            return await response.text()
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return ""


async def scrape_seminars_by_org_and_category(session, organisation: SeminarOrganisation, category: SeminarCategory) -> \
        List[ScrapedSeminar]:
    url = f'{settings.BASE_URL}{organisation.value}/{category.value}'
    print(f'Trying to scrape all seminars from "{url}"...')

    html = await fetch_page(session, url)
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    seminar_rows = soup.find_all('tr', class_='angebot_row')
    seminars: List[ScrapedSeminar] = []

    for row in seminar_rows:
        columns = row.find_all("td")
        try:
            seminar = ScrapedSeminar(
                title=columns[0].find("a").text.strip(),
                event_url=columns[0].find("a")["href"],
                date=columns[1].text.strip(),
                location=columns[2].text.strip(),
                price=columns[3].text.strip(),
                registration_deadline=columns[4].text.strip(),
                available_slots=int(columns[5].text.strip()),
                status=parse_status(columns[6]),
                organisation=organisation,
                category=category,
                details_url=columns[7].find("a")["href"]
            )
            seminars.append(seminar)
        except Exception as e:
            print(f"Error parsing a row: {e}")
    return seminars


async def scrape_all_seminars():
    all_seminars = []
    async with aiohttp.ClientSession() as session:
        tasks = [
            scrape_seminars_by_org_and_category(session, org, cat)
            for cat in SeminarCategory for org in SeminarOrganisation
        ]
        results = await asyncio.gather(*tasks)
        for seminars in results:
            all_seminars.extend(seminars)

    return all_seminars


async def save_seminars_to_db(seminars: list[Seminar]):
    async with async_session() as session:
        # Fetch all existing seminars from the database
        existing_seminars = await session.execute(select(Seminar))
        existing_seminars = {s.event_url: s for s in existing_seminars.scalars().all()}

        # Create a set of new seminar URLs for comparison
        new_seminar_urls = {seminar.event_url for seminar in seminars}

        for seminar in seminars:
            if seminar.event_url in existing_seminars:
                # Seminar exists → Update properties and set active=True
                existing_seminar = existing_seminars[seminar.event_url]
                existing_seminar.title = seminar.title
                existing_seminar.date = seminar.date
                existing_seminar.location = seminar.location
                existing_seminar.price = seminar.price
                existing_seminar.registration_deadline = seminar.registration_deadline
                existing_seminar.available_slots = seminar.available_slots
                existing_seminar.details_url = seminar.details_url
                existing_seminar.status = seminar.status
                existing_seminar.active = True  # Mark as active
            else:
                # New seminar → Insert it
                session.add(seminar)

        # Mark missing seminars as inactive (active=False)
        for url, seminar in existing_seminars.items():
            if url not in new_seminar_urls:
                seminar.active = False  # Mark as inactive

        await session.commit()


def to_seminar_entities(scraped_seminars: List[ScrapedSeminar]) -> List[Seminar]:
    return [Seminar(
        title=seminar.title,
        event_url=seminar.event_url,
        date=seminar.date,
        location=seminar.location,
        price=seminar.price,
        registration_deadline=seminar.registration_deadline,
        available_slots=seminar.available_slots,
        details_url=seminar.details_url,
        status=seminar.status,
        organisation=seminar.organisation,
        category=seminar.category
    ) for seminar in scraped_seminars]


# Run the scraper
if __name__ == "__main__":
    scraped_data = asyncio.run(scrape_all_seminars())
    seminar_entities = to_seminar_entities(scraped_data)
    asyncio.run(save_seminars_to_db(seminar_entities))
