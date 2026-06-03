CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    source_device TEXT,
    local_id TEXT,
    type TEXT,
    note TEXT,
    address TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    status TEXT DEFAULT 'new',
    photo_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
