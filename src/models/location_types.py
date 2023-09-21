from main import db

class LocationType(db.Model):

    # Data Table Name
    __tablename__ = "location_types"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    location_type = db.Column(db.String)

    