from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_DIR = os.path.expanduser("~/firefighter-server/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DB_CONFIG = {
    "host": "10.15.162.1",
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
        data.get("source_device", "central-dashboard"),
        data.get("local_id"),
        data.get("type", "deprem"),
        data.get("note", ""),
        data.get("address", ""),
        data.get("latitude"),
        data.get("longitude"),
        data.get("status", "critical"),
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
        LIMIT 500
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
            "created_at": str(r[9]),
            "imported_at": str(r[10]),
        })

    return jsonify(reports)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source_device, type, note, address, latitude, longitude, status, photo_path, created_at, imported_at
        FROM reports
        ORDER BY id DESC
        LIMIT 500
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
            "created_at": str(r[9]),
            "imported_at": str(r[10]),
        })

    critical_count = len([r for r in reports if str(r["status"]).lower() == "critical"])
    device_count = len(set([r["source_device"] for r in reports if r["source_device"]]))

    html = """
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Firefighter Central Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
body{margin:0;font-family:Arial,sans-serif;background:#111827;color:#f9fafb}
header{padding:16px 24px;background:#7f1d1d;border-bottom:3px solid #ef4444}
header h1{margin:0;font-size:24px}
header p{margin:4px 0 0;color:#fecaca}
.stats{display:flex;gap:12px;padding:16px;flex-wrap:wrap}
.card{background:#1f2937;border:1px solid #374151;border-radius:10px;padding:14px;min-width:160px}
.card strong{display:block;font-size:28px;color:#f87171}
#map{height:520px;margin:0 16px 16px;border-radius:10px;border:1px solid #374151}
.panel{margin:16px;padding:14px;background:#1f2937;border:1px solid #374151;border-radius:10px}
input,select,button{padding:9px;margin:4px;border-radius:6px;border:1px solid #374151}
button{background:#dc2626;color:white;cursor:pointer}
table{width:calc(100% - 32px);margin:16px;border-collapse:collapse;background:#1f2937;border-radius:10px;overflow:hidden}
th,td{padding:10px;border-bottom:1px solid #374151;text-align:left;font-size:14px}
th{background:#991b1b}
.critical{color:#fca5a5;font-weight:bold}
.muted{color:#9ca3af}
</style>
</head>
<body>
<header>
<h1>Firefighter Central Dashboard</h1>
<p>Haritaya tıkla, deprem/olay konumunu direkt veritabanına kaydet.</p>
</header>

<div class="stats">
<div class="card"><span>Toplam Olay</span><strong>{{ reports|length }}</strong></div>
<div class="card"><span>Kritik</span><strong>{{ critical_count }}</strong></div>
<div class="card"><span>Cihaz</span><strong>{{ device_count }}</strong></div>
</div>

<div class="panel">
<b>Yeni Deprem / Olay İşaretle</b><br>
<input id="type" value="deprem" placeholder="Olay türü">
<input id="note" placeholder="Not">
<input id="address" placeholder="Adres">
<select id="status">
<option value="critical">critical</option>
<option value="open">open</option>
<option value="closed">closed</option>
</select>
<span>Lat: <b id="latText">-</b></span>
<span>Lon: <b id="lonText">-</b></span>
<button onclick="saveClickedLocation()">Kaydet</button>
</div>

<div id="map"></div>

<table>
<thead>
<tr>
<th>ID</th><th>Cihaz</th><th>Tür</th><th>Not</th><th>Adres</th><th>Durum</th><th>Tarih</th>
</tr>
</thead>
<tbody>
{% for r in reports %}
<tr>
<td>{{ r.id }}</td>
<td>{{ r.source_device }}</td>
<td>{{ r.type }}</td>
<td>{{ r.note }}</td>
<td>{{ r.address }}</td>
<td class="{{ 'critical' if r.status == 'critical' else '' }}">{{ r.status }}</td>
<td class="muted">{{ r.created_at }}</td>
</tr>
{% endfor %}
</tbody>
</table>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const reports = {{ reports_json|safe }};
let selectedLat = null;
let selectedLon = null;
let selectedMarker = null;

const map = L.map('map').setView([39.0, 35.0], 6);

L.tileLayer('https://tile.openstreetmap.de/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

reports.forEach(r => {
    const lat = parseFloat(r.latitude);
    const lon = parseFloat(r.longitude);
    if (!isNaN(lat) && !isNaN(lon)) {
        L.marker([lat, lon]).addTo(map).bindPopup(`
            <b>${r.type || '-'}</b><br>
            ${r.note || '-'}<br>
            <b>Adres:</b> ${r.address || '-'}<br>
            <b>Durum:</b> ${r.status || '-'}<br>
            <b>Cihaz:</b> ${r.source_device || '-'}
        `);
    }
});

map.on('click', function(e) {
    selectedLat = e.latlng.lat.toFixed(6);
    selectedLon = e.latlng.lng.toFixed(6);

    document.getElementById("latText").innerText = selectedLat;
    document.getElementById("lonText").innerText = selectedLon;

    if (selectedMarker) {
        map.removeLayer(selectedMarker);
    }

    selectedMarker = L.marker([selectedLat, selectedLon]).addTo(map)
        .bindPopup("Seçilen konum<br>Lat: " + selectedLat + "<br>Lon: " + selectedLon)
        .openPopup();
});

function saveClickedLocation() {
    if (!selectedLat || !selectedLon) {
        alert("Önce haritadan konum seç.");
        return;
    }

    const form = new FormData();
    form.append("source_device", "central-dashboard");
    form.append("local_id", "0");
    form.append("type", document.getElementById("type").value || "deprem");
    form.append("note", document.getElementById("note").value || "-");
    form.append("address", document.getElementById("address").value || "-");
    form.append("latitude", selectedLat);
    form.append("longitude", selectedLon);
    form.append("status", document.getElementById("status").value || "critical");

    fetch("/api/report", {
        method: "POST",
        body: form
    })
    .then(r => r.json())
    .then(data => {
        if (data.ok) {
            alert("Kayıt veritabanına aktarıldı.");
            window.location.reload();
        } else {
            alert("Kayıt başarısız.");
        }
    })
    .catch(err => {
        alert("Hata: " + err);
    });
}
</script>
</body>
</html>
    """

    return render_template_string(
        html,
        reports=reports,
        reports_json=json.dumps(reports, default=str),
        critical_count=critical_count,
        device_count=device_count
    )

@app.route("/", methods=["GET"])
def home():
    return "Firefighter Central API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
