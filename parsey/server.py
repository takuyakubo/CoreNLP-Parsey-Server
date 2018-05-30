#!/usr/bin/python
from flask import Flask, request, Response
from multiprocessing import Pool
from parser import parse_sentences

app = Flask(__name__)
port = 5000

pool = Pool(1, maxtasksperchild=50)

@app.route('/', methods=['POST', 'GET'])
def index():
    data = request.data.decode('utf-8')
    if not data:
        return Response(status=500, response="error")
    result = list(pool.apply(parse_sentences, [data, request.args]))
    tagged = []
    tapp = tagged.append
    for idx in range(len(result[0])):
        token = result[0][idx + 1]
        tapp(token['form'] + '/' + token['xpostag'])
    sent = ' '.join(tagged)

    return Response(
        status=200,
        response=sent,
        content_type="text/plain")


if __name__ == '__main__':
    app.run(port=port, host="0.0.0.0")
