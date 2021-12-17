from app import app
from flask import render_template, request, redirect, url_for
from app.admin import *
from app.models import *


@app.route("/")
def index():
    return render_template('customer/index.html')


if __name__ == "__main__":
    app.run(debug=True)
