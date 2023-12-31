from main import db

class Project(db.Model):

    # Data Table Name
    __tablename__ = "projects"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    title = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    certification_number = db.Column(db.String(25), nullable=True)
    
    # Relationships
    drawings = db.relationship(
        "Drawing",
        back_populates="project",
        cascade="all, delete"
    )
    comments = db.relationship(
        "Comment",
        back_populates="project",
        cascade="all, delete"
    )
    manufactures = db.relationship(
        "Manufacture",
        back_populates="project",
        cascade="all, delete"
    )