"""All Flask extensions live here — created once, attached via init_app() in the factory.

Why a separate file: avoids circular imports. Models import `db` from here,
routes import `bcrypt` from here — and this file imports nothing from the app itself.
"""

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
socketio = SocketIO()
cors = CORS()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)