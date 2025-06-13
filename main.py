from flask import Flask, request, redirect, url_for, render_template_string
import json
from datetime import datetime
import os

app = Flask(__name__)

DATA_FILE = 'journal.json'


def load_entries():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    return data


def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('entry', '').strip()
        if text:
            entries = load_entries()
            entries.append({
                'timestamp': datetime.utcnow().isoformat(),
                'entry': text,
                'mood': 'Unknown'
            })
            save_entries(entries)
        return redirect(url_for('index'))

    entries = load_entries()
    entries_sorted = sorted(entries, key=lambda x: x['timestamp'], reverse=True)
    template = '''
    <html>
    <head><title>Journal</title></head>
    <body>
        <h1>Journal</h1>
        <form method="POST">
            <textarea name="entry" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Submit">
        </form>
        <h2>Past Entries</h2>
        {% for e in entries %}
            <div>
                <strong>{{ e.timestamp }}</strong> ({{ e.mood }})<br>
                <pre>{{ e.entry }}</pre>
            </div>
            <hr>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(template, entries=entries_sorted)


if __name__ == '__main__':
    app.run(debug=True)
