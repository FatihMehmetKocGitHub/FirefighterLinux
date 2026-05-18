from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_DIR = os.path.expanduser("~/firefighter-server/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_CONFIG = {
    "host": "localhost",
    "database": "firefighter_central",
    "user": "firefighter",
    "password": "14531453",
}

def db():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/api/report", methods=["POST"])
def add_report():
    data = request.form

    photo_path = None
    if "photo" in request.files:
        photo = request.files["photo"]
        if photo.filename:
            filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + secure_filename(photo.filename)
            save_path = os.path.join(UPLOAD_DIR, filename)
            photo.save(save_path)
            photo_path = save_path

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reports
        (source_device, local_id, type, note, address, latitude, longitude, status, photo_path, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data.get("source_device", "unknown"),
        data.get("local_id"),
        data.get("type"),
        data.get("note"),
        data.get("address"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("status"),
        photo_path,
        data.get("created_at", datetime.now().isoformat())
    ))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"ok": True, "message": "Report saved"}), 200

@app.route("/api/reports", methods=["GET"])
def list_reports():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, source_device, type, note, address, latitude, longitude, status, photo_path, created_at, imported_at
        FROM reports
        ORDER BY id DESC
        LIMIT 100
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    reports = []
    for r in rows:
        reports.append({
            "id": r[0],
            "source_device": r[1],
            "type": r[2],
            "note": r[3],
            "address": r[4],
            "latitude": r[5],
            "longitude": r[6],
            "status": r[7],
            "photo_path": r[8],
            "created_at": r[9],
            "imported_at": str(r[10]),
        })

    return jsonify(reports)

@app.route("/", methods=["GET"])
def home():
    return "Firefighter Central API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
