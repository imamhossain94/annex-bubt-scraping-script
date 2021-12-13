import os, sys

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify

from requests import get, post, Session
from requests.utils import dict_from_cookiejar
from requests.cookies import create_cookie

from bs4 import BeautifulSoup


# For Server
sys.path.insert(0, os.getcwd()+'/apis')



app = Flask(__name__)


# BLUEPRINTS
from bubt.bubt import bubt


app.register_blueprint(bubt)



@app.route('/')
def welcome():
    return '<h1 align="center">Successfully Running</h1>'


@app.route('/test')
def test():

    data = {
        'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    }

    proxies = {
        "http": '139.59.1.14:3128',
        }

    data['ip_api'] = get("http://ip-api.com/json/").text

    #print(dir(redirect("http://ip-api.com/json/")))
    print(redirect("http://ip-api.com/json/").data)
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


#if _name_ == '_main_':
#    app.secret_key = 'thisisverysecret'

#    app.run(debug=True)



