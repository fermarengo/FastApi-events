# Mittin

Backend project for events API created with FastAPI, SQLAlchemy, SQLModel and Postgres

## SetUp

Create backend/.env file, check backend/.env_sample

Build the containers by executing the following command:

```bash
docker-compose up --build
```

Apply migrations, check Migrations section

To enter DB admin: http://127.0.0.1:8000/admin/

To see swagger endpoint doc: http://127.0.0.1:8000/docs

## Migrations

If there are any changes to the SQLAlchemy ORM models, enter to the container and run the command to generate `alembic` migrations.

```python
docker ps
docker exec -it <container_id> bash
PYTHONPATH=. alembic revision --autogenerate -m "<message>"
```

To run the migrations against the database:
```python
PYTHONPATH=. alembic upgrade head
```

## Connect to db
```python
docker-compose exec db psql -h localhost -U postgres --dbname=postgres
```

## Create user from console
Enter to event bachend container
```python
docker ps
docker exec -it <container_id> bash
```

Enter to the ipython console and run this code:
```python
from app.api.deps import get_db
from app.models.user import User
import hashlib

password = "Admin343$"
hashed_password = hashlib.sha256(password.encode()).hexdigest()
data = {
    "password": hashed_password,
    "email": "email@gmail.com",
    "nickname": "nickname",
    "is_admin": True,
    "full_name": "Daniel Perez"
}
user = User(**data)
db_session = next(get_db())
db_session.add(user)
db_session.commit()
```