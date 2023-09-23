from main import db

class Currency(db.Model):

    # Data Table Name
    __tablename__ = "currencies"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Columns
    currency_abbr = db.Column(db.String(3), unique=True, nullable=False)

    