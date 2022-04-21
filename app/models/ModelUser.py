from .entities.User import User


class ModelUser():
    @classmethod
    def login(self,conexion,user):
        try:
            cursor=conexion.connection.cursor()
            sql="""SELECT id, username,password FROM user WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self,conexion,id):
        try:
            cursor=conexion.connection.cursor()
            sql="""SELECT id, username FROM user WHERE id = '{}'""".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return User(row[0],row[1],None)
            else:
                return None
        except Exception as ex:
            raise Exception(ex)