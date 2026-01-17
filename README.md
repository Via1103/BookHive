# 📚 BookHive – Book Recommendation System

## 🔍 Overview
BookHive is a web-based book recommendation system that fetches real-time book data from the Google Books API and recommends relevant books based on a user’s search query and optional genre preferences.

The project demonstrates API integration, text preprocessing, and content-based recommendation logic using basic machine learning techniques.

---

## ✨ Features
- Search books using keywords (title, topic, or author)
- Optional genre-based filtering using Google Books subject filters
- Real-time data fetched from Google Books API
- Content-based recommendations using TF-IDF and cosine similarity
- Displays book ratings (if available)
- Clickable links to Google Books pages
- Simple and clean web interface

---

## 🧠 How the Recommendation System Works
1. User enters a search query and optional genres
2. The system fetches book data from the Google Books API
3. Book titles and descriptions are combined as text data
4. Text preprocessing is applied:
   - Lowercasing
   - Tokenization
   - Stopword removal
5. TF-IDF vectorization converts text into numerical vectors
6. Cosine similarity is used to measure relevance between:
   - User query
   - Each book’s text
7. Books are ranked by similarity score
8. Top relevant books are shown to the user

This is a content-based recommendation approach.

---

## 🛠 Tech Stack
### Backend
- Python
- Flask
- Requests
- NLTK
- Scikit-learn

### Frontend
- HTML
- CSS
- JavaScript

### API
- Google Books API

---

## 📂 Project Structure
BookHive/
├── app.py
├── requirements.txt
├── README.md
├── static/
│   └── script.js
└── templates/
    └── index.html

---

## 🚀 How to Run the Project
1. Clone the repository
2. Install dependencies using:
   pip install -r requirements.txt
3. Add your Google Books API key in app.py
4. Run the application:
   python app.py
5. Open browser and go to:
   http://127.0.0.1:5000

---

## 📊 Dataset
- Source: Google Books API
- Type: Real-time API data
- Fields used: title, authors, description, categories, ratings

---

## ⚠️ Limitations
- Depends on availability and quality of API metadata
- Limited number of results per API request
- No user history or collaborative filtering

---

## 🔮 Future Improvements
- Add user login and reading history
- Hybrid recommendation system
- Improved NLP techniques
- Deployment on cloud platforms

---

## ## 👥 Project Team

- **Vineeta Sharma** – Backend development, recommendation logic, API integration
- **Jayesh Shrivastav** – Frontend design and UI implementation
- **Shreya Sihare** – Data handling, testing, and documentation

