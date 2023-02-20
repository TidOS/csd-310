-- create users in case they don't exist so we can be sure they get deleted without error
CREATE USER 'whatabook_user'@'localhost';
CREATE USER 'whatabook_user'@'newrig.attlocal.net';

-- delete them so we can remake them with a password
DROP USER 'whatabook_user'@'localhost';
DROP USER 'whatabook_user'@'newrig.attlocal.net';

-- create whatabook_user and grant them all privileges to the whatabook database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED BY 'MySQL8IsGreat!';
CREATE USER 'whatabook_user'@'newrig.attlocal.net' IDENTIFIED BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'newrig.attlocal.net';

-- ignore constraints so we can drop tables
SET FOREIGN_KEY_CHECKS = 0;

-- drop tables if they exist
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS wishlist;
DROP TABLE IF EXISTS user;

-- turn contstraints back on
SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    loc         VARCHAR(500)    NOT NULL,
    open_hour   INT             NOT NULL,
    close_hour  INT             NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    summary     VARCHAR(500),
    PRIMARY KEY(book_id)
);

CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
        REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
        REFERENCES user(user_Id)
);

-- INSERT STATEMENTS
-- insert 1 store
INSERT INTO store(loc, open_hour, close_hour)
    VALUES('Nashville', 8, 20);

-- insert 9 books
INSERT INTO book(book_name, author, summary)
    VALUES('The Rabbit Hutch: A Novel', 'Tess Gunty', 'A book about rabbits and hutches');

INSERT INTO book(book_name, author, summary)
    VALUES('Reckless Girls', 'Rachel Hawkins', 'These girls cause trouble');

INSERT INTO book(book_name, author, summary)
    VALUES('Carrie Soto is Back', 'Taylor Jenkins', 'She was gone...now she is back');

INSERT INTO book(book_name, author, summary)
    VALUES('Sea of Tranquility', 'Emily St. John Mandel', 'A peaceful sea that is not peaceful');

INSERT INTO book(book_name, author, summary)
    VALUES('Our Missing Hearts', 'Celeste Ng', 'When hearts go missing and we need them back.');

INSERT INTO book(book_name, author)
    VALUES('Electric Idol (Dark Olympus #2)', 'Kaleen Robert');

INSERT INTO book(book_name, author, summary)
    VALUES('Terms and Conditions', 'Laruen Asher', 'To join the billionaire club, you need to agree to the rules');

INSERT INTO book(book_name, author, summary)
    VALUES('Notes on an Execution', 'Danya Kufaka', 'A robotic executioner details its travels');

INSERT INTO book(book_name, author, summary)
    VALUES('Not another book', 'Anonymous', 'This is not a book.');

--insert 3 users
INSERT INTO user(first_name, last_name) 
    VALUES('Jordan', 'Thomas');

INSERT INTO user(first_name, last_name)
    VALUES('Bill', 'Clinton');

INSERT INTO user(first_name, last_name)
    VALUES('John', 'Johnson');

--insert 1 wishlist item for each user
INSERT INTO wishlist(user_id, book_id) 
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Jordan'), 
        (SELECT book_id FROM book WHERE book_name = 'Our Missing Hearts')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Bill'),
        (SELECT book_id FROM book WHERE book_name = 'Reckless Girls')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'John'),
        (SELECT book_id FROM book WHERE book_name = 'Not another book')
    );