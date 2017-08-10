from flask_login import UserMixin


class User(UserMixin):
    def __init__(self):
        self.id = 0

    @property
    def is_active(self):
        return self.id != 0

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return not self.is_active

    def get_id(self):
        return self.id

    def get_by_id(self, requested_id):
        if requested_id != 0:
            self.id = requested_id
            return self
        else:
            return None


