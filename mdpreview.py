#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import redirect, session, request, abort, url_for
from werkzeug import secure_filename
import urllib2

app = Flask(__name__)

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        mdfile = request.files['mdfile']
        filename = secure_filename(mdfile.filename)
        mddata = mdfile.read()
        req = urllib2.Request('https://api.github.com/markdown/raw')
        req.add_header('content-type', 'text/plain')
        req.add_data(mddata)
        ret = urllib2.urlopen(req)
        htmlstring = ret.read()
    else:
        return redirect(url_for('index'))

    return render_template('upload.html', body=htmlstring.decode('utf-8'), title=filename)

@app.route("/")
def index():
  return render_template('top.html')

if __name__ == '__main__':
    app.run(debug=True)
