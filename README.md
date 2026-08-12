# University data visualizations

This is the preserved baseline of a legacy Python 3.9 application. It reads
university data from MySQL and uses Bokeh to produce three charts in
`all_charts.html`.

## Repository layout

- `all.py` connects to MySQL, queries the legacy schema, builds the charts, and
  writes/opens the HTML output.
- `all_charts.html` is generated output. It remains tracked for now because it
  is the only viewable snapshot that does not require a configured database.
- `db/scheme_creation.sql` defines the seven legacy tables.
- `db/generate_*.sql` contains the seed data.
- `requirements.txt` preserves the original pinned Python environment.

## Database setup

The SQL files expect a MySQL database named `university`; they do not create
the database. After creating that database, load the files in dependency order:

1. `db/scheme_creation.sql`
2. `db/generate_persons.sql`
3. `db/generate_students.sql`
4. `db/generate_teachers.sql`
5. `db/generate_classes.sql`
6. `db/generate_rooms.sql`
7. `db/generate_classes_students.sql`
8. `db/generate_schedules.sql`

Important: `all.py` currently connects to a database named `uni`, while the
SQL files select `university`. This legacy mismatch is intentionally documented
rather than changed in this baseline. The database names must refer to the same
populated schema for the script to run.

## Python setup

Create and activate a Python 3.9 virtual environment:

```bash
python3.9 -m venv .venv
source .venv/bin/activate
```

Install the preserved dependencies:

```bash
python -m pip install -r requirements.txt
```

With MySQL running and the expected schema available, run:

```bash
python all.py
```

Bokeh writes `all_charts.html` and normally opens it in the default browser.
Running the script regenerates that tracked file with data from the local
database, so review its diff before committing it.

## Baseline constraints

The current database access, SQL queries, Bokeh charts, and pinned dependency
versions are deliberately unchanged. They should be tested against a populated
database before later refactoring or dependency upgrades.
