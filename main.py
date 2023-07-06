import logging

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.api.init_api:nogu_app", reload=True, log_level=logging.WARNING, port=8000)
