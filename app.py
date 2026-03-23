from flask import Flask, render_template, request, jsonify
import sqlite3

# ✅ Step 1: Create app FIRST
app = Flask(__name__)

# ✅ Step 2: DB function
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            content TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# ✅ Step 3: Routes AFTER app defined

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save', methods=['POST'])
def save_note():
    data = request.json

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT id FROM notes WHERE date=? AND type=?", (data['date'], data['type']))
    existing = c.fetchone()

    if existing:
        c.execute("UPDATE notes SET content=? WHERE date=? AND type=?",
                  (data['content'], data['date'], data['type']))
    else:
        c.execute("INSERT INTO notes (date, type, content) VALUES (?, ?, ?)",
                  (data['date'], data['type'], data['content']))

    conn.commit()
    conn.close()

    return jsonify({"status": "saved"})


@app.route('/get/<date>/<type>')
def get_notes(date, type):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("SELECT id, content FROM notes WHERE date=? AND type=?", (date, type))
    notes = c.fetchall()

    conn.close()

    return jsonify([{"id": n[0], "content": n[1]} for n in notes])


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_note(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})


# ✅ Step 4: Run app LAST
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)