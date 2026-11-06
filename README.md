# Book Recommendation System

A Flask web app that displays popular books and recommends similar titles from a book a reader enters.

## Features

- Browse the top 50 popular books, including cover images, authors, rating counts, and average ratings.
- Filter the popular-books list by title or author.
- Get up to five recommendations based on a selected book.
- Search is case-insensitive and ignores extra whitespace. The recommendation form also provides title suggestions.

## Requirements

- Python 3
- The project’s precomputed pickle files: `popular.pkl`, `pt.pkl`, `books.pkl`, and `similarity_score.pkl`

Install the Python dependencies from the project directory:

```bash
python -m pip install -r requirements.txt
```

## Run locally

From the project directory, start the Flask app:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Select **Recommend**, enter or choose a book title, and submit the form to see similar books.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── Procfile
├── popular.pkl
├── pt.pkl
├── books.pkl
├── similarity_score.pkl
└── templates/
    ├── index.html
    └── recommendation.html
```

The pickle files contain the precomputed popular-books list, book metadata, user-item data, and similarity scores used by the app. Keep these files in the same directory as `app.py`.

## Deployment

The included `Procfile` starts the app with Gunicorn:

```text
web: gunicorn app:app
```

Install the dependencies in `requirements.txt` and deploy to a platform that supports Gunicorn and the included pickle files.

> **Note:** Only load pickle files from a trusted source. Loading untrusted pickle files can execute arbitrary code.