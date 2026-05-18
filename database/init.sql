CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    contact TEXT NOT NULL,
    service TEXT NOT NULL,
    status TEXT NOT NULL,
    fee INTEGER NOT NULL,
    added TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
    inv_id TEXT NOT NULL,
    client TEXT NOT NULL,
    description TEXT NOT NULL,
    amount INTEGER NOT NULL,
    status TEXT NOT NULL,
    due_date TEXT,
    created TEXT NOT NULL
);