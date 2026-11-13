# Library Manager (Flask + PostgreSQL)

A web page that reads and writes your `library_db` database. Viewing is open; adding, editing and deleting need the password.

## 1. Set up the database (once)
Your SQL uses `SERIAL`, so this is PostgreSQL.
```
psql -U postgres -c "CREATE DATABASE library_db;"
psql -U postgres -d library_db -f db1.sql   # tables (skip its CREATE DATABASE line error if it says exists)
psql -U postgres -d library_db -f db2.sql   # sample data
```

## 2. Run the app
```
pip install -r requirements.txt
# Windows (cmd):  set DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD@localhost:5432/library_db
# Mac/Linux:      export DATABASE_URL=postgresql://postgres:YOUR_DB_PASSWORD@localhost:5432/library_db
python app.py
```
Open http://localhost:5000

## How the two-way sync works
- Page -> SQL: every Add / Edit / Delete runs an INSERT / UPDATE / DELETE on PostgreSQL.
- SQL -> Page: the page re-reads the tables every 5 seconds. Run an `INSERT` in psql or pgAdmin and it appears on the page within 5 seconds.

## Password
Default is `AMBER`, checked on the server (not in the browser). Change it with the `ADMIN_PASSWORD` environment variable. Also set `SECRET_KEY` to any long random string.

## Files
- `app.py` - Flask server and CRUD API
- `templates/index.html` - the page
