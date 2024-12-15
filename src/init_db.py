from src import create_app, db


def init_db():
    app = create_app()
    with app.app_context():
        # import models
        from src.models import User

        # drop all tables first (don't do this in production :))
        db.drop_all()

        # create all tables
        db.create_all()

        print("Database initialized!")


if __name__ == "__main__":
    init_db()