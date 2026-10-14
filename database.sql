

CREATE TABLE patient (
    id          INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    leeft       INTEGER,
    gesl        INTEGER,
    tum_afm     REAL,
    cstadium    TEXT,
    cn          TEXT,
    er_stat     INTEGER,
    pr_stat     INTEGER,
    her2_stat   INTEGER,
    diffgrad    INTEGER
);

INSERT INTO patient
    (display_name, leeft, gesl, tum_afm, cstadium, cn,
     er_stat, pr_stat, her2_stat, diffgrad)
VALUES
    ('Patient 1', 45, 2, 18.0, 'I',   'N0', 1, 1, 0, 2),
    ('Patient 2', 62, 2, 32.0, 'II',  'N1', 1, 0, 0, 3),
    ('Patient 3', 54, 2, 24.0, 'II',  'N0', 1, 1, 1, 2),
    ('Patient 4', 71, 2, 42.0, 'III', 'N2', 0, 0, 1, 3),
    ('Patient 5', 39, 2, 12.0, 'I',   'N0', 1, 1, 0, 1),
    ('Patient 6', 67, 2, 28.0, 'II',  'N1', 0, 0, 0, 3);