from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize app
app = Flask(__name__)
app.config.from_object('config')

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import views
from app.controllers import default



