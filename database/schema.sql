DROP TABLE IF EXISTS USERS;
CREATE TABLE USERS
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    USERNAME    VARCHAR(32)             NOT NULL UNIQUE,
    PASSWORD    VARCHAR(32)             NOT NULL
);

DROP TABLE IF EXISTS ONLINEMUSICS;
CREATE TABLE ONLINEMUSICS
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    NAME        VARCHAR(128)            NOT NULL UNIQUE,
    AUTHOR      VARCHAR(32)             NOT NULL,
    CREATETIME  DATETIME                NOT NULL,
    MUSICLINK   VARCHAR(128)            NOT NULL,
    IMGLINK     VARCHAR(128)            NOT NULL,
    UPVOTENUM   INTEGER                 NOT NULL,
    VIEWNUM     INTEGER                 NOT NULL
);

DROP TABLE IF EXISTS COMMENTS;
CREATE TABLE COMMENTS
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    COMMENTID   VARCHAR(128)            NOT NULL UNIQUE,
    MUSICID     VARCHAR(128)            NOT NULL,
    AUTHOR      VARCHAR(128)            NOT NULL,
    CREATETIME  VARCHAR(128)            NOT NULL,
    COMMENT     VARCHAR(128)            NOT NULL
);
