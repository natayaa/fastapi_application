from fastapi import FastAPI, Request
from custom_logging import KustomLogger
from pathlib import Path
import uvicorn, logging

logger = logging.getLogger(__name__)
conf_path = Path(__file__).with_name("logging_conf.json")

app = FastAPI(logger=KustomLogger.make_logger(config_path=conf_path), debug=False, title="Something")

@app.get("/loggs")
def custom_(request: Request):
    request.app.logger.info("Info log")
    a = 1/ 0
    request