from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)

# Inject current year for footer
@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}

# Database model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)  # Added clicks column

    def __init__(self, original_url, short_code):
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = 0

# Generate short code
def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        if not URL.query.filter_by(short_code=code).first():
            return code

# Landing page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original_url = request.form.get("original_url")
        if not original_url:
            flash("Please enter a URL.", "danger")
            return redirect(url_for("home"))

        existing = URL.query.filter_by(original_url=original_url).first()
        if existing:
            short_url = request.host_url + existing.short_code
            return render_template("result.html", short_url=short_url)

        short_code = generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        short_url = request.host_url + short_code
        return render_template("result.html", short_url=short_url)

    return render_template("index.html")

# Redirect short code
@app.route("/<short_code>")
def redirect_short_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first_or_404()
    url_entry.clicks += 1  # Increment click count
    db.session.commit()
    return redirect(url_entry.original_url)

@app.route("/history")
def history():
    urls = URL.query.all()
    return render_template("history.html", urls=urls)

# Initialize DB
if __name__ == "__main__":
    if not os.path.exists("urls.db"):
        with app.app_context():
            db.create_all()
    app.run(debug=True)