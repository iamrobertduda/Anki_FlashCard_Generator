import json
import requests
from http.server import BaseHTTPRequestHandler
from Anki_flashcards_creator import read_pdf, create_anki_cards, download_pdf, ROOT_DIRECTORY


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data)
        url = json_data['url']

        if not url:
            self.send_response(403)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

        download_pdf(url)

        pdf_text = read_pdf(f'{ROOT_DIRECTORY}/SOURCE_DOCUMENTS/document.pdf')
        create_anki_cards(pdf_text)

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('URL erhalten: {}'.format(url).encode('utf-8'))

        return
