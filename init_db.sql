CREATE TABLE IF NOT EXISTS author (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

INSERT INTO author (name) VALUES
    ('Author 1'),
    ('Author 2'),
    ('Author 3');

CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES author (id)
);

INSERT INTO book (title, author_id) VALUES
    ('Book 1', 1),
    ('Book 2', 2),
    ('Book 3', 3);
