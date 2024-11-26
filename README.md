
# Gesture Detail Web Application

## Overview

The **Gesture Detail Web Application** is a comprehensive platform designed to catalog and showcase gesture videos. It aims to provide an intuitive and visually appealing interface for users to explore gestures from various dialects of sign language. This project is particularly useful for researchers, educators, and learners in the domain of sign language.

---

## Features Implemented

### **1. Responsive Design**
   - **Bootstrap 4.5.2** integration ensures responsiveness across devices.
   - Custom CSS enhances visual aesthetics and maintains a consistent layout.

### **2. Navigation Bar**
   - Links to:
     - **Home**: Navigate to the homepage.
     - **View Videos**: Explore the collection of gesture videos.
     - **About**: Learn more about the application.
   - Hover effects improve usability.

### **3. Gesture Detail Page**
   - Displays comprehensive details of an individual gesture:
     - **Gesture Name**: Prominently displayed at the top.
     - **Video Playback**:
       - Embedded video player for gestures with video files.
       - Placeholder text ("No video available for this gesture") for missing videos.
     - **Description**:
       - Displays the gesture description or a fallback message if absent.
     - **Dialect(s)**:
       - Shows dialects related to the gesture or "Not specified."
     - **Submitted By**:
       - Indicates the submitter's name or defaults to "Anonymous."
   - Features a **"Back to Video List"** link for easy navigation.

### **4. Enhanced Styling**
   - Background: Light gray (`#f5f7fa`) ensures readability.
   - Boxes: White backgrounds with rounded corners and subtle shadows.
   - Text Colors:
     - Dark text (`#333`) for primary content.
     - Highlighted elements in blue (`#007bff`) or red (`#ea445a`).
   - Video Player: Centered with a fixed maximum width for a clean layout.

### **5. Error Handling**
   - Ensures fallback messages for missing data, such as:
     - Video files.
     - Description or dialect information.
     - Submitter details.

### **6. Database Integration (MongoDB)**
   - MongoDB is used as the backend database for storing gesture-related data.
   - Database Name: **`signhub`**
   - Collection Name: **`gestures`**

---

## MongoDB Database Structure

### **Database Name**
   - **`signhub`**

### **Collection Name**
   - **`gestures`**

### **Document Structure**
Each document in the `gestures` collection represents a gesture with the following fields:

| Field Name        | Data Type  | Description                                                   |
|--------------------|------------|---------------------------------------------------------------|
| `_id`             | ObjectId   | Unique identifier for the gesture (automatically generated). |
| `name`            | String     | The name of the gesture.                                      |
| `description`     | String     | Detailed description of the gesture.                         |
| `dialect`         | String     | Dialects associated with the gesture (e.g., Punjabi, Sindhi). |
| `video_url`       | String     | URL pointing to the gesture video file.                      |
| `submitted_by`    | String     | Name of the person who submitted the gesture.                |
| `created_at`      | Date       | Timestamp indicating when the gesture was added.             |

---

## How to Run the Project

### **Prerequisites**
1. Install **Python 3.8+**.
2. Install MongoDB and set up the database.
3. Install the required Python packages.

### **Setup Instructions**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   pip install flask pymongo
   ```
3. Set up MongoDB:
   - Start MongoDB locally or configure a cloud database.
   - Create the database and collection using the structure described above.
4. Configure the Flask application:
   - Update the `app.py` file with the MongoDB connection string:
     ```python
     from pymongo import MongoClient

     client = MongoClient("<your-mongodb-connection-string>")
     db = client['signhub']
     gestures_collection = db['gestures']
     ```

5. Run the Flask server:
   ```bash
   python app.py
   ```
6. Access the application in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

---

## Example Document in MongoDB
```json
{
  "_id": "6487f1a462b1e23f98b1d4e9",
  "name": "Hello Gesture",
  "description": "A friendly greeting gesture commonly used in Pakistani Sign Language.",
  "dialect": "Punjabi",
  "video_url": "/videos/hello.mp4",
  "submitted_by": "Ali Khan",
  "created_at": "2024-11-25T10:30:00Z"
}
```

---

## Planned Features
- **Upload Functionality**: Allow users to upload gesture videos and metadata.
- **User Authentication**: Secure login system for personalized interactions.
- **Search and Filter**: Enable searching and filtering gestures by dialect or category.
- **Analytics Dashboard**: Display insights into gesture usage and submissions.

---

## Contributing
Contributions are welcome! Please fork the repository, create a branch, and submit a pull request. For major changes, open an issue first to discuss the proposed changes.

---

## Feedback and Support
For any issues or suggestions, feel free to open an issue on GitHub or contact us at **support@signhub.com**.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

