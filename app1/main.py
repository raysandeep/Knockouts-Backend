from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router.main_router import api_router
from core import settings


app = FastAPI(
    title=settings.PROJECT_NAME
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=[str(method) for method in settings.CORS_ALLOW_METHODS],
        allow_headers=[str(header) for header in settings.CORS_ALLOW_HEADERS],
    )

app.include_router(api_router)