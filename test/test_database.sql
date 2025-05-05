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


INSERT INTO device (id, name, country) VALUES
(
    0,
    "NextSeq 550",
    "USA"
),
(
    1,
    "SURFSeq 5000",
    "China"
);

INSERT INTO article (id, title) VALUES
(
    0,
    "Inferring pattern-driving intercellular flows from single-cell and spatial transcriptomics",
),
(
    1,
    "A human neural crest model reveals the developmental impact of neuroblastoma-associated chromosomal aberrations",
);


INSERT INTO application (record_id, device_id, article_id, seq_obj) VALUES
(
    0,
    1,
    0,
    "tumor, RNA",
),
(
    1,
    1,
    1,
    "PBMC, DNA",
);
