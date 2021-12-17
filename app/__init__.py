from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel


app = Flask(__name__)

app.secret_key = 'Od\x01\xb3\xce\x12(\xfc\xe4\x10Q\x04\x0c\xa8\x8dX'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456789@localhost/hoteldb?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['FLASK_ADMIN_SWATCH'] = 'Materia'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True


db = SQLAlchemy(app=app)


babel = Babel(app=app)


@babel.localeselector
def get_locale():
    return 'vi'
