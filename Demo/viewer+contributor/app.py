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
import os  # Import os module to work with file paths
from flask import Flask, render_template, send_from_directory


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home1():
    return render_template('home1.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Handle video upload logic here
    # If upload is successful:
    return render_template('upload.html', success=True)
categories = ['education', 'health', 'emotions']
dialects = ['punjabi', 'sindhi', 'urdu']
@app.route('/view_by_categories')
def view_by_categories():
    # Render the View by Categories page and pass category names
    return render_template('view_by_categories.html', categories=categories)

@app.route('/view_by_dialects')
def view_by_dialects():
    # Render the View by Dialects page and pass dialect names
    return render_template('view_by_dialects.html', dialects=dialects)


@app.route('/upload_video', methods=['POST'])
def upload_video():
    # Your file handling logic here
    # Save video, handle form data, etc.
    return redirect(url_for('contributor_dashboard'))




# Route to view videos by category
@app.route('/videos/category/<category>')
def view_videos_by_category(category):
    # Check if the category exists in the videos directory
    category_path = os.path.join('static', 'videos', category)
    if os.path.isdir(category_path):
        video_files = [
            f"/static/videos/{category}/{video}" 
            for video in os.listdir(category_path) if video.endswith('.mp4')
        ]
        return render_template('view_videos.html', videos=video_files, category=category)
    else:
        return render_template('404.html', category=category)


@app.route('/videos/category/<category_name>')
def view_category(category_name):
    # Logic to fetch videos for the specific category
    # Example: fetching videos from a database or file system
    videos = get_videos_by_category(category_name)  # Assuming a function that fetches videos
    return render_template('category.html', videos=videos, category_name=category_name)


@app.route('/video_gallery')
def video_gallery():
    return render_template('video_gallery.html')


# Route for SignHub Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process form data (example placeholder logic)
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Perform authentication (replace this with actual logic)
        if email == "user@example.com" and password == "password":
            return redirect(url_for('contributor_dashboard'))  # Redirect to a dashboard or other page
        else:
            return "Invalid login credentials. Please try again.", 401  # Error response
    
    # Render login page for GET request
    return render_template('login.html')

# Example dashboard route (to test redirection)
@app.route('/contributor_dashboard')
def contributor_dashboard():
    return render_template('contributor_dashboard.html')


@app.route('/view_videos')
def view_videos():
    # Just render the template without any dynamic data
    return render_template('view_videos.html')


if __name__ == '__main__':
    app.run(debug=True)