# alembic + multitenat dbs + flask + pydantic

App is using barebones flask, sqlalchemy and Unit Of Work pattern (simplified).

## Quick setup

```bash
brew install uv

uv sync
source .venv/bin/activate

cp example.env .env

docker compose up db-admin db

alembic upgrade head

gunicorn -w 1 -t 0 --reload sqlalchemy_sandbox.main:app
```

## Testing

DB admin with pre-configured servers is listening on <http://localhost:8080>
Test requests are located in [test_requests.http](./tests/test_requests.http)
