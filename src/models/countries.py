from main import db

class Country(db.Model):

    # Data Table Name
    __tablename__ = "countries"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    country = db.Column(db.String(25), unique=True, nullable=False)

    # Relationships
    locations = db.relationship(
        "Location",
        back_populates="country",
        cascade="all, delete"
    )

    