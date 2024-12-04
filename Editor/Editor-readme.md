# SignHub Editor Role - Video Rating & Feedback

Welcome to the **Editor Dashboard** of SignHub! As an editor, your role is to evaluate and rate sign language videos based on three important criteria: **Action Rating**, **Movement Rating**, and **Video Quality Rating**. Your ratings and feedback will help ensure that only the best content is showcased on the platform for learners.

## 🌟 Editor Features

As an editor, you have the following capabilities:

- **Rate Videos**: Evaluate videos based on three criteria: Action, Movement, and Video Quality.
- **Action Rating**: Rate how accurately the sign language gesture is performed.
- **Movement Rating**: Rate the smoothness and accuracy of the hand movements during the gesture.
- **Video Quality Rating**: Rate the technical quality of the video, including clarity, lighting, and resolution.
- **Provide Feedback**: Leave constructive feedback on videos, offering suggestions for improvements.

---

### 1. 📝 Rate Video
- **Endpoint**: `/editor/videos/<video_id>/rate`
- **Method**: `POST`
- **Description**: Allows the editor to rate a video based on three categories: Action, Movement, and Video Quality.

#### Parameters:
- **action_rating** (integer): Rating for the accuracy of the action (1-5).
- **movement_rating** (integer): Rating for the smoothness of the movement (1-5).
- **video_quality_rating** (integer): Rating for the overall video quality (1-5).

#### Example Request:
```json
{
  "action_rating": 4,
  "movement_rating": 5,
  "video_quality_rating": 3
}
```
#### Example Response:
```json
{
  "message": "Video rated successfully",
  "video_id": 5
}
```
---
### 2. 📄 Get Video Ratings

-- **Endpoint**: /editor/videos/<video_id>/ratings
-- **Method**: GET
-- **Description**: Retrieves the current ratings for a specific video.

#### Example Request:
```json
GET /editor/videos/5/ratings
```

#### Example Response:
```json
{
  "action_rating": 4,
  "movement_rating": 5,
  "video_quality_rating": 3
}
```
---

### 3. 📝 Provide Feedback

-- **Endpoint**: /editor/videos/<video_id>/feedback
-- **Method**: POST
-- **Description**: Allows the editor to provide feedback for a video, detailing any improvements needed or suggestions for better quality.

#### Parameters:
-- **feedback (string)**: The feedback message for the video.

#### Example Request:
```json
{
  "feedback": "The lighting in the video can be improved, and the action could be made clearer."
}
```

#### Example Response:
```json
{
  "message": "Feedback submitted successfully",
  "video_id": 5
}
```
---

## 📋 Notes

### Video Rating Criteria:
- **Action Rating**: How accurately the sign language gesture is performed.
- **Movement Rating**: How smooth and natural the hand movements are.
- **Video Quality Rating**: The overall quality of the video, including clarity, lighting, and resolution.

### Feedback:
Editors should provide constructive and actionable feedback to help contributors improve their videos, especially in areas such as:
- Gesture clarity
- Movement precision
- Video quality

---

## 💡 Future Enhancements

- **Batch Rating**: Introduce functionality for editors to rate multiple videos at once.
- **User Reviews**: Allow users to rate and provide feedback on videos after they have been rated by editors.
- **Editor Dashboard**: Create a comprehensive dashboard for editors to efficiently manage and rate videos.
- **Video Rating History**: Implement a system to track and display the history of ratings and feedback for each video.

---

## 🎯 Getting Started

1. **Login** as an Editor (assuming login functionality is in place).
2. Use the provided API endpoints to rate videos based on the specified criteria.
3. Review and provide feedback for videos that need improvement.
4. Ensure that the ratings align with the platform's quality standards for sign language learning content.

