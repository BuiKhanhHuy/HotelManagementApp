from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)

app.secret_key = 'Od\x01\xb3\xce\x12(\xfc\xe4\x10Q\x04\x0c\xa8\x8dX'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456789@localhost/hoteldb?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['FLASK_ADMIN_SWATCH'] = 'Simplex'
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True

app.config['CUSTOMER_PAGE_SIZE'] = 6
app.config['EMPLOYEE_FIND_PAGE_SIZE'] = 5
app.config['COMMENT_SIZE'] = 5

cloudinary.config(
    cloud_name='dl6artkyb',
    api_key='377958885536713',
    api_secret='g0XCOiAv3pIpP1uFdYbz_Zwa6Sg'
)


db = SQLAlchemy(app=app)
login = LoginManager(app=app)


babel = Babel(app=app)


@babel.localeselector
def get_locale():
    return 'vi'
