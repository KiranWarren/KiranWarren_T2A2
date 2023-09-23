from main import db

class LocationType(db.Model):

    # Data Table Name
    __tablename__ = "location_types"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    location_type = db.Column(db.String(25), unique=True, nullable=False)

    # Relationships
    locations = db.relationship(
        "Location",
        back_populates="location_type",
        cascade="all, delete"
    )