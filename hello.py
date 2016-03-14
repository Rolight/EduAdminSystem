from flask import Flask as fk

app = fk(__name__)

@app.route('/')
def hello_world():
    return 'hello world'


if __name__ == '__main__':
    app.run(debug=True)
