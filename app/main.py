import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

# Middlewares
from fastapi.middleware.cors import CORSMiddleware
from asgi_matomo import MatomoMiddleware
from umami_asgi import UmamiMiddleware

# Routers
from .versions import v1

# Settings
from .config import Settings

app = FastAPI()
config = Settings()

app.include_router(
    v1.router,
    prefix="/api/v1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if config.matomo_enabled:
    if config.matomo_url is None:
        raise Exception("Error: environment variable matomo_url is missing")

    if config.matomo_site_id is None:
        raise Exception("Error: environment variable matomo_site_id is missing")

    app.add_middleware(
        MatomoMiddleware,
        matomo_url=config.matomo_url,
        idsite=config.matomo_site_id,
    )
    print("enabled matomo integration")

if config.umami_enabled:
    if config.umami_url is None:
        raise Exception("Error: environment variable umami_url is missing")

    if config.umami_site_id is None:
        raise Exception("Error: environment variable umami_website_id is missing")

    app.add_middleware(
        UmamiMiddleware,
        api_endpoint=config.umami_url,
        website_id=config.umami_site_id,
    )
    print("enabled umami integration")

@app.get("/")
async def root():
    return RedirectResponse("/docs")

# for debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
