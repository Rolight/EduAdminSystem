from flask import Flask as fk
from flask import request

app = fk(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return '<p>Your browser is %s</p>' % user_agent

if __name__ == '__main__':
    app.run(debug=True)
