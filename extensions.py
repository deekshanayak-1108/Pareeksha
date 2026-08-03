from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instantiate the extensions unbound to the app to prevent circular imports
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
