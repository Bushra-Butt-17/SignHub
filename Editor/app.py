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
MONGO_URI = "mongodb+srv://bsdsf21m017:G7HcD7Rry7NXM9tV@cluster0.bjoua.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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
        "video_id": file_id,  # Store the ObjectId of the file in GridFS
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




@app.route('/all_videos', methods=['GET'])
def show_all_videos():
    gestures = list(gestures_collection.find())  # Get all videos

    for gesture in gestures:
        gesture['video_url'] = url_for('get_video', video_id=str(gesture['video_id']))

    # Check if the user is an admin or contributor
    is_admin = session.get('user_role') == 'admin'
    is_contributor = session.get('user_role') == 'contributor'  # Check if contributor

    return render_template('videos.html', gestures=gestures, is_admin=is_admin, is_contributor=is_contributor)



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
        # Convert the video_id from string to ObjectId
        video_id = ObjectId(video_id)
        # Fetch the video from GridFS
        video_file = fs.get(video_id)  # Use ObjectId to fetch from GridFS
        return Response(video_file, content_type='video/mp4')
    except gridfs.errors.NoFile:
        return "Video not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

    




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user is an admin or contributor
        if email == 'aymen1@gmail.com' and password == '1234':
            session['user_role'] = 'admin'
        elif email == 'haider@gmail.com' and password == '1234':
            session['user_role'] = 'contributor'
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))

        flash("Login successful!", "success")
        return redirect(url_for('show_all_videos'))

    return render_template('login.html')
@app.route('/rate_video/<gesture_id>', methods=['POST'])
def rate_video(gesture_id):
    if session.get('user_role') != 'contributor':
        flash("You do not have permission to rate videos.", "danger")
        return redirect(url_for('show_all_videos'))  # Ensure this returns right after permission check

    # Get the ratings from the form
    actions_rating = request.form.get('actions_rating')
    movement_rating = request.form.get('movement_rating')
    video_quality_rating = request.form.get('video_quality_rating')

    # Update the gesture with the ratings
    gestures_collection.update_one(
        {"_id": ObjectId(gesture_id)},
        {"$set": {
            "actions_rating": actions_rating,
            "movement_rating": movement_rating,
            "video_quality_rating": video_quality_rating
        }}
    )

    flash("Rating submitted successfully.", "success")  # This will now show up after submitting
    return redirect(url_for('show_all_videos'))  # Redirect after the flash



@app.route('/logout', methods=['POST'])
def logout():
    # Clear session data
    session.pop('user_role', None)  # Or any other session data
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))  # Redirect to the homepage or any desired page







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

@app.route('/delete_video/<gesture_id>', methods=['POST'])
def delete_video(gesture_id):
    # Check if the user is an admin
    if session.get('user_role') != 'admin':
        flash("You do not have permission to delete videos.", "danger")
        return redirect(url_for('all_videos'))

    # Delete the video from GridFS
    gesture = gestures_collection.find_one({"_id": ObjectId(gesture_id)})
    if gesture:
        # Delete the video from GridFS
        fs.delete(ObjectId(gesture['video_id']))
        # Remove the gesture entry from the database
        gestures_collection.delete_one({"_id": ObjectId(gesture_id)})

        flash("Video deleted successfully.", "success")
        return redirect(url_for('show_all_videos'))
    else:
        flash("Video not found.", "danger")
        return redirect(url_for('show_all_videos'))









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


@app.route('/logout_admin', methods=['POST'])
def logout_admin():
    # Clear the session data for the admin
    session.pop('user_id', None)
    session.pop('user_role', None)

    # Optionally, flash a message and redirect
    flash("You have logged out as admin.", "info")
    return redirect(url_for('home'))  # Redirect to the homepage or login page















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
