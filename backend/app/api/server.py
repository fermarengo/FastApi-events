from app.admin.auth import authentication_backend
from app.admin.event import EventAdmin
from app.admin.question import QuestionAdmin
from app.admin.ticket import TicketAdmin, TicketOptionAdmin
from app.admin.user import UserAdmin
from app.api.routes import router as api_router
from app.core.config import settings
from app.db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin


def get_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    admin = Admin(app, engine, authentication_backend=authentication_backend)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # ---------- Admin dashboard ----------
    admin.add_view(EventAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(TicketAdmin)
    admin.add_view(TicketOptionAdmin)
    admin.add_view(QuestionAdmin)

    return app


app = get_application()
