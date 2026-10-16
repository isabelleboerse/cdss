

CREATE TABLE patient (
    id          INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    leeft       INTEGER,
    gesl        INTEGER,
    ct          TEXT,
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
    ('Damon Salvatore', 45, 1, "1C", 1, 1, 1, 0, 2, 1),
    ('Elena Gilbert', 62, 2, "2", 1, 1, 0, 0, 3, 2),
    ('Elijah Ziebler', 54, 1, "4C", 1, 1, 1, 1, 2, 2),
    ('Klaus Krasz', 71, 1, "1C", 0, 0, 0, 1, 3, 0),
    ('Katherine Pierce', 39, 2, "1B", 0, 1, 1, 0, 1, 0),
    ('Enzo Zebler', 67, 1, "1C", 1, 0, 0, 0, 3, 2);