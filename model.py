from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    bdate = db.Column(db.String(100), nullable=False)

    @classmethod
    def login_is_true(cls, email, password) -> bool:
        user_obj = cls.query.filter_by(email=email).first()
        return user_obj and password == user_obj.pwd

class Reservations(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    ucount = db.Column(db.Integer, nullable=False)
    rdate = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    comments = db.Column(db.String(250), nullable=False)
    bdate = db.Column(db.String(100), nullable=False)
    caddress = db.Column(db.String(250), nullable=False)
    cphone_no = db.Column(db.String(20), nullable=False)
    cemail_address = db.Column(db.String(250), nullable=False)
    rtime = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(255), nullable=False)

class Holidays(db.Model):
    __tablename__ = 'holidays'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    bdate = db.Column(db.String(100), nullable=False)

class Frontdesk(db.Model):
    __tablename__ = 'frontdest_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    pwd = db.Column(db.String(200), nullable=False)
    bdate = db.Column(db.String(100), nullable=False)