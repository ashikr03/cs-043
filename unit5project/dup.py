import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if (r == []):
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)

def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    path = environ['PATH_INFO']

    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['pw'][0] if 'pw' in params else None

    print(path)

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            connection.commit()
            headers.append(("Set-Cookie", 'session = {}:{}'.format(un, pw)))
            correct = 0
            wrong = 0
            #headers.append(('Set-Cookie', 'correct={}'.format(correct)))
            #headers.append(('Set-Cookie', 'wrong={}'.format(wrong)))
            start_response('200 OK', headers)
            return ['Username {} and password is successful. <a href="/account">Account</a>'.format(un).encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            correct = 0
            wrong = 0
            headers.append(('Set-Cookie', 'correct={}'.format(correct)))
            headers.append(('Set-Cookie', 'wrong={}'.format(wrong)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        #start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        #This is where the game begins. This section of is code only executed if the login form works, and if the user is successfully logged in.
        if user:
            correct = 0
            wrong = 0
            start_response('200 OK', headers)

            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                if 'correct' not in cookies or 'wrong' not in cookies:
                    headers.append(('Set-Cookie', 'correct={}'.format(correct)))
                    headers.append(('Set-Cookie', 'wrong={}'.format(wrong)))

            correct = int(cookies['correct'].value)
            wrong = int(cookies['wrong'].value)
            print(cookies)

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                if int(params['answer'][0]) == int(params['factor1'][0])* int(params['factor2'][0]):
                    correct += 1
                    print(correct)
                    return["<a href='/account'>Correct.</a>".encode()]
                else:
                    print(wrong)
                    wrong += 1
                    return ["<a href='/account'>Incorrect.</a>".encode()]
            elif 'reset' in params:
                correct = 0
                wrong = 0

            #headers.append(('Set-Cookie', 'correct={}'.format(correct)))
            #headers.append(('Set-Cookie', 'wrong={}'.format(wrong)))
            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}?</h1>'.format(f1, f2)
            #[INSERT CODE HERE.Create a list that stores f1 * f2(the right answer) and 3 other random answers]
            product = int(f1*f2)
            setof = []
            o1 = None
            o2 = product
            o3 = None
            while product == o1 or product == o2 or product == o3:
                o1 = random.randint(0,145)
                o2 = random.randint(0,145)
                o3 = random.randint(0,145)
                o4 = product
            setof.append(o1)
            setof.append(o2)
            setof.append(o3)
            setof.append(o4)
            random.shuffle(setof)
            no1 = setof[0]
            no2 = setof[1]
            no3 = setof[2]
            no4 = setof[3]

            hyperlink = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}:{}</a><br>'

            #[INSERT CODE HERE. Create the 4 answer hyperlinks here using string formatting.]
            page = page + hyperlink.format(un, pw, f1, f2, no1, 'A', no1) + hyperlink.format(un, pw, f1, f2, no2, 'B', no2) + hyperlink.format(un, pw, f1, f2, no3, 'C.', no3) + hyperlink.format(un, pw, f1, f2, no4, 'D', no4)
            print(cookies)
            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
    #[INSERT CODE HERE. Create the two forms, one to login, the other to register a new account]
        start_response('200 OK', headers)
        page = '''<!DOCTYPE html>
        <html>
        <head><title>Simple Form</title></head>
        <body>
        <h1>A web form</h1>
        <form action="/login">
            Username<input type= "text" name="username" value= "Enter username" ><br>
            Password <input type="password" name = "pw"><br>
            <input type ="submit" name= "thebutton" value= "Log me in">
        </form>
        <br>
        <form action = "/register">
            Username <input type = "text" name="username" value="Enter username" <br>
            Password <input type="password" name = "pw"> <br>
            <input type = "submit" value = "Register">
        </form>
        <a href = "/account">Account</a>
        </body></html>'''
        return [page.encode()]
    else:
        start_response('404 Not Found', headers)
        return['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()



