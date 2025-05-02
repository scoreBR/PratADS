from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PPADS.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # Configuração do Flask-Migrate
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import Usuario

    # Função para carregar o usuário
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    # Registra os blueprints
    from .auth import auth
    from .views import views
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    return app