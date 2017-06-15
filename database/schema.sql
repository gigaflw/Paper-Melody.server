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
    AUTHORID    INTEGER                 NOT NULL,
    CREATETIME  DATETIME                NOT NULL,
    MUSICNAME   VARCHAR(64)             NOT NULL,
    IMGNAME     VARCHAR(64)             NOT NULL,
    UPVOTENUM   INTEGER                 NOT NULL,
    VIEWNUM     INTEGER                 NOT NULL
);

DROP TABLE IF EXISTS COMMENTS;
CREATE TABLE COMMENTS
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    MUSICID     INTEGER                 NOT NULL,
    AUTHOR      VARCHAR(32)             NOT NULL,
    AUTHORID    INTEGER                 NOT NULL,
    CREATETIME  VARCHAR(64)             NOT NULL,
    COMMENT     VARCHAR(256)            NOT NULL
);

DROP TABLE IF EXISTS FAVORITES;
CREATE TABLE FAVORITES
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    AUTHORID    INTEGER                 NOT NULL,
    MUSICID     INTEGER                 NOT NULL
);

DROP TABLE IF EXISTS MESSAGES;
CREATE TABLE MESSAGES
(
    IND         INTEGER PRIMARY KEY     NOT NULL,
    AUTHOR      VARCHAR(32)             NOT NULL,
    AUTHORID    INTEGER                 NOT NULL,
    REPLYUSERID INTEGER                 NOT NULL,
    CREATETIME  DATETIME                NOT NULL,
    NEWS        INTEGER                 NOT NULL,
    MESSAGE     VARCHAR(256)            NOT NULL
);