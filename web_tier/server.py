from urllib import request
from flask import Flask, request
from werkzeug.utils import secure_filename
from os import environ, path
from utils import S3
from utils import SQS
import boto3
import base64
app = Flask(__name__)
app.config.from_pyfile('config.py')

results = {}


@app.route('/',methods = ['POST'])
def hello_world():
    return 'Hello world!'


@app.route('/upload', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      
      enc_string = base64.b64encode(f.read())

      S3.upload_file(file=f, filename=filename)
      response = SQS.enqueue(filename)
      print('Waiting for output')
      while(True):
        print(results)
        if filename in results:
            return results[filename]
        if SQS.get_queue_length == 0:
            continue
        result = SQS.get_messages()
        results.update(result)


    




        
    


