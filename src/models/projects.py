from main import db

class Project(db.Model):

    # Data Table Name
    __tablename__ = "projects"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    title = db.Column(db.String(50), nullable=False)
    published_date = db.Column(db.Date)
    description = db.Column(db.Text)
    certification_number = db.Column(db.String(25))