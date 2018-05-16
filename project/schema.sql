/* Setup */
CREATE TABLE IF NOT EXISTS password_storage (
    password TEXT PRIMARY KEY,
    breaches INTEGER default 0
);
