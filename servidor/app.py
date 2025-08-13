from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return'¡Hola,mundo!'

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api/sensor')