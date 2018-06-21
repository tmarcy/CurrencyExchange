from google.appengine.ext import ndb


def user_key(id):
    return ndb.Key(User, id)


class Search(ndb.Model):
    cur_in = ndb.StringProperty()
    cur_out = ndb.StringProperty()
    amount = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


class User(ndb.Model):
    email = ndb.StringProperty()


class Currency(ndb.Model):
    cur_in = ndb.StringProperty()
    cur_out = ndb.StringProperty()
    counter = ndb.IntegerProperty()