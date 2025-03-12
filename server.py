from windows import WindowsInterface
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import ssl


class Request(BaseHTTPRequestHandler):
    def set_failure_headers(self):
        self.send_response(400)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def set_not_started_headers(self):
        self.send_response(503)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def set_success_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        print("Received post response")
        wi = WindowsInterface()

        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode())
        print("Received request {}".format(request))

        if not request['process_name'] or not request['startup_path']:
            print("Did not receive process_name or startup_path")
            self.set_failure_headers()
            return

        if request['type'] == 'status':
            res = wi.is_program_running(request['process_name'])
            if res:
                self.set_success_headers()
                return
            print("The process was not running, sending not started")
            self.set_not_started_headers()
            return

        elif request['type'] == 'start':
            res = wi.start_program(request['startup_path'], request['process_name'])
            if res:
                self.set_success_headers()
                return
            print("The process did not start when requested, sending not started")
            self.set_not_started_headers()
            return

        print("Did not hit any if statements")
        self.set_failure_headers()


def run(server_class=HTTPServer, handler_class=Request, port=54321):
    server_address = ('api.northernlights.network', port)
    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='pub.pem',
                                   keyfile='key.pem')
    print("Starting service on port {}".format(port))
    httpd.serve_forever()


run()
