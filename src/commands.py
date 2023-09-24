from main import db
from flask import Blueprint
import datetime

from models import Country, Currency, LocationType, Location, User, Project, Drawing, Comment

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
        admin_phone_number = "+614 555 555 55",
        country_id = 1,
        location_type_id = 1
    )

    loc2 = Location(
        name = "Aldruhn",
        admin_phone_number = "+614 666 666 66",
        country_id = 1,
        location_type_id = 2
    )

    loc3 = Location(
        name = "Gnisis",
        admin_phone_number = "+614 777 777 77",
        country_id = 2,
        location_type_id = 3
    )

    # Seed Locations
    db.session.add_all([loc1, loc2, loc3])
    db.session.commit()

    user1 = User(
        username = "ccosades",
        email_address = "ccosades@blades.com",
        position = "Grand Spymaster",
        is_admin = True,
        location_id = 1
    )

    user2 = User(
        username = "tsadus",
        email_address = "tsadus@genmerch.com",
        position = "Merchant",
        is_admin = False,
        location_id = 2
    )

    user3 = User(
        username = "ajira",
        email_address = "ajira@magesguild.com",
        position = "Associate",
        is_admin = False,
        location_id = 1
    )

    # Seed Users
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    proj1 = Project(
        title = "789C BTG Access System",
        published_date = "2014-01-22",
        description = "Bumper-to-ground access system for Caterpillar 789C.",
        certification_number = "S0004513"
    )

    proj2 = Project(
        title = "CAT MD6310 Feed Cyl Transport Frame",
        certification_number = "S0023546"
    )

    proj3 = Project(
        title = "RWG Stud Pressing Tool",
        description = "Suits 785, 789, 793 Std RWGs.",
        certification_number = "S0012344"
    )

    # Seed Projects
    db.session.add_all([proj1, proj2, proj3])
    db.session.commit()

    drw1 = Drawing(
        drawing_number = "41756",
        project_id = 1,
        part_description = "pin",
        version = 1,
        last_modified = datetime.datetime.now()
    )
    drw2 = Drawing(
        drawing_number = "41757",
        project_id = 1,
        part_description = "step asm",
        version = 1,
        last_modified = datetime.datetime.now()
    )
    drw3 = Drawing(
        drawing_number = "41758",
        project_id = 1,
        part_description = "stringer",
        version = 1,
        last_modified = datetime.datetime.now()
    )
    drw4 = Drawing(
        drawing_number = "39857",
        project_id = 2,
        part_description = "general assembly",
        version = 4,
        last_modified = datetime.datetime.now()
    )
    drw5 = Drawing(
        drawing_number = "40987",
        project_id = 2,
        last_modified = datetime.datetime.now()
    )
    drw6 = Drawing(
        drawing_number = "41999",
        project_id = 2,
        last_modified = datetime.datetime.now()
    )
    drw7 = Drawing(
        drawing_number = "41087",
        project_id = 2,
        last_modified = datetime.datetime.now()
    )
    drw8 = Drawing(
        drawing_number = "41088",
        project_id = 2,
        last_modified = datetime.datetime.now()
    )
    drw9 = Drawing(
        drawing_number = "52321",
        project_id = 3,
        part_description = "tool",
        version = 2,
        last_modified = datetime.datetime.now()
    )

    # Seed Drawings
    db.session.add_all([drw1, drw2, drw3, drw4, drw5, drw6, drw7, drw8, drw9])
    db.session.commit()

    cmnt1 = Comment(
        project_id = 1,
        user_id = 2,
        comment = "Does this design suit the 789D models?",
        when_created = datetime.datetime.now()
    )
    cmnt2 = Comment(
        project_id = 1,
        user_id = 1,
        comment = "Yes, this design should suit the 789D's.",
        when_created = datetime.datetime.now()
    )
    cmnt3 = Comment(
        project_id = 1,
        user_id = 2,
        comment = "Thanks for clearing that up.",
        when_created = datetime.datetime.now()
    )
    cmnt4 = Comment(
        project_id = 2,
        user_id = 3,
        comment = "Can this transport frame be transported on a standard 12m trailer?",
        when_created = datetime.datetime.now()
    )
    cmnt5 = Comment(
        project_id = 2,
        user_id = 1,
        comment = "No, an extended trailer is required to transport this component/frame.",
        when_created = datetime.datetime.now()
    )

    # Seed Comments
    db.session.add_all([cmnt1, cmnt2, cmnt3, cmnt4, cmnt5])
    db.session.commit()

    print("Tables have been seeded.")
