from main import db

class Currency(db.Model):

    # Data Table Name
    __tablename__ = "currencies"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    currency = db.Column(db.String)

    