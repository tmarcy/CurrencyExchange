from api.models.export import User, Search, Currency, user_key
from flask import request, make_response

from api import app, csrf_protect
import json
from google.appengine.ext import ndb
import logging


@app.route('/api/v1.0/stats', methods=['GET'])
def most_popular():
    """
        It shows a list of the last 3 conversions about a
        specific user and the last 3 conversions with a
        specific currency code as input.
        User email and currency type are GET request parameters.
        :return: response in json format
        """
    json_response = {}

    param_email = request.args.get('email')
    param_currency = request.args.get('currency')

    if param_email is None and param_currency is None:
        json_response['status'] = 'Bad Request'
        json_response['message'] = 'Missing parameters.'
        status_code = 400

    elif param_email is not None and param_currency is None:
        qry = User.query(User.email == param_email).get()
        print qry
        data_list = []
        if not qry:
            json_response['status'] = 'Bad request.'
            json_response['message'] = 'The user inserted is not present in the database.'
            status_code = 400
        else:
            user = user_key(param_email)
            logging.info('User: {}'.format(user))

            searches_query = Search.query(ancestor=user).order(-Search.date)
            searches = searches_query.fetch(3)

            for each in searches:
                mydict = {}
                mydict['cur_in'] = each.cur_in
                mydict['cur_out'] = each.cur_out
                mydict['amount'] = each.amount
                data_list.append(mydict)

            json_response['data'] = data_list
            json_response['status'] = 'OK'
            json_response['message'] = 'Succesfully returned the resource.'
            status_code = 200

    elif param_email is None and param_currency is not None:
        qry = Currency.query(Currency.cur_in == param_currency).order(-Currency.counter).fetch(3)
        print qry
        data_list = []

        if not qry:
            json_response['status'] = 'Bad request.'
            json_response['message'] = 'The currency inserted is not present in the database.'
            status_code = 400
        else:
            for each in qry:
                mydict = {}
                mydict['cur_in'] = each.cur_in
                mydict['cur_out'] = each.cur_out
                mydict['counter'] = each.counter
                data_list.append(mydict)

            json_response['data'] = data_list
            json_response['status'] = 'OK'
            json_response['message'] = 'Succesfully returned the resource.'
            status_code = 200
    else:
        json_response['status'] = 'Bad Request'
        json_response['message'] = 'Please only one parameter in this request.'
        status_code = 400

    response = make_response(json.dumps(json_response, ensure_ascii=True), status_code)
    response.headers['content-type'] = 'application/json'
    return response


@csrf_protect.exempt
@app.route('/api/v1.0/insert', methods=['POST'])
def force_insert():
    """
           It allows inserting a new conversion in the Datastore.
           All Currency model properties are POST requests parameter.
           :return: response in json format
           """
    json_response = {}

    email = request.args.get('email')
    cur_in = request.args.get('curin')
    cur_out = request.args.get('curout')
    amount = int(request.args.get('amount'))

    # save in Datastore
    qry = User.query(User.email == email).get()
    qry2 = Currency.query(ndb.AND(Currency.cur_in == cur_in, Currency.cur_out == cur_out)).get()

    if not qry:
        newu = User(email=email, counter=1)
        newu.put()

        s = Search(parent=user_key(newu.email), cur_in=cur_in, cur_out=cur_out, amount=amount)
        s.put()
        logging.info('Correctly added new user {} and his search'.format(email))

    else:
        s = Search(parent=user_key(qry.email), cur_in=cur_in, cur_out=cur_out, amount=amount)
        s.put()
        logging.info('Correctly updated user {} and his search'.format(email))

    if not qry2:
        newc = Currency(cur_in=cur_in, cur_out=cur_out, counter=1)
        newc.put()
        logging.info('Correctly added new currency search {}'.format(cur_in))

    else:
        qry2.counter = qry2.counter + 1
        qry2.put()
        logging.info('Correctly updated currency search {} and his search'.format(cur_in))

    json_response['user_stats'] = 'http://127.0.0.1:8080/api/v1.0/stats?email={}'.format(email)
    json_response['currency_stats'] = 'http://127.0.0.1:8080/api/v1.0/stats?currency={}'.format(cur_in)
    json_response['status'] = 'OK'
    json_response['message'] = 'Succesfully inserted in the database.'
    json_response['status_code'] = 200

    response = make_response(json.dumps(json_response, ensure_ascii=True), 200)
    response.headers['content-type'] = 'application/json'
    return response
