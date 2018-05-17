from app import db
from app.common.mixin import JSONMixin

class User(db.Model,JSONMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    UserCode = db.Column(db.String(64), unique=True, index=True)
    Password = db.Column(db.String(128))

    def __init__(self, UserCode=None, Password=None):
        self.UserCode = UserCode
        self.Password = Password
    #
    # def __repr__(self):
    #     return '<User %r>' % self.UserName


class User2(db.Model):
    __tablename__ = 'users2'

    id = db.Column(db.Integer, primary_key=True)
    UserCode = db.Column(db.String(64), unique=True, index=True)
    Password = db.Column(db.String(128))

    def __init__(self, UserCode=None, Password=None):
        self.UserCode = UserCode
        self.Password = Password
    #
    # def __repr__(self):
    #     return '<User2 %r>' % self.UserName