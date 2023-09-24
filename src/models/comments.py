from main import db

class Comment(db.Model):

    # Data Table Name
    __tablename__ = "comments"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    comment = db.Column(db.Text, nullable=False)
    when_created = db.Column(db.DateTime)
    last_edited = db.Column(db.DateTime)

    # Foreign Key Columns
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relationships
    project = db.relationship(
        "Project",
        back_populates="comments"
    )
    user = db.relationship(
        "User",
        back_populates="comments"
    )

    