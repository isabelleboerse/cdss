CREATE TABLE patient (
    id          INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,

    leeft       INTEGER,
    gesl        INTEGER,
    diffgrad    INTEGER,
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
