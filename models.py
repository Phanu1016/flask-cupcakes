from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

def connect_database(app):
    """ Connect to database """
    database.app = app
    database.init_app(app)


class Cupcake(database.Model):
    """ Cupcake model """
    __tablename__ = 'cupcakes'

    id = database.Column(database.Integer, nullable=False, primary_key=True, autoincrement=True)

    flavor = database.Column(database.Text, nullable=False)

    size = database.Column(database.Text, nullable=False)

    rating = database.Column(database.Float, nullable=False, default=0)

    image = database.Column(database.Text, nullable=False, default="https://tinyurl.com/demo-cupcake")


