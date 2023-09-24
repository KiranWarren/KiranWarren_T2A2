from main import db
from sqlalchemy_utils import EmailType

class User(db.Model):

    # Data Table Name
    __tablename__ = "users"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    username = db.Column(db.String(25), unique=True, nullable=False)
    email_address = db.Column(EmailType, unique=True, nullable=False)
    position = db.Column(db.String(25), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign Key Columns
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)

    # Relationships
    location = db.relationship(
        "Location",
        back_populates="users"
    )
    comments = db.relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete"
    )
