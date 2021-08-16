import os

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        import test1
        return test1.main()
    except Exception as e:
        pass
    return 'OH NO!\n'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))