SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('doctor', 'technician', 'admin')) NOT NULL,
    avatar TEXT
);
CREATE TABLE IF NOT EXISTS image_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    size INTEGER NOT NULL,
    type TEXT NOT NULL,
    last_modified INTEGER NOT NULL,
    url TEXT NOT NULL,
    thumbnail TEXT,
    width INTEGER,
    height INTEGER,
    uploaded_at TEXT NOT NULL,  -- Se guarda como ISO string
    status TEXT CHECK(status IN ('uploading', 'uploaded', 'error', 'processing')) NOT NULL,
    error TEXT
);

CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_id INTEGER NOT NULL,
    pcos_probability REAL NOT NULL,
    confidence REAL NOT NULL,
    findings TEXT,            -- Podemos guardar como JSON string
    recommendations TEXT,     -- También como JSON string
    analyzed_at TEXT NOT NULL, -- Se guarda como ISO string
    status TEXT CHECK(status IN ('pending', 'processing', 'completed', 'error')) NOT NULL,
    error TEXT,
    FOREIGN KEY (image_id) REFERENCES image_files(id) ON DELETE CASCADE
);

"""