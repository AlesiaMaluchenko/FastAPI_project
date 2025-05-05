CREATE TABLE IF NOT EXISTS device (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS article (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS application (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device (id),
    article_id INTEGER NOT NULL,
    FOREIGN KEY (article_id) REFERENCES article (id),
    seq_obj TEXT NOT NULL
);
