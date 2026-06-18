# CineMatch AI — Content-Based Movie Recommendation System

A production-quality AI recommendation system built for internship submission.
Uses **TF-IDF vectorisation** and **Cosine Similarity** to match user preferences
against a curated dataset of 50 movies.

---

## Quick Start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac / Linux
.\\venv\\Scripts\\activate       # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Project Structure

```
recommendation_system/
├── app.py                  # Entry point — page router
├── requirements.txt        # Python dependencies
├── README.md
│
├── data/
│   └── movies.csv          # 50-movie dataset (11 features)
│
├── models/
│   └── recommender.py      # Core engine: TF-IDF + Cosine Similarity
│
├── pages/
│   ├── home.py             # Landing page
│   ├── dataset.py          # Dataset Explorer
│   ├── engine.py           # Recommendation Engine
│   ├── explain.py          # Explanation View
│   ├── analytics.py        # Analytics Dashboard
│   └── docs.py             # Documentation & Interview Q&A
│
├── components/
│   ├── styles.py           # Global CSS, re-usable UI components
│   └── sidebar.py          # Navigation sidebar
│
└── utils/
    ├── data_loader.py      # CSV loading & filtering helpers
    └── session.py          # Streamlit session state initialisation
```

---

## Algorithm — How It Works

### 1. Feature Engineering
Each movie's attributes are combined into a weighted text string:

| Feature     | Weight (repetitions) |
|-------------|----------------------|
| Genre       | 4x                   |
| Director    | 3x                   |
| Language    | 2x                   |
| Cast        | 1x                   |
| Description | 1x                   |

### 2. TF-IDF Vectorisation
`TfidfVectorizer` (scikit-learn) converts the text corpus into a sparse matrix.
- Bigrams enabled (`ngram_range=(1, 2)`)
- English stop-words removed
- 5000 maximum features

### 3. Preference Vector
User selections are encoded into the same TF-IDF space as a single query vector.

### 4. Cosine Similarity
```
similarity = (A · B) / (||A|| × ||B||)
```
Returns a score in [0, 1] — independent of vector magnitude.

### 5. Popularity Blend
```
final_score = (1 - blend) × cosine_score + blend × popularity_score
popularity_score = 0.6 × norm_rating + 0.4 × norm_votes
```
Default blend = 15%.

---

## Tech Stack

| Layer       | Technology                |
|-------------|---------------------------|
| Language    | Python 3.10+              |
| Data        | Pandas                    |
| ML          | Scikit-learn (TF-IDF, Cosine Similarity) |
| Visualisation | Plotly                  |
| Frontend    | Streamlit                 |
| Typography  | Poppins · Space Grotesk · Inter |

---

## Pages

| Page                   | Description                                      |
|------------------------|--------------------------------------------------|
| Landing                | Project overview, algorithm explainer            |
| Dataset Explorer       | Browse, filter, and visualise the corpus         |
| Recommendation Engine  | Run the engine with your preferences             |
| Explanation View       | Feature-level breakdown of each recommendation  |
| Analytics Dashboard    | Corpus and recommendation analytics             |
| Documentation          | Architecture, execution guide, interview Q&A     |

---

## Interview Preparation

Key questions covered in the Documentation page:

- Why content-based filtering?
- How does TF-IDF work?
- Why Cosine Similarity over Euclidean distance?
- How does genre weighting work?
- What are the limitations?
- How would you scale to millions of movies?
- How would you add collaborative filtering?

---


