
---

# 👀 Viewer Role - SignHub  

Welcome to the **Viewer** section of **SignHub**, a platform to explore and learn sign language through video gestures in various dialects. No signup or login is required! 🚀  

## 🌟 Features  

- 🎥 **Explore Videos**: Browse all available sign language videos.  
- 🔍 **Search Functionality**: Quickly find specific gestures or dialects.  
- 📂 **Categorized View**: Videos organized by dialect and predefined categories for easy navigation.  

---

## 🛠️ Endpoints for Viewers  

### 1. 📚 **Get All Videos**  
**Endpoint**: `/viewer/videos`  
- **Method**: `GET`  
- **Description**: Retrieves all approved sign language videos in different dialects.  

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

### 2. 🔍 **Search Videos**  
**Endpoint**: `/viewer/search`  
- **Method**: `GET`  
- **Parameters**:  
  - `query` (string): The keyword or phrase to search for.  

**Example Request**:  
`/viewer/search?query=hello`  

**Example Response**:  
```json  
[  
  {  
    "id": 1,  
    "title": "Hello Gesture",  
    "dialect": "Punjabi",  
    "category": "Greetings",  
    "video_url": "http://example.com/videos/hello.mp4"  
  }  
]  
```

---

### 3. 📂 **View Videos by Category**  
**Endpoint**: `/viewer/videos/category/<category_name>`  
- **Method**: `GET`  
- **Description**: Retrieves videos in the specified category.  

**Example Request**:  
`/viewer/videos/category/Greetings`  

**Example Response**:  
```json  
[  
  {  
    "id": 1,  
    "title": "Hello Gesture",  
    "dialect": "Punjabi",  
    "video_url": "http://example.com/videos/hello.mp4"  
  }  
]  
```

---

### 4. 🌍 **View Videos by Dialect**  
**Endpoint**: `/viewer/videos/dialect/<dialect_name>`  
- **Method**: `GET`  
- **Description**: Retrieves videos in the specified dialect.  

**Example Request**:  
`/viewer/videos/dialect/Punjabi`  

**Example Response**:  
```json  
[  
  {  
    "id": 1,  
    "title": "Hello Gesture",  
    "category": "Greetings",  
    "video_url": "http://example.com/videos/hello.mp4"  
  }  
]  
```

---

## 📋 Notes  
- Only **approved videos** will appear in the Viewer dashboard.  
- You can use these endpoints to create a seamless learning experience for users.  

Enjoy exploring the beauty of sign language! ✨  

---


