# -*- coding: utf-8 -*-
import flask
from flask import *
import requests
from dotenv import load_dotenv
import os
import ffmpeg



app = flask.Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def index():
    return '''
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <button>upload</button>
    </form>
'''


@app.route('/hello')
def hello_world():
    return jsonify({'message': 'Hello, world'})

@app.route('/upload', methods=['POST'])
def upload():

    # print(request.files)
        print("test")
        if 'file' not in flask.request.files:
            return 'no-file'

        fs = flask.request.files['file']

        filename = fs.filename
        fs.save(filename)
        
        # 入力
        stream = ffmpeg.input(filename)
        
        # 出力
        stream = ffmpeg.output(stream, "test.wav", ac=1, ar=11025).overwrite_output()
        
        try:
        # 実行
            ffmpeg.run(stream)
        except Error as e:
            print(e)

        url ='https://api.webempath.net/v2/analyzeWav'

        # .envにAPI_KEY = xxxx を記述する
        apikey = os.getenv('API_KEY')
        payload = {'apikey': apikey}
        wav = "test.wav"
        data = open(wav, 'rb')
        file = {'wav': data}
        res = requests.post(url, params=payload, files=file)

        print(res.json())

        return res.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug=True)