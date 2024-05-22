from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from starlette.middleware.cors import CORSMiddleware
import sys
import logging
import config
from config import Config

from AAA.loggerConfig import appendToLogger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from GPT.SessionManager import GPTManager
from GPT import DocumentedResponse
from Parser.Metrics import parseMetrics

from pydantic import BaseModel

class Request_BodyWithPrompt(BaseModel):
    prompt: str
    data: dict

appendToLogger()
logger = logging.getLogger(__name__)

config.logConfig()

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await cache_object.startup(app, scheduler)

    # start AI model
    global model
    model = GPTManager()

    # scheduler.start()

    yield

    # await cache_object.shutdown(app, scheduler)

    # scheduler.shutdown()

    model.close()

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
    # fastapi_cdn_host.patch_docs(app, docs_cdn_host='https://gcore.jsdelivr.net/npm')

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
    # app.include_router(dashboard_router)

    @app.post("/recommendations/{agent_id}")
    def get_agent_recommendations(agent_id: str, json_data: dict) -> str:
        '''
        Get recommendations for an agent based on the call data
        '''

        parsed_data = parseMetrics(json_data)

        try:
            response = model.prompt(f'recommendations-{agent_id}', parsed_data)
        except ValueError:
            model.create_session(f'recommendations-{agent_id}', """You are a personal trainer. 
                The person you are training works on a front-desk call center and needs a lot of help while talking to costumers. 
                You must give your trainee a list of recommendations, in a positive leadership manner. 
                You are talking directly to your trainee, make sure to make it as personal as possible. 
                Note that the average call duration is 3 minutes, it should be under that.
                A negative sentiment means that they might have been angry, stressed, or without a positive attitude.
                Durations are given in milliseconds.
                Make sure the Agent NEVER interrupts the customer.
                Talk time should be as little as possible.
                Your trainee's name is unknown, however, refer to it in second person, avoid saying things like 'the agent'. Try to start feedback like: 'You should...' or 'Have you tried ...'""", "### Call record:\n{0}\n\n### What can I (the agent) improve based on the last call record? Please give me feedback on what I can improve!\n")
            
            response = model.prompt(f'recommendations-{agent_id}', parsed_data)

        return response
    
    @app.post("/response/{call_id}")
    async def get_client_response(call_id: str, question: Request_BodyWithPrompt) -> str:
        toReturn = DocumentedResponse.get_response(question.prompt, call_id, model)

        return toReturn

    logger.info("FastAPI app started without errors")
except Exception as e:
    logger.critical(f"Error starting the FastAPI app: {e}")

if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting the FastAPI app programmatically on {Config.HOST}:{Config.PORT}")
    uvicorn.run(app=app, host=Config.HOST, port=int(Config.PORT), log_level="debug" if Config.DEBUG else "info")