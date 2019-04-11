from app import db


class User(db.Model):
    __tablename__ = 'cms_apply'
    SID = db.Column(db.String(30), primary_key=True)
    PASSWORD = db.Column(db.String(32))

    def __init__(self, user_id, pwd):
        self.SID = user_id
        self.PASSWORD = pwd

    def get_id(self):
        if self.SID is None:
            return None
        return self.SID

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        if self.SID:
            return self.SID
        else:
            return 'Anonymous'
