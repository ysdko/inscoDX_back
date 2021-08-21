import flask
import requests
from dotenv import load_dotenv
import os

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
    <form method="post" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <button>upload</button>
    </form>
'''

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in flask.request.files:
        return 'ファイル未指定'

    fs = flask.request.files['file']

    app.logger.info('file_name={}'.format(fs.filename))
    app.logger.info('content_type={} content_length={}, mimetype={}, mimetype_params={}'.format(
        fs.content_type, fs.content_length, fs.mimetype, fs.mimetype_params))

    fs.save('test.wav')
    url ='https://api.webempath.net/v2/analyzeWav'

    # .envにAPI_KEY = xxxx を記述する
    apikey = os.getenv('API_KEY')
    payload = {'apikey': apikey}
    wav = "test.wav" 
    data = open(wav, 'rb')
    file = {'wav': data}
    res = requests.post(url, params=payload, files=file)
    print(res.json())

    return "フィアルアップロード成功"

if __name__ == '__main__':
    app.run(debug=True)