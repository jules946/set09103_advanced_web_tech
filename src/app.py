from flask import Flask, render_template
import os

# setting templates folder path
templates_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')

app = Flask(__name__, template_folder=templates_folder, static_folder=static_folder)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
