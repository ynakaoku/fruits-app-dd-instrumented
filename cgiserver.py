import http.server
from ddtrace.runtime import RuntimeMetrics
RuntimeMetrics.enable()

server_address = ("", 80)
handler_class = http.server.CGIHTTPRequestHandler
handler_class.cgi_directories = ["/fruits"]
server = http.server.HTTPServer(server_address, handler_class)
server.serve_forever()