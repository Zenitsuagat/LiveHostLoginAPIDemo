from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask import render_template

load_dotenv()

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------
# USER MODEL
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# ----------------------
# SIGNUP API
# ----------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing fields"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Signup successful"}), 201

# ----------------------
# LOGIN API
# ----------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        return jsonify({
            "message": "Login successful",
            "user_id": user.id
        })
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ----------------------
# USER DETAILS API
# ----------------------
@app.route('/userdetails', methods=['GET'])
def user_details():
    username = request.args.get('username')

    if not username:
        return jsonify({"message": "Username required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username
    })

# ----------------------
# ROOT TEST
# ----------------------
@app.route('/')
def home():
    return render_template('index.html')

# ----------------------
# RUN
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)