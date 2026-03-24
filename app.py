from flask import Flask, render_template, request, jsonify
from supabase import create_client

# Supabase config
SUPABASE_URL = "https://dbwuherxwmxlnlrcssty.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRid3VoZXJ4d214bG5scmNzc3R5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQzNjc4NDQsImV4cCI6MjA4OTk0Mzg0NH0.kQkF8p290G3xya6JP5_pDE-Krnz3nicJMdVI41x6a2w"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')


# SAVE or UPDATE note
@app.route('/save', methods=['POST'])
def save_note():
    data = request.json

    # Check if note exists
    response = supabase.table("notes") \
        .select("*") \
        .eq("date", data['date']) \
        .eq("type", data['type']) \
        .execute()

    existing = response.data

    if existing:
        # UPDATE
        supabase.table("notes") \
            .update({"content": data['content']}) \
            .eq("date", data['date']) \
            .eq("type", data['type']) \
            .execute()
    else:
        # INSERT
        supabase.table("notes").insert({
            "date": data['date'],
            "type": data['type'],
            "content": data['content']
        }).execute()

    return jsonify({"status": "saved"})


# GET notes
@app.route('/get/<date>/<type>')
def get_notes(date, type):
    response = supabase.table("notes") \
        .select("*") \
        .eq("date", date) \
        .eq("type", type) \
        .execute()

    return jsonify(response.data)


# DELETE note
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_note(id):
    supabase.table("notes") \
        .delete() \
        .eq("id", id) \
        .execute()

    return jsonify({"status": "deleted"})


# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

