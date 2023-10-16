from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# we all the userloader to where we created our application
db = SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"] = "12345mine"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)


    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    # so I think I have this login view baecaue I am using auth.login

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
       db.create_all()

    return app
