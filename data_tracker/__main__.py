import argparse
import logging

import uvicorn

from data_tracker.config import PORT_LISTEN


def main():
    parser = argparse.ArgumentParser(description="Start the server")
    parser.add_argument("--reload", type=bool, default=False)
    options = parser.parse_args()
    logger = logging.getLogger()
    logger.info("Starting Data Tracker", extra={"port": PORT_LISTEN})
    uvicorn.run(
        "data_tracker.server.app:asgi_create_app",
        host="0.0.0.0",
        port=PORT_LISTEN,
        reload=options.reload,
        lifespan="on",
    )


if __name__ == "__main__":
    main()
