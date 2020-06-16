import wsgiref.simple_server


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    page = '''<!DOCTYPE html>
          <html>
          <head><title>Biography</title></head><body>
          <h1 style= "color: lightblue">Invictus</h1>
          <h2>By Stephen Crane</h2>
          <p>It matters not how strait the gate,</p>
          <p>Nor charged with punishments the scroll.</p>
          <p>I am the master of my fate,</p>
          <p>The captain of my soul.</p>
          <br>
          <a href="https://en.wikipedia.org/wiki/Invictus">
          <img src=https://upload.wikimedia.org/wikipedia/commons/f/fc/William_Ernest_Henley_Vanity_Fair_1892-11-26.jpg"/></a>
          <br>
          <p>Check out the link to the full poem here!</p>
          <p><a href= "https://www.poetryfoundation.org/poems/51642/invictus">Full Poem </a></p>
          <p> More poets:</p>
          <p><a href=https://www.poetryfoundation.org/poets/stephen-crane> Stephen Crane</a></p>
          <p><a href=https://www.poetryfoundation.org/poets/henry-david-thoreau> Henry David Thoreau</a></p>
          </body>
          </html>'''

    return [page.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
