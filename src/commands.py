from flask import Blueprint
from flask_bcrypt import Bcrypt
import datetime

from main import db
from models import Country, Currency, LocationType, Location, User, Project, Drawing, Comment, Manufacture

bcrypt = Bcrypt()
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
        country = "Australia"
    )

    ctry2 = Country(
        country = "Indonesia"
    )

    ctry3 = Country(
        country = "Canada"
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
        currency_abbr = "IDR"
    )

    curr3 = Currency(
        currency_abbr = "CAD"
    )
        
    curr4 = Currency(
        currency_abbr = "USD"
    )

    # Seed supporting entities
    db.session.add_all([ctry1, ctry2, ctry3, loc_type1, loc_type2, loc_type3, curr1, curr2, curr3, curr4])
    db.session.commit()

    loc1 = Location(
        name = "Balmora",
        admin_phone_number = "+614 555 555 55",
        country_id = 1,
        location_type_id = 1
    )

    loc2 = Location(
        name = "Ald'ruhn",
        admin_phone_number = "+614 666 666 66",
        country_id = 1,
        location_type_id = 2
    )

    loc3 = Location(
        name = "Gnisis",
        admin_phone_number = "+614 777 777 77",
        country_id = 1,
        location_type_id = 3
    )

    loc4 = Location(
        name = "Seyda Neen",
        admin_phone_number = "+625 487 434 43",
        country_id = 2,
        location_type_id = 1
    )

    loc5 = Location(
        name = "Khuul",
        admin_phone_number = "+625 888 888 69",
        country_id = 2,
        location_type_id = 3
    )

    loc6 = Location(
        name = "Sadrith Mora",
        admin_phone_number = "+1250 555 0199",
        country_id = 3,
        location_type_id = 2
    )

    loc7 = Location(
        name = "Vivec",
        admin_phone_number = "+1875 900 0001",
        country_id = 3,
        location_type_id = 3
    )

    # Seed Locations
    db.session.add_all([loc1, loc2, loc3, loc4, loc5, loc6, loc7])
    db.session.commit()

    user1 = User(
        username = "ccosades",
        email_address = "ccosades@blades.com",
        position = "Mechanical Engineer",
        password = bcrypt.generate_password_hash("blades4ever").decode("utf-8"),
        is_admin = True,
        location_id = 1
    )

    user2 = User(
        username = "tsadus",
        email_address = "tsadus@genmerch.com",
        position = "Maintenance Superintendent",
        password = bcrypt.generate_password_hash("justice4juib").decode("utf-8"),
        is_admin = False,
        location_id = 2
    )

    user3 = User(
        username = "ajira",
        email_address = "ajira@magesguild.com",
        position = "Fabrication Supervisor",
        password = bcrypt.generate_password_hash("alchemist4").decode("utf-8"),
        is_admin = False,
        location_id = 1
    )

    user4 = User(
        username = "lvarro",
        email_address = "larrius.varro@legion.com",
        position = "Asset Engineer",
        password = bcrypt.generate_password_hash("byanymeans").decode("utf-8"),
        is_admin = True,
        location_id = 3
    )

    user5 = User(
        username = "sgravius",
        email_address = "sgravius@legion.com",
        position = "Workshop Supervisor",
        password = bcrypt.generate_password_hash("ahyesyoumustbe").decode("utf-8"),
        is_admin = False,
        location_id = 4
    )

    user6 = User(
        username = "arrille",
        email_address = "arrille@tradehouse.com",
        position = "Maintenance Manager",
        password = bcrypt.generate_password_hash("hideindatrunk5").decode("utf-8"),
        is_admin = False,
        location_id = 5
    )

    user7 = User(
        username = "prielle",
        email_address = "phane@cornerclub.com",
        position = "Mechanical Engineer",
        password = bcrypt.generate_password_hash("savant952").decode("utf-8"),
        is_admin = True,
        location_id = 4
    )

    user8 = User(
        username = "rathrys",
        email_address = "ranis@magesguild.com",
        position = "Asset Specialist",
        password = bcrypt.generate_password_hash("alteration4life").decode("utf-8"),
        is_admin = False,
        location_id = 6
    )

    user9 = User(
        username = "amantiti",
        email_address = "a.mantiti@mantitimining.com",
        position = "Maintenance Superintendent",
        password = bcrypt.generate_password_hash("moneyyyyyy").decode("utf-8"),
        is_admin = False,
        location_id = 7
    )

    user10 = User(
        username = "ehlaalu",
        email_address = "eno@househlaalu.com",
        position = "Diesel Fitter",
        password = bcrypt.generate_password_hash("password#4").decode("utf-8"),
        is_admin = False,
        location_id = 7
    )

    # Seed Users
    db.session.add_all([user1, user2, user3, user4, user5, user6, user7, user8, user9, user10])
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

    proj4 = Project(
        title = "789C Chassis Rails",
        published_date = "2005-05-01",
        description = "Handrails for safe access on 789C chassis.",
        certification_number = "S76453"
    )

    proj5 = Project(
        title = "R996 Bucket Cylinder Rock Guards",
        published_date = "2023-01-10",
        description = "Suits both left & right cylinders. Bolt-on design."
    )

    proj6 = Project(
        title = "OHT RWG Disassembly Stand",
        description = "Rotating disassembly/assembly stand.",
        certification_number = "S471633"
    )

    proj7 = Project(
        title = "Pump Drive Box Rotator",
        description = "Worktable mounted rotator for disassembly and assembly."
    )

    proj8 = Project(
        title = "793F Brake Accumulator Set Transport Frame",
        description = "Suits set of 3 x 793F brake accumulators.",
        certification_number = "S8789422"
    )

    # Seed Projects
    db.session.add_all([proj1, proj2, proj3, proj4, proj5, proj6, proj7, proj8])
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

    drw10 = Drawing(
        drawing_number = "45643",
        project_id = 4,
        last_modified = datetime.datetime.now()
    )

    drw11 = Drawing(
        drawing_number = "54433",
        project_id = 5,
        part_description = "General Assembly",
        version = 4,
        last_modified = datetime.datetime.now()
    )

    drw12 = Drawing(
        drawing_number = "42329",
        project_id = 6,
        last_modified = datetime.datetime.now()
    )

    drw13 = Drawing(
        drawing_number = "56466",
        project_id = 7,
        last_modified = datetime.datetime.now()
    )

    drw14 = Drawing(
        drawing_number = "45634",
        project_id = 8,
        part_description = "Frame",
        version = 1,
        last_modified = datetime.datetime.now()
    )

    drw15 = Drawing(
        drawing_number = "45635",
        project_id = 8,
        part_description = "Supports",
        version = 1,
        last_modified = datetime.datetime.now()
    )

    # Seed Drawings
    db.session.add_all([drw1, drw2, drw3, drw4, drw5, drw6, drw7, drw8, drw9, drw10, drw11, drw12, drw13, drw14, drw15])
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
    cmnt6 = Comment(
        project_id = 8,
        user_id = 5,
        comment = "Will this frame fit steering accumulators?",
        when_created = datetime.datetime.now()
    )
    cmnt7 = Comment(
        project_id = 8,
        user_id = 7,
        comment = "No, they would be too long for this frame.",
        when_created = datetime.datetime.now()
    )

    # Seed Comments
    db.session.add_all([cmnt1, cmnt2, cmnt3, cmnt4, cmnt5, cmnt6, cmnt7])
    db.session.commit()

    manu1 = Manufacture(
        location_id = 1,
        project_id = 1,
        price_estimate = 22000,
        currency_id = 1
    )
    manu2 = Manufacture(
        location_id = 1,
        project_id = 2,
        price_estimate = 14000,
        currency_id = 1
    )
    manu3 = Manufacture(
        location_id = 1,
        project_id = 3,
        price_estimate = 2324.50,
        currency_id = 1
    )
    manu4 = Manufacture(
        location_id = 1,
        project_id = 7,
        price_estimate = 3500.00,
        currency_id = 1
    )
    manu5 = Manufacture(
        location_id = 1,
        project_id = 8,
        price_estimate = 1523.57,
        currency_id = 1
    )
    manu6 = Manufacture(
        location_id = 2,
        project_id = 1,
        price_estimate = 150000000,
        currency_id = 2
    )
    manu7 = Manufacture(
        location_id = 2,
        project_id = 4,
        price_estimate = 49810000,
        currency_id = 2
    )
    manu8 = Manufacture(
        location_id = 2,
        project_id = 5,
        price_estimate = 300000000,
        currency_id = 2
    )
    manu9 = Manufacture(
        location_id = 2,
        project_id = 6,
        price_estimate = 120000000,
        currency_id = 2
    )
    manu10 = Manufacture(
        location_id = 2,
        project_id = 8,
        price_estimate = 12000000,
        currency_id = 2
    )

    # Seed Manufactures
    db.session.add_all([manu1, manu2, manu3, manu4, manu5, manu6, manu7, manu8, manu9, manu10])
    db.session.commit()

    print("Tables have been seeded.")
