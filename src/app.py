from flask import render_template

from src import create_app

# create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
