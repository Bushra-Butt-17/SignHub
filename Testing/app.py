from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
from pymongo import MongoClient
import gridfs
from bson import ObjectId  # Import ObjectId for MongoDB ObjectID manipulation
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask import Flask, request, jsonify, render_template, redirect, url_for, Response, session, flash

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




@app.route('/upload_form')
def upload_form():
    return render_template('upload_video.html')





@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Ensure that a file is provided in the request
    if 'video' not in request.files:
        return jsonify({"error": "No video file found in request"}), 400
    
    file = request.files['video']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file to GridFS
    file_id = fs.put(file, filename=file.filename)

    # Now create a new gesture entry in the gestures collection
    gesture_data = {
        "name": request.form.get("name"),  # e.g., "Hello"
        "description": request.form.get("description"),  # e.g., "A greeting gesture in PSL."
        "dialect": request.form.getlist("dialect"),  # List of dialects
        "video_id": str(file_id),  # Store GridFS file ID
        "submitted_by": request.form.get("submitted_by"),  # User ID of the submitter
        "status": "pending",  # Initial status (could be under_review, validated, etc.)
        "created_at": datetime.now()  # Current date for submission (dynamic)
    }

    # Insert the gesture data into the gestures collection
    gesture_id = gestures_collection.insert_one(gesture_data).inserted_id

    # Redirect to confirmation page with gesture_id
    return redirect(url_for('upload_success', gesture_id=str(gesture_id)))



@app.route('/upload_success/<gesture_id>')
def upload_success(gesture_id):
    # Retrieve gesture details using the gesture_id
    gesture = gestures_collection.find_one({"_id": ObjectId(gesture_id)})

    # If gesture is not found, return an error (should not happen if redirect works)
    if not gesture:
        return "Gesture not found", 404

    # Render a confirmation page showing the gesture details
    return render_template('upload_success.html', gesture=gesture)




# Route to get all videos
@app.route('/all_videos', methods=['GET'])
def show_all_videos():
    gestures_collection = db.gestures
    gestures = list(gestures_collection.find())  # Convert cursor to a list
    
    for gesture in gestures:
        # Prepare video URL to be used in the template
        gesture['video_url'] = url_for('get_video', video_id=gesture['video_id'])
    
    return render_template('videos.html', gestures=gestures)


@app.route('/gesture_detail/<gesture_id>')
def gesture_detail(gesture_id):
    # Retrieve the gesture by its ID from the gestures collection
    gesture = gestures_collection.find_one({"_id": ObjectId(gesture_id)})

    if not gesture:
        return "Gesture not found", 404

    # Render the gesture detail page with the specific gesture's data
    return render_template('gesture_detail.html', gesture=gesture)




# Route to serve video
@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    try:
        # Fetch the video from GridFS
        video_file = fs.get(ObjectId(video_id))  # Use ObjectId to fetch from GridFS
        return Response(video_file, content_type='video/mp4')
    except gridfs.errors.NoFile:
        return "Video not found", 404
    




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



@app.route('/approve_gestures', methods=['GET', 'POST'])
def approve_gestures():
    # Ensure the user is an admin
    if session.get('user_role') != 'admin':
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for('dashboard'))

    # Fetch gestures that need approval (you can add a field like 'status' in your gestures collection to track)
    gestures = gestures_collection.find({"status": "pending"})  # Assuming "pending" means awaiting approval

    if request.method == 'POST':
        # Logic for approving a gesture (e.g., changing its status to 'approved')
        gesture_id = request.form.get('gesture_id')
        gestures_collection.update_one({"_id": ObjectId(gesture_id)}, {"$set": {"status": "approved"}})
        flash("Gesture approved successfully.", "success")
        return redirect(url_for('approve_gestures'))

    return render_template('approve_gestures.html', gestures=gestures)








@app.route('/contributor')
def contributor_dashboard():
    if session.get('role') != 'contributor':
        return "Unauthorized Access", 403
    name = session.get('name', 'User')  # Default to 'User' if name is missing
    return f"Welcome to the Contributor Dashboard, {name}!"






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'viewer')  # Default role is 'viewer'

        # Check if the email already exists
        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for('signup'))

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user document
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": role
        }

        # Insert the new user into the user_management database
        users_collection.insert_one(new_user)

        flash("Signup successful! Please log in.", "success")  # Success message
        return redirect(url_for('login'))
    
    return render_template('signup.html')















@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You need to log in first.", "danger")
        return redirect(url_for('login'))
    
    user_role = session.get('user_role')  # Get the user's role from the session

    if user_role == 'admin':
        return render_template('admin_dashboard.html')
    elif user_role == 'contributor':
        return render_template('contributor_dashboard.html')
    elif user_role == 'viewer':
        return render_template('viewer_dashboard.html')
    else:
        flash("Unknown role.", "danger")
        return redirect(url_for('login'))







@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash("You have logged out successfully.", "success")
    return redirect(url_for('login'))





# Route to view all users
@app.route('/users')
def view_users():
    users = mongo.db.users.find()  # Accessing the 'users' collection
    return render_template('view_users.html', users=users)

# Route to delete a user
@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': mongo.ObjectId(user_id)})  # Deleting user by ObjectId
    return redirect(url_for('view_users'))




@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('view_users'))
    return render_template('add_user.html')







@app.route('/viewer_dashboard')
def viewer_dashboard():
    if 'user_id' not in session:
        flash("Please log in first", "danger")
        return redirect(url_for('login'))
    
    user_role = session.get('user_role')
    if user_role != 'viewer':
        flash("Access Denied. You are not a viewer.", "danger")
        return redirect(url_for('dashboard'))

    # Fetch recent gestures
    recent_gestures = gestures_collection.find().sort("created_at", -1).limit(5)

    # Fetch categories or dialects for gestures (adjust based on your data structure)
    categories = db.categories.find()

    # Fetch featured contributors (limit to top 5)
    featured_contributors = users_collection.find({"role": "contributor"}).limit(5)

    return render_template('viewer_dashboard.html', 
                           gestures=recent_gestures, 
                           categories=categories, 
                           contributors=featured_contributors)






@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        # Perform a search in the gestures collection
        results = gestures_collection.find({'$text': {'$search': query}})
    else:
        results = []

    return render_template('search_results.html', gestures=results)





@app.route('/recent_gestures')
def recent_gestures():
    # Fetch gestures, ordered by created_at (descending)
    gestures = list(gestures_collection.find().sort('created_at', -1).limit(5))
    
    print("Gestures fetched:", gestures)  # Debugging line

    if not gestures:
        return render_template('recent_gestures.html', message="No gesture available yet")

    return render_template('recent_gestures.html', gestures=gestures)




gestures_collection.create_index([("name", "text"), ("description", "text")])

if __name__ == "__main__":
    app.run(debug=True)
