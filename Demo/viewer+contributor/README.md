
---

# SignHub Viewer and Contributor Role Demo  

This repository showcases the functionality of the **Viewer** and **Contributor** roles for the **SignHub** learning platform. The platform focuses on sign language education with videos categorized by dialects and categories.  

---

## Viewer Role Features  

1. **View by Categories**  
   - Browse gesture videos grouped into predefined categories such as "Greetings," "Educational Signs," and more.  

2. **View by Dialects**  
   - Videos are organized based on regional dialects of Pakistani sign language.  
   - Examples: Punjabi, Sindhi, Pashto, Balochi, etc.  

3. **Search Videos**  
   - Find specific gestures using a search bar with keyword-based matching.  

4. **Explore Without Login**  
   - No signup or login required—users can freely browse all available videos.  

---

## Contributor Role Features  

1. **Add Video Gestures**  
   - Contributors can upload gesture videos by:  
     - Selecting a predefined **category** (e.g., Greetings).  
     - Specifying a regional **dialect**.  

2. **View Contributed Videos**  
   - Contributors can view a list of all the gestures they have uploaded.  

3. **Success Feedback**  
   - After uploading, contributors receive a success message confirming their submission.  

4. **Secure Login**  
   - Contributors must log in to upload gestures, ensuring a secure and controlled contribution process.  

 

---

## Prerequisites  

- **Python** (v3.8 or above)  
- **Flask** (v2.0 or above)  
- **MongoDB Atlas** (database for storing video and contributor metadata)  

Install the required Python libraries:  
```bash  
pip install flask pymongo  
```  


---

## Demo  

### Viewer Role  
- **Landing Page**: Explore options like "View by Categories," "View by Dialects," and search for gestures.  
- **View by Categories**: Videos grouped under themes like "Greetings" and "Daily Activities."  
- **View by Dialects**: Videos filtered by regional dialects.  
- **Search**: Keyword-based search for gestures.  

### Contributor Role  
- **Upload Videos**: Add gesture videos with a category and dialect.  
- **View Uploads**: See all submitted videos in one place.  
- **Login**: Ensure secure access before contributing.  

---


