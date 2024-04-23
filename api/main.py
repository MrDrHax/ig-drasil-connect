from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import sys

try:
    # Load environment variables
    from config import Config
    # Import routers
    from apps.dashboard.endpoints import router as dashboard_router
    from apps.lists.endpoints import router as lists_router
    from apps.summary.endpoints import router as summary_router
    from apps.actions.endpoints import router as actions_router
    from apps.extras.endpoints import router as extras_router
except ImportError:
    # Load environment variables
    from .config import Config

    # Import routers
    from .apps.dashboard.endpoints import router as dashboard_router
    from .apps.lists.endpoints import router as lists_router
    from .apps.summary.endpoints import router as summary_router
    from .apps.actions.endpoints import router as actions_router
    from .apps.extras.endpoints import router as extras_router

app = FastAPI(debug=Config.DEBUG, title="Ig-drasil connect API", description="API for Ig-drasil connect dashboard", version="0.1.0", redoc_url="/docs", docs_url="/swagger")

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

@app.get("/")
def read_root():
    return {"Hello": "World  >_<"}