from main import db

class Manufacture(db.Model):

    # Data Table Name
    __tablename__ = "manufactures"

    # Primary Keys
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), primary_key=True)

    # Columns
    price_estimate = db.Column(db.Float, nullable=False)
    id = db.Column(db.String, unique=True)

    # Foreign Key Columns
    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=False)

    # Relationships
    project = db.relationship(
        "Project",
        back_populates="manufactures"
    )
    location = db.relationship(
        "Location",
        back_populates="manufactures"
    )
    currency = db.relationship(
        "Currency",
        back_populates="manufactures"
    )
