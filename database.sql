CREATE TABLE patient (
    id          INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,

    leeft       INTEGER,
    gesl        INTEGER,
<<<<<<< HEAD
    diffgrad    INTEGER,
=======
    ct          INTEGER,
    cn          INTEGER,
>>>>>>> c73ac1903dcadbe482068c51a233d95e5b6d579b
    er_stat     INTEGER,
    pr_stat     INTEGER,
    her2_stat   INTEGER,
    pos_lymf    INTEGER,
    ct          TEXT,
    cn          INTEGER,

    morf        INTEGER,
    tumorsoort  INTEGER,
    okd         INTEGER,
    org_chir    INTEGER,
    horm        INTEGER,
    rt          INTEGER,
    meta_rt     INTEGER,
    meta_chir   INTEGER
);

INSERT INTO patient (
    display_name,
    leeft,
    gesl,
    diffgrad,
    er_stat,
    pr_stat,
    her2_stat,
    pos_lymf,
    ct,
    cn,
    morf,
    tumorsoort,
    okd,
    org_chir,
    horm,
    rt,
    meta_rt,
    meta_chir
)
VALUES
<<<<<<< HEAD
    ('Damon Salvatore', 45, 1, 2, 1, 1, 0, 1, '1C', 1,
     8500, 501300, 1, 1, 0, 1, 0, 0),

    ('Elena Gilbert', 62, 2, 3, 1, 0, 0, 2, '2', 1,
     8481, 503200, 0, 1, 1, 1, 0, 0),

    ('Elijah Ziebler', 54, 1, 2, 1, 1, 1, 2, '4C', 1,
     8260, 501300, 0, 1, 2, 2, 0, 1),

    ('Klaus Krasz', 71, 1, 3, 0, 0, 1, 0, '1C', 0,
     8500, 502200, 1, 1, 2, 1, 1, 1),

    ('Katherine Pierce', 39, 2, 1, 1, 1, 0, 0, '1B', 0,
     8520, 502200, 1, 0, 1, 2, 0, 1),

    ('Enzo Zebler', 67, 1, 3, 0, 0, 0, 2, '1C', 1,
     8260, 501300, 1, 0, 1, 0, 1, 0);
=======
    ('Patient 1', 45, 1, 3, 2, 1, 1, 0, 2, 1),
    ('Patient 2', 62, 0, 2, 2, 1, 0, 0, 3, 2),
    ('Patient 3', 54, 1, 3, 1, 1, 1, 1, 2, 3),
    ('Patient 4', 71, 1, 1, 0, 0, 0, 1, 3, 0),
    ('Patient 5', 39, 0, 0, 0, 1, 1, 0, 1, 0),
    ('Patient 6', 67, 1, 1, 2, 0, 0, 0, 3, 2);
>>>>>>> c73ac1903dcadbe482068c51a233d95e5b6d579b
