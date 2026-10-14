

CREATE TABLE patient (
    id          INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    leeft       INTEGER,
    gesl        INTEGER,
    ct          INTEGER,
    cn          INTEGER,
    er_stat     INTEGER,
    pr_stat     INTEGER,
    her2_stat   INTEGER,
    diffgrad    INTEGER,
    pos_lymf    INTEGER
);

INSERT INTO patient
    (display_name, leeft, gesl, ct, cn,
     er_stat, pr_stat, her2_stat, diffgrad, pos_lymf)
VALUES
    ('Patient 1', 45, 1, 3, 2, 1, 1, 0, 2, 1),
    ('Patient 2', 62, 0, 2, 2, 1, 0, 0, 3, 2),
    ('Patient 3', 54, 1, 3, 1, 1, 1, 1, 2, 3),
    ('Patient 4', 71, 1, 1, 0, 0, 0, 1, 3, 0),
    ('Patient 5', 39, 0, 0, 0, 1, 1, 0, 1, 0),
    ('Patient 6', 67, 1, 1, 2, 0, 0, 0, 3, 2);