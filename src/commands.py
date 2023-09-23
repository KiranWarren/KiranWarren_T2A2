from main import db
from flask import Blueprint

from models import Country, Currency, LocationType, Location

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables have been created.")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables have been dropped.")

@db_commands.cli.command("seed")
def seed_db():

    ctry1 = Country(
        country = "Morrowind"
    )

    ctry2 = Country(
        country = "Elsweyr"
    )

    ctry3 = Country(
        country = "Hammerfell"
    )

    loc_type1 = LocationType(
        location_type = "Workshop"
    )

    loc_type2 = LocationType(
        location_type = "Office"
    )

    loc_type3 = LocationType(
        location_type = "Mine Site"
    )

    curr1 = Currency(
        currency_abbr = "AUD"
    )

    curr2 = Currency(
        currency_abbr = "USD"
    )
        
    curr3 = Currency(
        currency_abbr = "IDR"
    )

    # Seed supporting entities
    db.session.add_all([ctry1, ctry2, ctry3, loc_type1, loc_type2, loc_type3, curr1, curr2, curr3])
    db.session.commit()

    loc1 = Location(
        name = "Balmora",
        admin_phone_number = "+614 555 555 55"
    )

    loc2 = Location(
        name = "Aldruhn",
        admin_phone_number = "+614 666 666 66"
    )

    loc3 = Location(
        name = "Gnisis",
        admin_phone_number = "+614 777 777 77"
    )

    # Seed Locations
    db.session.add_all([loc1, loc2, loc3])
    db.session.commit()

    print("Tables have been seeded.")
