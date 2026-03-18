from dotenv import load_dotenv
from loguru import logger

logger.info("Loading environment variables")
load_dotenv()
logger.info("Environment variables loaded")

from config.logger import setup_logging

setup_logging(console_level="INFO")

from api.app import app

if __name__ == "__main__":
    logger.info("Starting Fashion E-commerce")
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
