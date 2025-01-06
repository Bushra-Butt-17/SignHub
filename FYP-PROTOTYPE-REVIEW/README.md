# SignHub Crowdsourcing Platform: User Stories, Screens, System Architecture & Project Plan 📱💻

Welcome to **SignHub**! A collaborative platform designed for the **deaf community**, **language experts**, and **researchers** to contribute, review, and learn Pakistan Sign Language (PSL) gestures. This document provides an in-depth look at the user stories, screens, system architecture, and flowcharts for all platform roles to ensure seamless collaboration and growth of PSL.

---

## User Roles & Stories

### 1. Viewer Role 👀
As a **Viewer**, the primary goal is to explore and learn PSL gestures.

#### **User Stories:**
- Explore available gestures to understand PSL.
- Browse the gesture repository by keyword or category.
- Watch avatar-rendered gestures for better understanding.
- Download gesture-related data for educational and research purposes.

#### **User Screens:**
1. **Gesture Detail Screen**
   - Detailed metadata like **dialect**, **meaning**, and **usage examples**.
   - **Avatar demonstration** of the gesture.
   - **Download button** for gesture videos or metadata.

   **Design Considerations**:
   - **Responsive design** for cross-device compatibility.
   - Clean, easy-to-read **metadata sections**.

2. **Home Screen**
   - **Platform overview** with functionalities.
   - Easy access to **repositories** and **resources**.

   **Design Considerations**:
   - Engaging visuals for **PSL** representation.
   - **Intuitive navigation bar** for seamless access.

---

### 2. Contributor Role 🖋️
As a **Contributor**, the aim is to submit PSL gestures to expand the platform's corpus.

#### **User Stories:**
- Submit gesture videos to add to the corpus.
- Provide **detailed metadata** for submissions.
- Participate in **targeted campaigns** to contribute specific gestures.
- Track the **status** of submissions and receive feedback.

#### **User Screens:**
1. **Gesture Submission Screen**
   - **Form for uploading videos** with metadata (e.g., word, dialect, description).
   - **Real-time validation** for video format and size.

   **Design Considerations**:
   - Clear, step-by-step **submission instructions**.
   - **Error messages** with corrective actions.

2. **Dashboard Screen**
   - View **submission statuses** (pending, approved, rejected).
   - Notifications for feedback and **campaign participation**.
   - Options to **edit** or **resubmit** rejected gestures.

   **Design Considerations**:
   - Organized layout with **filters** for submission status.
   - Prominent **resubmission buttons**.

---

### 3. Editor (Reviewer) Role 📑
As an **Editor**, review and validate gesture submissions to maintain high quality.

#### **User Screens:**
1. **Login Screen**
   - **Email and password** input fields.
   - **"Login"** button for secure authentication.

2. **Gesture Videos Library**
   - Display gesture **thumbnails**, **metadata**, and **ratings**.
   - Pagination or **scrolling** for browsing videos.

3. **Gesture Video Details & Rating**
   - **Video player** for viewing gestures.
   - **Rating** options for action, movement, and quality.

4. **Logout**
   - **Secure logout** button to exit the platform.

---

### 4. Admin Role 👨‍💻
As an **Admin**, oversee platform functionality, campaigns, and user accounts.

#### **User Stories:**
- Manage **user accounts** and roles.
- **Monitor campaigns** and content submissions.
- Access **analytics** to track platform performance.
- **Oversee quality** by resolving flagged issues.

#### **User Screens:**
1. **Admin Dashboard**
   - **Uploaded videos overview**.
   - Options to **delete** or **archive** content.

2. **Logout Option**
   - **Logout** button to securely exit.

---

## System Architecture 🖥️

### 1. **Frontend**
- **Login Page**: For secure user authentication.
- **Video Gallery**: To explore gesture videos.
- **Video Player & Rating**: Allows users to watch and rate gestures.

### 2. **Backend**
- **Authentication API**: Handles login and registration.
- **Video Data API**: Retrieves gesture metadata.
- **Rating Submission API**: Manages user feedback.

### 3. **Database & Storage**
- **Users Collection**: Stores user details.
- **Gesture Videos Collection**: Manages metadata and content.
- **Ratings Collection**: Stores user ratings for videos.
![Architecture-Diagram](https://github.com/user-attachments/assets/79d011e6-8ec1-4986-ba97-6a91979a0bdc)

---

## Entity-Relationship Diagram (ERD) 🗂️

### Entities and Relationships:
1. **Users**
   - Attributes: `user_id`, `email`, `password`, `name`, `created_at`.
   - Relationships: Submits gesture videos, provides ratings.
   
2. **Gesture Videos**
   - Attributes: `video_id`, `title`, `description`, `file_path`, `dialect`, `submitted_by`.
   - Relationships: Receives ratings from users.

3. **Ratings**
   - Attributes: `rating_id`, `video_id`, `user_id`, `actions_rating`, `movement_rating`, `quality_rating`, `created_at`.
![Entity-Relationship-Diagram](https://github.com/user-attachments/assets/38892780-44f8-4d16-850c-5feffa56bb8c)

---

## Use Case Diagram 🎯

### Key User Actions:
- **Login/Signup**: Access the platform securely.
- **View Gesture Videos**: Explore videos by category/dialect.
- **Watch and Rate Videos**: Provide ratings for improvement.
- **Logout**: Securely exit the platform.
![Use-Case-Diagram](https://github.com/user-attachments/assets/60aeb6b6-3799-40d7-8863-0132177b0418)

---

## Project Plan & Flowcharts 📊

### 1. **Admin Role Flowchart**
   - Manage **user accounts** and roles.
   - Oversee **flagged content** and analytics.
   - Monitor and perform **database maintenance**.
     ![Admin-Flowchart](https://github.com/user-attachments/assets/c3ada9d2-fa10-481a-9212-54143a451d2c)


### 2. **Viewer Role Flowchart**
   - Log in or **sign up**.
   - View and explore **gesture videos**.
   - Rate videos for feedback.
   - **Log out** securely.
![Viewer-Flowchart](https://github.com/user-attachments/assets/4a17f092-cca7-4ba8-b754-33f509f78f2e)

### 3. **Contributor Role Flowchart**
   - **Submit new gestures** and metadata.
   - Track status (pending, approved, rejected).
   - **Respond to feedback** and resubmit if needed.
![Contributor Flowchart](https://github.com/user-attachments/assets/93f4459b-7d7a-4ce7-a58b-854ab1630d97)

### 4. **Editor Role Flowchart**
   - **Review videos** and metadata.
   - Approve or **reject content**.
   - Moderate flagged ratings and feedback.
![Editor-Flowchart](https://github.com/user-attachments/assets/412c79da-1249-430e-96d4-5ff0a10568e9)

---

## Key Features 🌟

- **User Authentication**: Secure login and registration system.
- **Video Exploration**: Discover PSL gestures by category/dialect.
- **Interactive Feedback**: Rate videos for quality improvement.
- **Data Management**: MongoDB storage for efficient and scalable data handling.

---

The **SignHub Crowdsourcing Platform** is committed to bridging gaps in PSL resources through collaboration and high-quality validation. This platform will support the development, learning, and adoption of PSL at scale. 🚀
