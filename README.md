## Migrations

To run the database migrations, make sure that alembic and its dependencies are installed:


Then set DATABASE_URL to point to your database:

```powershell
$env:DATABASE_URL = "postgresql://user:password@host/database"
```

Finally, run the migrations using alembic:

```bash
alembic -c alembic.ini revision -m "test" --autogenerate
alembic -c alembic.ini upgrade head
```