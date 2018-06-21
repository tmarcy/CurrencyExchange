from api import app
from flask import render_template, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import required
from api.models.export import User, Search, Currency, user_key
from google.appengine.ext import ndb


import logging

import urllib, urllib2
import json

API_KEY = 'your-API-key'

code_list = []

url = 'http://data.fixer.io/api/latest'

param = { 'access_key': API_KEY }

class MyForm(FlaskForm):

    params = urllib.urlencode(param)
    myurl = '{}?{}'.format(url, params)
    logging.info('myurl: {}'.format(myurl))
    req = urllib2.Request(myurl)
    urlencode = urllib2.urlopen(req)
    content = urlencode.read()
    risp = json.loads(content)
    rates = risp['rates']

    for each, each2 in rates.items():
        obj = (each, each2)
        code_list.append(obj)
    code_list.sort()

    email = StringField('email', [required()])
    code_input = SelectField('code_in', choices = [(code[0], code[0]) for code in code_list], validators=[required()])
    code_output = SelectField('code_out', choices = [(code[0], code[0]) for code in code_list], validators=[required()])
    amount = IntegerField('amount', [required()])
    submit = SubmitField('submit', [required()])


@app.route('/conversion', methods=['GET'])
def show_form():
    form = MyForm()
    return render_template('data.html', form=form)


@app.route('/conversion', methods=['POST'])
def submit_form():
    form = MyForm(request.form)
    if not form.validate():
        print "ERRORS"
        print form.errors
        return render_template('data.html', form=form), 400

    email_inserted = form.email.data
    code_in_inserted = form.code_input.data
    code_out_inserted = form.code_output.data
    amount_inserted = form.amount.data

    # save in Datastore
    qry = User.query(User.email == email_inserted).get()
    qry2 = Currency.query(ndb.AND(Currency.cur_in == code_in_inserted, Currency.cur_out == code_out_inserted)).get()

    if not qry:
        newu = User(email=email_inserted)
        newu.put()
        # insert new Search
        s = Search(parent=user_key(newu.email), cur_in=code_in_inserted, cur_out=code_out_inserted,
                   amount=amount_inserted)
        s.put()
        logging.info('Correctly added new user {} and his search'.format(email_inserted))
    else:
        # insert new Search
        s = Search(parent=user_key(qry.email), cur_in=code_in_inserted, cur_out=code_out_inserted,
                   amount=amount_inserted)
        s.put()
        logging.info('Correctly updated user {} and his search'.format(email_inserted))

    if not qry2:
        # insert new Currency conversion Search
        newc = Currency(cur_in=code_in_inserted, cur_out=code_out_inserted, counter=1)
        newc.put()
        logging.info('Correctly added new currency search {}'.format(code_in_inserted))
    else:
        # update Currency conversion Search
        qry2.counter = qry2.counter+1
        qry2.put()
        logging.info('Correctly updated currency search {} and his search'.format(code_in_inserted))

    logging.info('Convert {} {} in {}'.format(amount_inserted, code_in_inserted, code_out_inserted))
    for each in code_list:
        if each[0] == code_in_inserted:
            tax = each[1]
            logging.info('trovato: {}, tax: {}'.format(each, tax))
    ris = tax*amount_inserted

    return render_template('response.html', codin = code_in_inserted, codout = code_out_inserted,
                           amount=amount_inserted, tax=tax, ris=ris)
