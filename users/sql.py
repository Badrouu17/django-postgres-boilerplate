def insertUser(user):
    name, email, password = (user["name"], user["email"], user["password"])

    return f"""INSERT INTO users_user(name, email, password) 
               VALUES('{name}', '{email}', '{password}') 
               RETURNING *"""


def getUserWithEmail(email):
    return f""" SELECT id,name,email,photo,password
                FROM users_user
                WHERE users_user.email = '{email}' """


def getUserWithId(id):
    return f""" SELECT id,name,email,photo,password,password_changed_at
                FROM users_user_user
                WHERE users_user_user.id = {id} """


def updateUserPassResetData(id, prt, pre):
    return f""" UPDATE users_user
                SET users_user.password_reset_token = '{prt}' ,users_user.password_reset_expires = {pre}
                WHERE users_user.id = {id} """


def getUserByResetToken(prt, now):
    return f""" SELECT id,name,email,photo,password
                FROM users_user
                WHERE users_user.password_reset_token = '{prt}'
                AND
                users_user.password_reset_expires > {now} """


def updateResetPassword(id, psw, pca):
    return f""" UPDATE users_user
                SET users_user.password = '{psw}', 
                users_user.password_reset_token = NULL, 
                users_user.password_reset_expires = NULL,
                users_user.password_changed_at = '{pca}'
                WHERE users_user.id = {id} """


def updateUserEmail(id, email):
    return f""" UPDATE users_user
                SET email = '{email}'
                WHERE users_user.id = {id} """


def updateUserName(id, name):
    return f""" UPDATE users_user
                SET name = '{name}'
                WHERE users_user.id = {id} """


def updatUserPhoto(id, photo):
    return f""" UPDATE users_user
                SET photo = '{photo}'
                WHERE users_user.id = {id} """


def deleteUser(id):
    return f""" DELETE FROM users_user
                WHERE users_user.id = {id} """
