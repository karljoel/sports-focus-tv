from flask import Flask, render_template

app = Flask(__name__)

# Our list of matches (we'll add more later)
matches = [
    {   "id": 1,
        "home": "Curacao",
        "away": "Ivory Coast",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "23:00",
        "stream_link": None
    },
    {   "id": 2,
        "home": "Ecuador",
        "away": "Germany",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "23:00",
        "stream_link": None
    },
    {   "id": 3,
        "home": "Tunisia",
        "away": "Netherlands",
        "league": "World Cup",
        "date": "2026-06-27",
        "time": "02:00",
        "stream_link": None
    },
    {   "id": 4,
        "home": "Japan",
        "away": "Sweden",
        "league": "World Cup",
        "date": "2026-06-27",
        "time": "02:00",
        "stream_link": None
     },
     {   "id": 5,
        "home": "Turkiye",
        "away": "USA",
        "league": "World Cup",
        "date": "2026-06-27",
        "time": "05:00",
        "stream_link": None
     },
     {   "id": 6,
        "home": "Paraguay",
        "away": "Australia",
        "league": "World Cup",
        "date": "2026-06-27",
        "time": "05:00",
        "stream_link": None
     }
]
@app.route('/')
def home():
    return render_template('index.html', matches=matches)

@app.route('/match/<int:match_id>')
def match_page(match_id):
    # Find the match with this ID
    match = None
    for m in matches:
        if m['id'] == match_id:
            match = m
            break
    return render_template('match.html', match=match)

if __name__ == '__main__':
    app.run(debug=True)