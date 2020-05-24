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
                FROM users_user
                WHERE users_user.id = {id} """


def updateUserPassResetData(id, prt, pre):
    return f""" UPDATE users_user
                SET password_reset_token = '{prt}' ,password_reset_expires = {pre}
                WHERE id = {id} """


def getUserByResetToken(prt, now):
    return f""" SELECT id,name,email,photo,password
                FROM users_user
                WHERE users_user.password_reset_token = '{prt}'
                AND
                users_user.password_reset_expires > {now} """


def updateResetPassword(id, psw, pca):
    return f""" UPDATE users_user
                SET password = '{psw}', 
                password_reset_token = NULL, 
                password_reset_expires = NULL,
                password_changed_at = '{pca}'
                WHERE id = {id} """


def updateUserEmail(id, email):
    return f""" UPDATE users_user
                SET email = '{email}'
                WHERE id = {id}
                RETURNING * """


def updateUserName(id, name):
    return f""" UPDATE users_user
                SET name = '{name}'
                WHERE id = {id}
                RETURNING * """


def updatUserPhoto(id, photo):
    return f""" UPDATE users_user
                SET photo = '{photo}'
                WHERE id = {id} 
                RETURNING *"""


def deleteUser(id):
    return f""" DELETE FROM users_user
                WHERE id = {id} """
