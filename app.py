from flask import Flask, render_template, request, redirect, url_for, flash, abort
from jinja2 import TemplateNotFound
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "bizz_secret_key"

# ---------------------- MONGODB CONNECTION ----------------------
try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection test
    db = client["bizz_journey"]
    registered_users = db["registered_users"]  # Stores user registration
    login_logs = db["login_logs"]              # Stores login history
except Exception as e:
    print("⚠️ Could not connect to MongoDB:", e)
    exit(1)

# ---------------------- ALLOWED DATA ----------------------
ALLOWED_CITIES = ('hyderabad', 'bangalore', 'chennai')
ALLOWED_COMPANIES = {
    "hyderabad": ("bizcore", "technova"),
    "bangalore": ("infowise", "nexgen"),
    "chennai": ("techmahendra", "accenture")
}

# ---------------------- ROUTES ----------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    """Login page route"""
    # Check if no users exist → force redirect to register
    if registered_users.count_documents({}) == 0:
        flash("No users found. Please register first.", "info")
        return redirect(url_for('register'))

    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password cannot be empty.", "error")
            return redirect(url_for('login'))

        user = registered_users.find_one({"username": username})

        if user and check_password_hash(user["password"], password):
            # Log the successful login
            login_logs.insert_one({
                "username": username,
                "login_time": datetime.now()
            })

            flash("✅ Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("❌ Invalid username or password!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if request.method == 'POST':
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if not username or not password:
            flash("Username and password cannot be empty.", "error")
            return redirect(url_for('register'))

        existing_user = registered_users.find_one({"username": username})
        if existing_user:
            flash("⚠️ Username already exists. Please choose another.", "error")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        registered_users.insert_one({"username": username, "password": hashed_password})

        flash("🎉 Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/area')
def area():
    return render_template('area.html')


@app.route('/companies/<city>')
def companies(city):
    city = city.lower()
    if city not in ALLOWED_CITIES:
        abort(404)

    try:
        return render_template(f"companies_{city}.html")
    except TemplateNotFound:
        abort(404)


@app.route('/details/<company>')
def company_details(company):
    company = company.lower()

    found = any(company in companies for companies in ALLOWED_COMPANIES.values())
    if not found:
        abort(404)

    try:
        return render_template(f"details/{company}.html")
    except TemplateNotFound:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True)
