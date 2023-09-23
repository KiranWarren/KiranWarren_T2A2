from main import db

class Location(db.Model):

    # Data Table Name
    __tablename__ = "locations"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    name = db.Column(db.String(50), unique=True, nullable=False)
    admin_phone_number = db.Column(db.String(25), nullable=False)

    # Foreign Key Columns
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    location_type_id = db.Column(db.Integer, db.ForeignKey("location_types.id"), nullable=False)

    # Relationships
    country = db.relationship(
        "Country",
        back_populates="locations"
    )
    location_type = db.relationship(
        "LocationType",
        back_populates="locations"
    )
    users = db.relationship(
        "User",
        back_populates="location",
        cascade="all, delete"
    )

    