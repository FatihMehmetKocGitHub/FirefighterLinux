CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    source_device TEXT,
    local_id INTEGER,
    type TEXT,
    note TEXT,
    address TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    status TEXT,
    photo_path TEXT,
    created_at TEXT,
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
