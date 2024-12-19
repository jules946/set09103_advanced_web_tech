from flask import render_template

from src import create_app

# create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=False)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        'error.html',
        code=404,
        message="Page Not Found",
        description="The page you're looking for doesn't exist or has been moved."
    ), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        'error.html',
        code=500,
        message="Internal Server Error",
        description="Something went wrong on our end. Please try again later."
    ), 500