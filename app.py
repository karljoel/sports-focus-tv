from flask import Flask, render_template

app = Flask(__name__)

# Our list of matches (we'll add more later)
matches = [
    {
        "id": 1,
        "home": "Morocco",
        "away": "Haiti",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "01:00",
        "stream_link": "https://hesgoalss.hes-goals.mov/?m=4627938&p=87350"
    },
    {
        "id": 2,
        "home": "Scotland",
        "away": "Brazil",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "01:00",
        "stream_link": "https://hesgoalss.hes-goals.mov/?m=4627881&p=87350",
        "stream_link2": None,
        "stream_link3": None
    },
    {
        "id": 3,
        "home": "Czech Republic",
        "away": "Mexico",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "04:00",
        "stream_link": None 
    },
    {
        "id": 4,
        "home": "South Africa",
        "away": "South Korea",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "04:00",
        "stream_link": None
    },
    {   "id": 5,
        "home": "Curacao",
        "away": "Ivory Coast",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "23:00",
        "stream_link": None
    },
    {   "id": 6,
        "home": "Ecuador",
        "away": "Germany",
        "league": "World Cup",
        "date": "2026-06-25",
        "time": "23:00",
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