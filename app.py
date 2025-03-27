import cgi
import json
import os
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler, \
    SimpleHTTPRequestHandler
from os import listdir
from os.path import isfile, join
from PIL import Image

from loguru import logger
from db.DBManager import DBManager
from dotenv import load_dotenv

SERVER_ADDRESS = ('0.0.0.0', 8000)
ALLOWED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif')
ALLOWED_LENGTH = (5 * 1024 * 1024)
UPLOAD_DIR = 'images'
logger.add('logs/app.log', format="[{time: YYYY-MM-DD HH:mm:ss}] | {level} | {message}")


class ImageHostingHandler(BaseHTTPRequestHandler):
    server_version = 'Image Hosting Server/0.1'

    def __init__(self, request, client_address, server):
        """Initialize the handler with routing for GET and POST requests."""
        self.get_routes = {
            '/upload': self.get_upload,
            '/images': self.get_images,
        }
        self.post_routes = {
            '/upload': self.post_upload,
        }
        super().__init__(request, client_address, server)

    def do_GET(self):
        """Handle GET requests by routing to the appropriate handler or returning a 404 error."""
        if self.path in self.get_routes:
            self.get_routes[self.path]()
        else:
            logger.warning(f'GET 404 {self.path}')
            self.send_response(404, 'Not Found')

    def do_POST(self):
        """Handle POST requests by routing to the appropriate handler or returning a 405 error."""
        if self.path in self.post_routes:
            self.post_routes[self.path]()
        else:
            logger.warning(f'POST 404 {self.path}')
            self.send_response(405, 'Method Not Allowed')

    def end_headers(self):
        """Add custom headers before ending the HTTP response headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def get_images(self):
        """Handle GET request to retrieve the list of image filenames in JSON format."""
        logger.info(f'GET {self.path}')
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        images = [f for f in listdir(UPLOAD_DIR) if isfile(join('images', f))]
        self.wfile.write(json.dumps({'images': images}).encode('utf-8'))

    def get_upload(self):
        """Handle GET request to render the upload page."""
        logger.info(f'GET {self.path}')
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(open('upload.html', 'rb').read())

    def post_upload(self):
        """Handle POST request to upload an image."""
        logger.info(f'POST {self.path}')
        content_length = int(self.headers.get('Content-Length'))
        if content_length > ALLOWED_LENGTH:
            logger.error('Payload Too Large')
            self.send_response(413, 'Payload Too Large')
            return
        logger.info(f'Before cgi')
        logger.info(f'POST {self.path}')
        logger.info(f'self.rfile: {self.rfile}')
        logger.info(f'self.headers: {self.headers}')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        logger.info(f'After cgi')
        logger.info(f'form: {form}')
        data = form['image'].file

        _, ext = os.path.splitext(form['image'].filename)

        if ext not in ALLOWED_EXTENSIONS:
            logger.error('File type not allowed')
            self.send_response(400, 'File type not allowed')
            return

        image_id = uuid.uuid4()
        image_name = f'{image_id}{ext}'
        logger.info(f'Before with open')
        with open(f'{UPLOAD_DIR}/{image_name}', 'wb') as f:
            f.write(data.read())
        logger.info(f'After with open')

        try:
            im = Image.open(f'{UPLOAD_DIR}/{image_name}')
            im.verify()
        except (IOError, SyntaxError) as e:
            logger.error(f'Invalid file: {e}')
            self.send_response(400, 'Invalid file')
            return

        logger.info(f'Upload success: {image_name}')
        self.send_response(301)
        self.send_header('Location', f'/images/{image_name}')
        self.end_headers()


def run():
    load_dotenv()
    db = DBManager(os.getenv('POSTGRES_DB'),
                   os.getenv('POSTGRES_USER'),
                   os.getenv('POSTGRES_PASSWORD'),
                   os.getenv('POSTGRES_HOST'),
                   os.getenv('POSTGRES_PORT'))
    db.load_init_data()
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
