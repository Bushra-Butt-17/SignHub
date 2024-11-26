from flask import Flask, request, jsonify, render_template, redirect, url_for, Response
from pymongo import MongoClient
import gridfs
from bson import ObjectId  # Import ObjectId for MongoDB ObjectID manipulation
from datetime import datetime

app = Flask(__name__)

# Replace with your MongoDB Atlas connection string
MONGO_URI = "mongodb+srv://bsdsf21m020:ZnmtirpcUlMusr1u@gestures.qg4td.mongodb.net/?retryWrites=true&w=majority&appName=Gestures"

# Initialize the MongoDB client and GridFS
client = MongoClient(MONGO_URI)
db = client["gestures"]  # Use the gestures database
fs = gridfs.GridFS(db)   # Initialize GridFS for file storage

# Example structure for the gestures collection
gestures_collection = db["gestures"]

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
        "created_at": datetime.now().strftime("%Y-%m-%d")  # Current date for submission (dynamic)
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

if __name__ == "__main__":
    app.run(debug=True)
