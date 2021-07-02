from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from requests import Session
from datetime import datetime, date, time, timedelta

from wabot import WABot
import json

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
sess = Session()


@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        # bot = WABot(request.json)
        return render_template('index.html')


@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if request.method == 'POST':
        bot = WABot()

        result = bot.send_message(request.form['chatbot_phone'], request.form['chatbot_message'])
        if result['sent']:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(seconds=1)
            session['success'] = True
            return redirect(request.referrer)
        else:
            session.permanent = True
            app.permanent_session_lifetime = timedelta(seconds=1)
            session['fail'] = True
            return redirect(request.referrer)
    if request.method == 'GET':
        return render_template('send_message.html')


if __name__ == '__main__':
    app.run()
