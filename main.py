from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def result():
    print(request.form['type'])
    return '<p>Hi!</p>'

app.run()