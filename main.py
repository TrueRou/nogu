import logging

import uvicorn

import config
from app import sessions
from app.logging import Ansi, log

if __name__ == '__main__':
    log(f"Uvicorn running on {sessions.get_uri()} (Press CTRL+C to quit)", Ansi.YELLOW)
    uvicorn.run("app.api.init_api:nogu_app", reload=True, log_level=logging.WARNING, port=config.bind_port, host=config.bind_address)
