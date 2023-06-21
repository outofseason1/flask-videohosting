import sqlite3

from coder import generate_id


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getVideos(self):
        sql = 'SELECT * FROM videos ORDER BY date DESC'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения из БД')
        return []

    def addVideo(self, title, description, user, video):
        id = generate_id()
        try:
            a = self.__cur.execute(F'SELECT * FROM videos where id={id}').fetchone()
            while a is not None:
                id = generate_id()
        except sqlite3.OperationalError as e:
            pass

        try:
            self.__cur.execute('INSERT INTO videos (title, description, id, author, video) VALUES (?, ?, ?, ?, ?)', (title, description, id, user, video))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка добавления видео в БД {e}')
            return False

        return True

    def getThatVideo(self, id):
        self.__cur.execute(f'SELECT * FROM videos WHERE id="{id}"')
        res = self.__cur.fetchone()
        if res: return res

    def getVideosBySearch(self, search):
        sql = f'SELECT * FROM videos WHERE lower(title) LIKE "%{search}%"'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print(f"Ошибка {e}")
        return []

    def getVideosByUser(self, username):
        sql = f'SELECT * FROM videos WHERE author LIKE "%{username}%"'
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print(f"Ошибка {e}")
        return []

    def addUser(self, username, mail, pas):
        try:
            self.__cur.execute(f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{mail}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False

            self.__cur.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, pas, mail))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка {e}')
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print(f"Ошибка получения данных из БД {e}")

        return False

    def getUserByName(self, username):
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE username = "{username}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False

            return res
        except sqlite3.Error as e:
            print(f"Ошибка получения данных из БД {e}")

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f'UPDATE users SET avatar = ? WHERE id = ?', (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Ошибка обновления аватара в БД {e}')
            return False
        return True