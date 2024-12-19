from src import create_app, db
from sqlalchemy import text


def init_db():
    app = create_app()
    with app.app_context():

        # create a connection to execute raw SQL
        with db.engine.connect() as connection:
            # disable foreign key checks temporarily
            connection.execute(text("DROP SCHEMA public CASCADE;"))
            connection.execute(text("CREATE SCHEMA public;"))
            connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))

        # Create all tables
        db.create_all()

        print("Database initialized!")


if __name__ == "__main__":
    init_db()