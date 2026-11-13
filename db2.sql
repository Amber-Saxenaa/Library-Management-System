-- Authors
INSERT INTO authors (name, country) VALUES
('George Orwell', 'UK'),
('J.K. Rowling', 'UK'),
('Chetan Bhagat', 'India'),
('Yuval Noah Harari', 'Israel'),
('Agatha Christie', 'UK');

-- Books
INSERT INTO books (title, author_id, genre, isbn, total_copies, year_published) VALUES
('1984', 1, 'Dystopian', '9780451524935', 3, 1949),
('Animal Farm', 1, 'Satire', '9780451526342', 2, 1945),
('Harry Potter and the Philosopher''s Stone', 2, 'Fantasy', '9780747532699', 5, 1997),
('Harry Potter and the Chamber of Secrets', 2, 'Fantasy', '9780747538493', 4, 1998),
('Five Point Someone', 3, 'Fiction', '9788129105944', 2, 2004),
('Sapiens', 4, 'History', '9780062316097', 3, 2011),
('Murder on the Orient Express', 5, 'Mystery', '9780062693662', 2, 1934);

-- Members
INSERT INTO members (name, email, phone, join_date) VALUES
('Aarav Sharma', 'aarav@example.com', '9876543210', '2024-01-15'),
('Priya Verma', 'priya@example.com', '9876543211', '2024-02-20'),
('Rahul Mehta', 'rahul@example.com', '9876543212', '2024-03-10'),
('Sneha Iyer', 'sneha@example.com', '9876543213', '2024-04-05'),
('Karan Patel', 'karan@example.com', '9876543214', '2024-05-01');

-- Loans (mix of returned + active + overdue)
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date) VALUES
(1, 1, '2024-06-01', '2024-06-15', '2024-06-10'),   -- returned on time
(3, 2, '2024-06-05', '2024-06-19', '2024-06-25'),   -- returned late
(6, 3, '2024-06-10', '2024-06-24', NULL),           -- active
(2, 1, '2024-06-12', '2024-06-26', NULL),           -- active
(7, 4, '2024-05-20', '2024-06-03', NULL),           -- OVERDUE (due date passed)
(4, 5, '2024-06-15', '2024-06-29', NULL),           -- active
(5, 2, '2024-06-18', '2024-07-02', '2024-06-28');   -- returned early
