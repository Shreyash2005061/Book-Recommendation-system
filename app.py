from pathlib import Path
import pickle

import numpy as np
from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'popular.pkl', 'rb') as f:
    popular_df = pickle.load(f)
with open(BASE_DIR / 'pt.pkl', 'rb') as f:
    pt = pickle.load(f)
with open(BASE_DIR / 'books.pkl', 'rb') as f:
    books = pickle.load(f)
with open(BASE_DIR / 'similarity_score.pkl', 'rb') as f:
    similarity_scores = pickle.load(f)

app = Flask(__name__)


def normalize_title(title):
    return ' '.join(str(title).split()).casefold()


title_lookup = {}
for title in pt.index:
    title_lookup.setdefault(normalize_title(title), title)


@app.route('/')
def index():
    top_books = popular_df[['Book-Title', 'num_ratings', 'avg_ratings']].copy()
    top_books = top_books.merge(
        books[['Book-Title', 'Book-Author', 'Image-URL-M']].drop_duplicates(subset=['Book-Title']),
        on='Book-Title',
        how='left',
    ).head(50)

    return render_template(
        'index.html',
        book_name=list(top_books['Book-Title'].fillna('Unknown').values),
        author=list(top_books['Book-Author'].fillna('Unknown').values),
        image=list(top_books['Image-URL-M'].fillna('').values),
        votes=list(top_books['num_ratings'].fillna(0).astype(int).values),
        rating=list(top_books['avg_ratings'].fillna(0).astype(float).values),
    )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommendation.html', data=[], book_titles=pt.index.tolist())


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = (request.form.get('user_input') or '').strip()
    if not user_input:
        return render_template(
            'recommendation.html',
            data=[],
            book_titles=pt.index.tolist(),
            error='Please enter a book title.',
            user_input='',
        )

    selected_title = title_lookup.get(normalize_title(user_input))
    if selected_title is None:
        return render_template(
            'recommendation.html',
            data=[],
            book_titles=pt.index.tolist(),
            error=f"'{user_input}' wasn't found. Check the title or choose one from the suggestions.",
            user_input=user_input,
        )

    index = np.where(pt.index == selected_title)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True,
    )[1:6]

    data = []
    for book_index, _ in similar_items:
        recommended_title = pt.index[book_index]
        temp_df = books[books['Book-Title'] == recommended_title]
        unique_book = temp_df.drop_duplicates('Book-Title').iloc[0]
        data.append([
            unique_book['Book-Title'],
            unique_book['Book-Author'],
            unique_book['Image-URL-M'],
        ])

    return render_template(
        'recommendation.html',
        data=data,
        book_titles=pt.index.tolist(),
        searched_title=selected_title,
        user_input=user_input,
    )


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)