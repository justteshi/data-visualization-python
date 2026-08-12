# University data visualizations

This is the preserved baseline of a legacy Python 3.9 application. It reads
university data from MySQL and uses Bokeh to produce three charts in
`all_charts.html`.

## Repository layout

- `all.py` queries the legacy schema, builds the charts, and writes/opens the
  HTML output.
- `database.py` validates environment-based settings and creates MySQL
  connections.
- `.env.example` documents the local database configuration.
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

The SQL files select a database named `university`, which is also the database
name used by the included Docker setup. Set `DB_NAME` to the populated schema
that the application should query.

## Database configuration

Copy the safe example file to create local configuration:

```bash
cp .env.example .env
```

Then edit `.env` for the local MySQL installation:

```dotenv
DB_HOST=localhost
DB_PORT=3336
DB_NAME=university
DB_USER=root
DB_PASSWORD=change-me
```

All five variables must be present. `DB_PASSWORD` may be empty when the local
MySQL account has no password. The `.env` file is ignored by Git and must not be
committed. Environment variables already exported by the shell take precedence
over values in `.env`.

### Local MySQL with Docker

The included Compose service uses `DB_PORT` and `DB_PASSWORD` from `.env` and
loads the existing SQL files into a persistent MySQL 8.0 container. Use a
non-empty development password and set `DB_NAME=university`, then run:

```bash
docker compose up -d
docker compose ps
```

Initialization runs only when the `mysql_data` volume is empty. Stop the
container with `docker compose stop`; `docker compose down` also removes the
container but preserves the database volume.

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

The SQL queries, Bokeh charts, and existing pinned dependency versions are
deliberately unchanged. `python-dotenv` is included only to load ignored local
`.env` configuration. The application should be tested against a populated
database before later refactoring or dependency upgrades.
