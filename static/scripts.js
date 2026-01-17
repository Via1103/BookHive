async function getRecommendations() {
  const query = document.getElementById("search").value.trim();
  const genreInput = document.getElementById("genre-input").value.trim();
  
  // Split genre input by commas, trim extra whitespace, and remove empty strings
  const selectedGenres = genreInput
    .split(',')
    .map(genre => genre.trim())
    .filter(genre => genre !== "");
  
  if (!query) return;  // Exit if no query is provided
  
  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, genres: selectedGenres })
    });
    
    const data = await response.json();
    if (data.recommendations) {
      displayBooks(data.recommendations);
    } else {
      alert("No recommendations found!");
    }
  } catch (error) {
    console.error("Error fetching recommendations:", error);
  }
}

function displayBooks(books) {
  const bookList = document.getElementById("book-list");
  bookList.innerHTML = ""; // Clear previous recommendations

  // Create a book card for each recommendation
  books.forEach(book => {
    const container = document.createElement("div");
    container.className = "book-card";
    
    container.innerHTML = `
      <a class="book-link" href="${book.info_link}" target="_blank">
        <img src="${book.cover}" alt="${book.title}" style="width:100%; border-radius:10px;">
        <h3>${book.title}</h3>
        <p><strong>${book.author}</strong></p>
        <p>Relevance: ${book.score}</p>
        <p class="summary">${book.description}</p>
        <p class="rating">Rating: ${book.rating}</p>
      </a>
    `;
    
    bookList.appendChild(container);
  });
}

// Trigger search on button click or Enter key press in the search input
document.getElementById("search-button").addEventListener("click", getRecommendations);
document.getElementById("search").addEventListener("keyup", function(event) {
  if (event.key === "Enter") {
    getRecommendations();
  }
});