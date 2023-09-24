from main import db

class Drawing(db.Model):

    # Data Table Name
    __tablename__ = "drawings"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    drawing_number = db.Column(db.String(10), nullable=False)
    part_description = db.Column(db.Text, nullable=True)
    version = db.Column(db.Integer, nullable=True)
    last_modified = db.Column(db.DateTime)

    # Foreign Key Columns
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    # Relationships
    project = db.relationship(
        "Project",
        back_populates="drawings"
    )