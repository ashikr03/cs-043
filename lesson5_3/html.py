from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    page = '''<!DOCTYPE html>
          <html>
          <head><title>Page Title</title></head>
          <body>Page Body</body>
          </html>'''

    return [page.encode()]


httpd = make_server('', 8000, application)
httpd.serve_forever()
