import wsgiref.simple_server
import urllib.parse
from lesson2_2.database3 import Simpledb

def application(environ, start_response):
    headers = [("Content-Type", 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])

    db = Simpledb('db.txt')

    if path == "/insert":
        db.addEntry(str(params['key']), str(params['value']))
        start_response("200 OK", headers)
        return["Inserted".encode()]
    elif path == '/select':
        s = db.findEntry(str(params['key'][0]))
        start_response("200 OK", headers)
        if s == None:
            return ['NULL'.encode()]
        else:
            return [s.encode()]
    elif path == "/delete":
        if db.findEntry(params['key'][0]) != None:
            db.deleteEntry(params['key'])
            start_response("200 OK", headers)
            return["Deleted.".encode()]
        else:
            return["NULL".encode()]
    elif path == '/update':
        if db.findEntry(params['key'][0]) != None:
            db.updateEntry(params['key'], params['value'])
            start_response("200 OK", headers)
            return ["Updated.".encode()]
        else:
            return["NULL.".encode()]

    else:
        start_response('404 Not Found', headers)
        return ["Status 404: Resource not found".encode()]

httpdb = wsgiref.simple_server.make_server('', 8000, application)
httpdb.serve_forever()
