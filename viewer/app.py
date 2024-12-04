from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
from pymongo import MongoClient
import gridfs
from bson import ObjectId  # Import ObjectId for MongoDB ObjectID manipulation
from datetime import datetime

from flask import Flask, request, jsonify, render_template, redirect, url_for, Response, session, flash
from flask_bcrypt import Bcrypt
# Initialize Flask-Bcrypt
app = Flask(__name__)
import secrets
app.secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal secret key

bcrypt = Bcrypt(app)

# Replace with your MongoDB Atlas connection string
MONGO_URI = ""

# Initialize the MongoDB client and GridFS
client = MongoClient(MONGO_URI)
db = client["gestures"]  # Use the gestures database
fs = gridfs.GridFS(db)   # Initialize GridFS for file storage

# Example structure for the gestures collection
gestures_collection = db["gestures"]


# Database for user management
user_db = client["user_management"]
users_collection = user_db["users"]  # Collection for user authentication

@app.route('/')
def home():
    return render_template('home.html')  # Use a proper template for the homepage




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for('signup'))

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new contributor document
        new_contributor = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "contributor"  # Set role explicitly to "contributor"
        }

        # Insert the new contributor into the database
        users_collection.insert_one(new_contributor)

        flash("Signup successful! Please log in to start contributing.", "success")
        return redirect(url_for('login'))  # Redirect to the login page
    
    # Render the contributor-specific signup page
    return render_template('signup.html')





@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user in the database
        user = users_collection.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):
            # Store user information in session (including role)
            session['user_id'] = str(user["_id"])
            session['user_role'] = user["role"]  # Store the role

            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')




# Sample categories for gestures
categories = [
    {"name": "Computer", "icon": "💻"},
    {"name": "Kitchen", "icon": "🍴"},
    {"name": "Transportation", "icon": "🚗"},
    {"name": "Animals", "icon": "🐾"},
    {"name": "Health", "icon": "🏥"},
    {"name": "Nature", "icon": "🌳"},
    {"name": "Education", "icon": "📚"},
    {"name": "Sports", "icon": "⚽"},
    {"name": "Music", "icon": "🎵"},
    {"name": "Clothing", "icon": "👗"},
    {"name": "Emotions", "icon": "😊"},
    {"name": "Food", "icon": "🍕"},
    {"name": "Time", "icon": "⏰"},
    {"name": "Weather", "icon": "🌤️"},
    {"name": "Colors", "icon": "🎨"},
    {"name": "Hobbies", "icon": "🎨"},
    {"name": "Tools", "icon": "🛠️"},
    {"name": "Furniture", "icon": "🪑"},
    {"name": "Body Parts", "icon": "🖐️"},
    {"name": "Jobs", "icon": "👨‍💼"}
]


@app.route('/viewer', methods=['GET'])
def viewer_dashboard():
    search_query = request.args.get('q', '')  # Handle search functionality
    # Mock data for gestures (you can replace it with dynamic data later)
    gestures = [
        {"name": "Laptop", "category": "Computer"},
        {"name": "Frying Pan", "category": "Kitchen"},
        {"name": "Car", "category": "Transportation"},
        {"name": "Dog", "category": "Animals"},
        {"name": "Doctor", "category": "Health"},
    ]

    # Filter gestures based on search query
    if search_query:
        gestures = [g for g in gestures if search_query.lower() in g['name'].lower()]

    return render_template('viewer_dashboard.html', categories=categories, gestures=gestures, search_query=search_query)


@app.route('/category/<string:category_name>')
def category_gestures(category_name):
    # Get the page number from query parameters, default is 1
    page = int(request.args.get('page', 1))
    gestures_per_page = 10

    # Fetch gestures from the MongoDB collection
    gestures = gestures_collection.find({"category": category_name}).skip((page - 1) * gestures_per_page).limit(gestures_per_page)
    total_gestures = gestures_collection.count_documents({"category": category_name})

    return render_template(
        'category_gestures.html',
        category_name=category_name,
        gestures=list(gestures),
        total_pages=(total_gestures // gestures_per_page) + (1 if total_gestures % gestures_per_page > 0 else 0),
        current_page=page
    )




@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if query:
        gesture = gestures_collection.find_one({"name": {"$regex": query, "$options": "i"}})
        if gesture:
            return render_template('search_result.html', gesture=gesture)
        else:
            flash("Gesture not found.", "warning")
    return redirect(url_for('viewer_dashboard'))



if __name__ == "__main__":
    app.run(debug=True)
