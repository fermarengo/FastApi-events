import hashlib

import jwt
from app.api.deps import get_db
from app.core.config import settings
from app.db.session import engine
from app.models.user import User
from fastapi import APIRouter, Depends
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

Session = sessionmaker(bind=engine)


class AdminBackendAuth(AuthenticationBackend):
    """
    module createdin order to authenticate only users in admin site
    """

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        session = Session()
        user = session.query(User).filter(User.email==username, User.is_admin==True).first()
        print("print1")
        if user:
            print("User exists")
            # If we found user verify password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user.password == hashed_password:
                # if password is correct generate jwt token
                token = jwt.encode({'username': username}, settings.SECRET_KEY, algorithm='HS256')
                request.session.update({"token": token})
                return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # TODO: add functionality to expire token

        token = request.session.get("token")
        if not token:
            return False
        
        session = Session()
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if not session.query(User).filter(User.email == decoded_data.get('username')).first():
            return False

        return True

authentication_backend = AdminBackendAuth(secret_key=settings.SECRET_KEY)