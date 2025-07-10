CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sentiment TEXT NOT NULL DEFAULT 'neutral',
    category TEXT NOT NULL DEFAULT 'другое'
);

CREATE TABLE IF NOT EXISTS check_spam (
    ip INTEGER PRIMARY KEY NOT NULL,
    number_requests TEXT NOT NULL,
    block TEXT NOT NULL DEFAULT 'open',
);
