from contextlib import asynccontextmanager
from fastapi import FastAPI
import fastapi_cdn_host
from starlette.middleware.cors import CORSMiddleware
import sys
from AAA.requireToken import TokenRefreshMiddleware
from AAA.loggerConfig import appendToLogger
import logging
import config
from cache import cache_object
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


appendToLogger()
logger = logging.getLogger(__name__)

config.logConfig()

try:
    # Load environment variables
    from config import Config
    # Import routers
    from apps.dashboard.endpoints import router as dashboard_router
    from apps.lists.endpoints import router as lists_router
    from apps.summary.endpoints import router as summary_router
    from apps.actions.endpoints import router as actions_router
    from apps.extras.endpoints import router as extras_router
    from apps.dashboardAgent.endpoints import router as dashboardAgents_router
    from MongoAtlas.DB_endpoints import router as database_router

except Exception as e:
    logger.error("Error loading environment variables: " + str(e))
    sys.exit(1)

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache_object.startup(app, scheduler)

    scheduler.start()

    yield

    await cache_object.shutdown(app, scheduler)

    scheduler.shutdown()

logger.info("Starting the FastAPI app")

try:
    app = FastAPI(
        debug=Config.DEBUG, 
        title="Ig-drasil connect API", 
        description="API for Ig-drasil connect dashboard", 
        version="0.1.0", 
        redoc_url="/docs", docs_url="/swagger",
        lifespan=lifespan)

    # change docs cdn host
    fastapi_cdn_host.patch_docs(app, docs_cdn_host='https://gcore.jsdelivr.net/npm')

    # Add middleware for token refresh
    # app.add_middleware(TokenRefreshMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(dashboard_router)
    app.include_router(lists_router)
    app.include_router(summary_router)
    app.include_router(actions_router)
    app.include_router(extras_router)
    app.include_router(database_router)
    app.include_router(dashboardAgents_router)

    @app.get("/")
    def read_root():
        return {"Hello": "World  >_<"}

    logger.info("FastAPI app started without errors")
except Exception as e:
    logger.critical(f"Error starting the FastAPI app: {e}")

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting the FastAPI app programmatically on {Config.HOST}:{Config.PORT}")
    uvicorn.run(app=app, host=Config.HOST, port=int(Config.PORT), log_level="debug" if Config.DEBUG else "info")