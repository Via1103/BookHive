from flask import Flask, render_template, request, jsonify
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download required NLP resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

app = Flask(__name__)

# BookHive Branding
PROJECT_NAME = "BookHive"

# Google Books API URL configured to fetch up to 20 results.
# Replace YOUR_API_KEY with your actual key.
# Note: The {query} placeholder will be replaced with the full search query, including subject filters if provided.
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=20&key=AIzaSyBJCqLB4TERRoRmEqWwrp9ORsU6H9zl9Nw"

# Number of recommendations to output on the website.
NUM_OUTPUT = 10

def preprocess_text(text):
    """Converts text to lowercase, tokenizes it, and removes stopwords."""
    tokens = word_tokenize(text.lower())
    return " ".join([word for word in tokens if word not in stopwords.words('english')])

@app.route('/')
def home():
    """Render the home page (with BookHive branding)."""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_books():
    """
    Fetch book recommendations based on a user query and, optionally, selected genres.
    
    Instead of doing post-query filtering, this version appends the genre filters directly
    to the API query using the 'subject:' operator. This should yield results that match the genre,
    even when the API response doesn't always include complete 'categories' data.
    """
    user_query = request.json.get("query", "")
    selected_genres = request.json.get("genres", [])
    
    if not user_query:
        return jsonify({"error": f"{PROJECT_NAME}: No query provided."}), 400

    # Build the query.
    # If a user provides genre(s), append them using the 'subject:' operator.
    if selected_genres:
        # Build a string like "subject:Fiction subject:Fantasy" for each selected genre.
        subject_filters = " ".join([f"subject:{genre.strip()}" for genre in selected_genres if genre.strip() != ""])
        full_query = f"{user_query} {subject_filters}"
    else:
        full_query = user_query

    # For relevance scoring, we preprocess the original user query.
    preprocessed_query = preprocess_text(user_query)
    if not preprocessed_query:
        preprocessed_query = user_query.lower()
    
    # Construct the API URL using the full query (which now might include subject filters)
    api_url = GOOGLE_BOOKS_API.format(query=full_query)
    response = requests.get(api_url)
    if response.status_code != 200:
        return jsonify({"error": f"{PROJECT_NAME}: Failed to fetch book data."}), 500

    books_data = response.json().get("items", [])
    if not books_data:
        return jsonify({"error": f"{PROJECT_NAME}: No books found for your search."}), 404

    # Since the API already applies the subject filter, we no longer need post-fetch filtering.
    books_data = books_data[:20]  # Limit the results per the API's maxResults

    book_list = []
    combined_texts = []  # For storing combined title and description texts

    for book in books_data:
        volume_info = book.get("volumeInfo", {})
        title = volume_info.get("title", "Unknown Title")
        author = volume_info.get("authors", ["Unknown Author"])[0]
        cover = volume_info.get("imageLinks", {}).get("thumbnail", "")
        description = volume_info.get("description")
        # Fallback: if no description, use the title.
        if not description:
            description = title
        
        # Extract info link for clickability.
        info_link = volume_info.get("infoLink", "#")
        # Extract rating if available; else set a default.
        rating = volume_info.get("averageRating", "No rating")
        # Combine title and description for a richer text representation.
        combined_text = title + " " + description

        book_list.append({
            "title": title,
            "author": author,
            "cover": cover,
            "description": description,
            "info_link": info_link,
            "rating": rating
        })
        combined_texts.append(preprocess_text(combined_text))

    # Compute TF-IDF vectors over the combined texts.
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined_texts)
    
    # Transform the original (preprocessed) user query.
    user_vector = vectorizer.transform([preprocessed_query])
    scores = cosine_similarity(user_vector, tfidf_matrix)[0]

    # Pair each book with its relevance score, sort descending, and take the top NUM_OUTPUT.
    recommended_books = sorted(zip(book_list, scores), key=lambda x: x[1], reverse=True)[:NUM_OUTPUT]
    
    # Format the output.
    result = [{
        "title": book["title"],
        "author": book["author"],
        "cover": book["cover"],
        "description": book["description"],
        "score": round(score, 2),
        "info_link": book["info_link"],
        "rating": book["rating"]
    } for book, score in recommended_books]
    
    return jsonify({"recommendations": result})

if __name__ == "_main_":
    app.run(debug=True)