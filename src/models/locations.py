from main import db

class Location(db.Model):

    # Data Table Name
    __tablename__ = "locations"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String)
    admin_phone_number = db.Column(db.String)

    