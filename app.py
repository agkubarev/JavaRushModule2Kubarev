import os
from http.server import HTTPServer
from loguru import logger
from db.DBManager import DBManager
from dotenv import load_dotenv
from ImageHostingHandler import ImageHostingHandler
from settings import SERVER_ADDRESS

logger.add('logs/app.log', format="[{time: YYYY-MM-DD HH:mm:ss}] | {level} | {message}")


def run():
    load_dotenv()
    db = DBManager(os.getenv('POSTGRES_DB'),
                   os.getenv('POSTGRES_USER'),
                   os.getenv('POSTGRES_PASSWORD'),
                   os.getenv('POSTGRES_HOST'),
                   os.getenv('POSTGRES_PORT'))
    db.init_tables()
    logger.info(db.get_images())
    db.execute("DROP TABLE IF EXISTS images")
    # noinspection PyTypeChecker
    httpd = HTTPServer(SERVER_ADDRESS, ImageHostingHandler)
    # noinspection PyBroadException
    try:
        logger.info(f'Serving at http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
        httpd.serve_forever()
    except Exception:
        pass
    finally:
        logger.info('Server stopped')
        httpd.server_close()


if __name__ == "__main__":
    run()
