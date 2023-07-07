import logging

import uvicorn

from app.logging import Ansi, log

if __name__ == '__main__':
    log("Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)", Ansi.YELLOW)
    uvicorn.run("app.api.init_api:nogu_app", reload=True, log_level=logging.WARNING, port=8000)
