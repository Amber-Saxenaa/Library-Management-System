CREATE DATABASE library_db;

CREATE TABLE authors (
    author_id     SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    country       VARCHAR(50)
);

CREATE TABLE books (
    book_id       SERIAL PRIMARY KEY,
    title         VARCHAR(200) NOT NULL,
    author_id     INT REFERENCES authors(author_id) ON DELETE SET NULL,
    genre         VARCHAR(50),
    isbn          VARCHAR(20) UNIQUE,
    total_copies  INT NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    year_published INT
);

CREATE TABLE members (
    member_id     SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    email         VARCHAR(120) UNIQUE NOT NULL,
    phone         VARCHAR(15),
    join_date     DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE loans (
    loan_id       SERIAL PRIMARY KEY,
    book_id       INT NOT NULL REFERENCES books(book_id),
    member_id     INT NOT NULL REFERENCES members(member_id),
    loan_date     DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date      DATE NOT NULL,
    return_date   DATE,                      
    CHECK (due_date >= loan_date)
);
