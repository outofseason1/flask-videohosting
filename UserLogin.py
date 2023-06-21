from flask import url_for
from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])

    def getName(self):
        return self.__user['username'] if self.__user else 'Без имени'

    def getEmail(self):
        return self.__user['email'] if self.__user else 'Без почты'

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), 'rb') as f:
                    img = f.read()
            except FileNotFoundError as e:
                print(f'Не найден аватар по умолчанию {e}')
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == 'PNG':
            return True
        return False

    def verifyFormat(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'mp4' or ext == 'MP4':
            return True
        return False