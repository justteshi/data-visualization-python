# University data visualizations

This project reads university data from MySQL, exports static analytics JSON,
and presents it through a Vite + Chart.js dashboard.

## Repository layout

- `src/database.py` loads `DB_*` environment variables and creates MySQL
  connections.
- `src/analytics.py` contains reusable, plain-Python analytics functions.
- `src/export_data.py` generates `public/data/analytics.json`.
- `db/scheme_creation.sql` creates the seven legacy tables.
- `db/generate_*.sql` contains the preserved seed data.

## Local Development

The complete local development environment runs in Docker: MySQL runs in the
`mysql` container and Python runs in the `python` container. Docker and Docker
Compose are the only host-machine prerequisites; no local Python installation
or Python dependencies are required.

Start (or rebuild) the environment:

```bash
docker compose up -d --build
```

Check service state. Wait until `mysql` is `healthy` before using the Python
container:

```bash
docker compose ps
```

Generate the static analytics data for a future frontend. The resulting
tracked file is `public/data/analytics.json` on the host:

```bash
docker compose exec python python src/export_data.py
```

Open a shell in the Python development container:

```bash
docker compose exec python sh
```

Inspect the initialized database from the MySQL container:

```bash
docker compose exec mysql mysql -uapp -papp uni
```

Stop the containers while preserving the database volume:

```bash
docker compose down
```

Reset all local database data and re-run initialization:

```bash
docker compose down -v
docker compose up -d --build
```

MySQL is reachable as `localhost:3306` from the host, but Docker services must
use `mysql:3306`. The Python service receives the values in `.env.example`
(`DB_HOST=mysql`, `DB_PORT=3306`, `DB_NAME=uni`, `DB_USER=app`,
`DB_PASSWORD=app`) through Compose. Copy it to `.env` only when you need to
override those local development defaults; `.env` is not committed. If a
legacy `.env` already exists, replace it with the new example values or remove
it so it does not override the Docker defaults.

### Database initialization

On an empty `mysql_data` volume, MySQL runs the existing SQL files through
`/docker-entrypoint-initdb.d/` in this order:

1. `scheme_creation.sql` (schema)
2. `generate_persons.sql`
3. `generate_students.sql`
4. `generate_teachers.sql`
5. `generate_classes.sql`
6. `generate_rooms.sql`
7. `generate_classes_students.sql`
8. `generate_schedules.sql`

The data files depend on the tables created first and on the previously loaded
person, student, teacher, class, and room records. Their `USE university`
directive was changed to `USE uni` so they load into the Compose database; no
schema or seed records were changed. MySQL is started with
`--lower-case-table-names=1` because this legacy schema and application use
table names with inconsistent casing. Initialization scripts run only for a new
volume.

## Analytics architecture

`src.analytics` contains the grade-distribution, enrollment-by-gender/year,
and study-duration calculations and returns plain Python values.
`src.export_data` serializes those results to static JSON for the dashboard.
Database connection configuration remains isolated in `src.database`.

## Frontend development

The dashboard foundation uses Vite and vanilla JavaScript. It reads no live
analytics values yet; future frontend work will consume the static
`public/data/analytics.json` export.

```bash
npm install
npm run dev
```

Create a production build or preview it locally with:

```bash
npm run build
npm run preview
```
