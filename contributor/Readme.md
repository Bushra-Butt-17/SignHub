

---

# ✨ Contributor Role - SignHub  

Welcome to the **Contributor** section of **SignHub**! As a Contributor, you play a vital role in enriching our platform with sign language gestures in various dialects. Thank you for helping us grow this resource! 🙌  

## 🌟 Features  

- ➕ **Add Videos**: Upload video gestures with details like dialect and category.  
- 📂 **View Your Contributions**: Check all the gestures you've added.  
- ✅ **Instant Feedback**: Get a success message upon successful video submission.  

---

## 🛠️ Endpoints for Contributors  

### 1. ➕ **Add a New Video Gesture**  
**Endpoint**: `/contributor/add-video`  
- **Method**: `POST`  
- **Description**: Allows Contributors to upload a new gesture video with details.  
- **Request Body**:  
  ```json  
  {  
    "title": "Hello Gesture",  
    "dialect": "Punjabi",  
    "category": "Greetings",  
    "video_url": "http://example.com/videos/hello.mp4"  
  }  
  ```  

**Example Response**:  
```json  
{  
  "message": "Video gesture added successfully!",  
  "video_id": 1  
}  
```

---

### 2. 📂 **View Contributed Videos**  
**Endpoint**: `/contributor/my-videos`  
- **Method**: `GET`  
- **Description**: Displays a list of all videos uploaded by the logged-in Contributor.  

**Example Response**:  
```json  
[  
  {  
    "id": 1,  
    "title": "Hello Gesture",  
    "dialect": "Punjabi",  
    "category": "Greetings",  
    "video_url": "http://example.com/videos/hello.mp4"  
  },  
  {  
    "id": 2,  
    "title": "Thank You Gesture",  
    "dialect": "Sindhi",  
    "category": "Politeness",  
    "video_url": "http://example.com/videos/thankyou.mp4"  
  }  
]  
```

---

### 3. ⚙️ **Contributor Login**  
**Endpoint**: `/contributor/login`  
- **Method**: `POST`  
- **Description**: Logs the Contributor into the system.  
- **Request Body**:  
  ```json  
  {  
    "username": "contributor123",  
    "password": "securepassword"  
  }  
  ```  

**Example Response**:  
```json  
{  
  "message": "Login successful!",  
  "token": "your-auth-token-here"  
}  
```

---

## 📋 Notes  

- Each video you upload must include a **title**, **dialect**, and **category** for approval.  
- You can always check your contributions and manage them from the `/my-videos` endpoint.  
- Make sure to log in to access contributor functionalities.  

Thank you for being a part of **SignHub** and making sign language accessible for everyone! 🌍✨  

---


