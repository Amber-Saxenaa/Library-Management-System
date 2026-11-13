"""Library Management System - web page on top of your PostgreSQL database.

Reads are public. Create / update / delete need the password (default: AMBER).
Every request talks to PostgreSQL directly, so changes made in SQL (psql, pgAdmin...)
show up on the page, and changes made on the page are written to SQL.
"""
import os
import hmac
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, session, render_template

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-before-deploying")

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/library_db"
)
PASSWORD = os.environ.get("ADMIN_PASSWORD", "AMBER")

# Whitelist of tables/columns. Only these names are ever placed in SQL text.
TABLES = {
    "authors": {"pk": "author_id", "cols": ["name", "country"]},
    "books": {
        "pk": "book_id",
        "cols": ["title", "author_id", "genre", "isbn", "total_copies", "year_published"],
    },
    "members": {"pk": "member_id", "cols": ["name", "email", "phone", "join_date"]},
    "loans": {
        "pk": "loan_id",
        "cols": ["book_id", "member_id", "loan_date", "due_date", "return_date"],
    },
}


def db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)


def clean(row):
    """Make dates JSON-friendly (YYYY-MM-DD)."""
    return {k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in row.items()}


def run(sql, params=(), fetch=False):
    conn = db()
    try:
        with conn, conn.cursor() as cur:  # commits on success, rolls back on error
            cur.execute(sql, params)
            return [clean(r) for r in cur.fetchall()] if fetch else None
    finally:
        conn.close()


def table_or_404(name):
    if name not in TABLES:
        return None
    return TABLES[name]


@app.before_request
def require_login_for_writes():
    if request.path.startswith("/api/") and request.method in ("POST", "PUT", "DELETE"):
        if request.path != "/api/login" and not session.get("ok"):
            return jsonify(error="Locked. Enter the password to make changes."), 401


@app.errorhandler(psycopg2.Error)
def db_error(e):
    msg = (e.diag.message_primary if e.diag and e.diag.message_primary else str(e)).strip()
    if e.diag and e.diag.message_detail:
        msg += " - " + e.diag.message_detail
    return jsonify(error=msg), 400


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/login")
def login():
    given = (request.json or {}).get("password", "")
    if hmac.compare_digest(given.encode(), PASSWORD.encode()):
        session["ok"] = True
        return jsonify(ok=True)
    return jsonify(error="Wrong password."), 401


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/status")
def status():
    return jsonify(unlocked=bool(session.get("ok")))


@app.get("/api/<table>")
def list_rows(table):
    t = table_or_404(table)
    if not t:
        return jsonify(error="Unknown table"), 404
    rows = run(f"SELECT * FROM {table} ORDER BY {t['pk']}", fetch=True)
    return jsonify(rows)


def values_from(t, data, for_insert):
    cols, vals = [], []
    for c in t["cols"]:
        v = data.get(c)
        v = None if v is None or str(v).strip() == "" else str(v).strip()
        if for_insert and v is None:
            continue  # let the column default / NULL apply
        cols.append(c)
        vals.append(v)
    return cols, vals


@app.post("/api/<table>")
def create_row(table):
    t = table_or_404(table)
    if not t:
        return jsonify(error="Unknown table"), 404
    cols, vals = values_from(t, request.json or {}, True)
    if cols:
        sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})"
    else:
        sql = f"INSERT INTO {table} DEFAULT VALUES"
    run(sql, vals)
    return jsonify(ok=True), 201


@app.put("/api/<table>/<int:row_id>")
def update_row(table, row_id):
    t = table_or_404(table)
    if not t:
        return jsonify(error="Unknown table"), 404
    cols, vals = values_from(t, request.json or {}, False)
    sets = ", ".join(f"{c} = %s" for c in cols)
    run(f"UPDATE {table} SET {sets} WHERE {t['pk']} = %s", vals + [row_id])
    return jsonify(ok=True)


@app.delete("/api/<table>/<int:row_id>")
def delete_row(table, row_id):
    t = table_or_404(table)
    if not t:
        return jsonify(error="Unknown table"), 404
    run(f"DELETE FROM {table} WHERE {t['pk']} = %s", (row_id,))
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
