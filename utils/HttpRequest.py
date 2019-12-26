import json
from requests import Session, Request
from flask import Response

__author__ = 'litl'


def send(url, method, headers, data):
    s = Session()
    req = Request(method, url, data=data.encode('utf-8'), params=data, headers=headers)
    prepped = req.prepare()
    resp = s.send(prepped)
    try:
        res = {"header": "{0}".format(resp.headers), "body": "{0}".format(resp.content.decode(encoding='utf-8'))}
        return Response(json.dumps(res), mimetype='application/json')
    except:
        res = {"header": "{0}".format(resp.headers), "body": "{0}".format(resp.content)}
        return Response(json.dumps(res), mimetype='application/json')


def parse_headers(headers):
    args = {}
    if headers:
        sps = headers.split(',')
        for s in sps:
            p = s.split(":")
            print(p[0], "=", p[1])
            args[p[0]] = p[1]
    return args


def parse_params(params):
    args = {}
    if params:
        sps = params.split('&')
        for s in sps:
            p = s.split("=")
            print(p[0], "=", p[1])
            args[p[0]] = p[1]
    return args