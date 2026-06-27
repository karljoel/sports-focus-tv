from flask import Flask, render_template

app = Flask(__name__)

# Our list of matches
matches = [
    # 🔴 LIVE TONIGHT - Wednesday, June 24
    {
        "id": 1,
        "home": "Croatia",
        "away": "England",
        "league": "World Cup - Group B",
        "date": "2026-06-24",
        "time": "23:00 EAT",
        "stream_link": '<iframe id="player" width="1100" height="619" allowfullscreen="" loading="eager" fetchpriority="high" referrerpolicy="no-referrer-when-downgrade" allow="autoplay; fullscreen; picture-in-picture" src="https://912acsss8af382.shootny.com/playerv5.php?match=4627921&amp;key=9f39972b67d6ce22189507d008acwc26">\n                </iframe>'
    },
    {
        "id": 2,
        "home": "Bosnia and Herzegovina",
        "away": "Qatar",
        "league": "World Cup - Group B",
        "date": "2026-06-24",
        "time": "23:00 EAT",
        "stream_link": None
    },
    # Thursday, June 25
    {
        "id": 3,
        "home": "Morocco",
        "away": "Haiti",
        "league": "World Cup - Group C",
        "date": "2026-06-25",
        "time": "02:00 EAT",
        "stream_link": None
    },
    {
        "id": 4,
        "home": "Scotland",
        "away": "Brazil",
        "league": "World Cup - Group C",
        "date": "2026-06-25",
        "time": "02:00 EAT",
        "stream_link": None
    },
    {
        "id": 5,
        "home": "South Africa",
        "away": "South Korea",
        "league": "World Cup - Group A",
        "date": "2026-06-25",
        "time": "05:00 EAT",
        "stream_link": None
    },
    {
        "id": 6,
        "home": "Czech Republic",
        "away": "Mexico",
        "league": "World Cup - Group A",
        "date": "2026-06-25",
        "time": "05:00 EAT",
        "stream_link": None
    },
    # Friday, June 26
    {
        "id": 7,
        "home": "Curacao",
        "away": "Ivory Coast",
        "league": "World Cup - Group E",
        "date": "2026-06-26",
        "time": "00:00 EAT",
        "stream_link": None
    },
    {
        "id": 8,
        "home": "Ecuador",
        "away": "Germany",
        "league": "World Cup - Group E",
        "date": "2026-06-26",
        "time": "00:00 EAT",
        "stream_link": None
    },
    {
        "id": 9,
        "home": "Tunisia",
        "away": "Netherlands",
        "league": "World Cup - Group F",
        "date": "2026-06-26",
        "time": "03:00 EAT",
        "stream_link": None
    },
    {
        "id": 10,
        "home": "Japan",
        "away": "Sweden",
        "league": "World Cup - Group F",
        "date": "2026-06-26",
        "time": "03:00 EAT",
        "stream_link": None
    },
    {
        "id": 11,
        "home": "Turkey",
        "away": "USA",
        "league": "World Cup - Group D",
        "date": "2026-06-26",
        "time": "06:00 EAT",
        "stream_link": None
    },
    {
        "id": 12,
        "home": "Paraguay",
        "away": "Australia",
        "league": "World Cup - Group D",
        "date": "2026-06-26",
        "time": "06:00 EAT",
        "stream_link": None
    },
    # Saturday, June 27
    {
        "id": 13,
        "home": "Cape Verde",
        "away": "Saudi Arabia",
        "league": "World Cup - Group H",
        "date": "2026-06-27",
        "time": "04:00 EAT",
        "stream_link": None
    },
    {
        "id": 14,
        "home": "Uruguay",
        "away": "Spain",
        "league": "World Cup - Group H",
        "date": "2026-06-27",
        "time": "04:00 EAT",
        "stream_link": None
    },
    {
        "id": 15,
        "home": "New Zealand",
        "away": "Belgium",
        "league": "World Cup - Group G",
        "date": "2026-06-27",
        "time": "07:00 EAT",
        "stream_link": None
    },
    {
        "id": 16,
        "home": "Egypt",
        "away": "Iran",
        "league": "World Cup - Group G",
        "date": "2026-06-27",
        "time": "07:00 EAT",
        "stream_link": None
    }
]

@app.route('/')
def home():
    return render_template('index.html', matches=matches)

@app.route('/match/<int:match_id>')
def match_page(match_id):
    match = None
    for m in matches:
        if m['id'] == match_id:
            match = m
            break
    return render_template('match.html', match=match)

if __name__ == '__main__':
    app.run(debug=True)