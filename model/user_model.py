import mysql.connector
import json
from flask import make_response
from datetime import datetime, timedelta
import jwt
from config.config import dbconfig

class user_model:

    def __init__(self):
        try:
            self.con = mysql.connector.connect(host=dbconfig["hostname"], user=dbconfig["username"], password=dbconfig["password"], database=dbconfig["database"])
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            print("Connection successful")
        except:
            print("Some error")
    
    def user_getall_model(self):
        # Business Logic
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result) > 0:
            # return json.dumps(result)
            res = make_response({"payload" : result}, 200)
            res.headers["Access-Control-Allow-Origin"] = "*"
            return res
        else:
            return make_response({"message" : "No data found"}, 204)

    def user_addone_model(self, data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, role_id, password) VALUES('{data['name']}', '{data['email']}', '{data['phone']}', '{data['role_id']}', '{data['password']}')")
        return make_response({"message" : "User created successfully"}, 201)
    
    def user_addmultiple_model(self, data):
        qry = "INSERT INTO users(name, email, phone, role_id, password) VALUES "
        for userdata in data:
            qry += f"('{userdata['name']}', '{userdata['email']}', '{userdata['phone']}', {userdata['role_id']},'{userdata['password']}'),"
        finalqry = qry.rstrip(",")
        self.cur.execute(finalqry)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def user_update_model(self, data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', role_id='{data['role_id']}', password='{data['password']}' WHERE id='{data['id']}'")
        if self.cur.rowcount > 0:
            return make_response({"message" : "User updated successfully"}, 201)
        else:
            return make_response({"message" : "Nothing to update"}, 202)

    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        if self.cur.rowcount > 0:
            return make_response({"message" : "User deleted successfully"}, 200)
        else:
            return make_response({"message" : "Nothing to delete"}, 202)

    def user_patch_model(self, data, id):
        qry = "UPDATE users SET "
        for key in data:
            qry += f"{key}='{data[key]}',"

        qry = qry[:-1] + f" WHERE id={id};"
        self.cur.execute(qry)

        if self.cur.rowcount > 0:
            return make_response({"message" : "User updated successfully"}, 201)
        else:
            return make_response({"message" : "Nothing to update"}, 202)

    def user_pagination_model(self, limit, page):
        limit = int(limit)
        page = int(page)
        start = (page * limit) - limit
        qry = f"SELECT * from users LIMIT {start}, {limit}"
        self.cur.execute(qry)
        result = self.cur.fetchall()
        if len(result) > 0:
            res = make_response({"payload" : result, "limit" : limit, "page" : page}, 200)
            return res
        else:
            return make_response({"message" : "No data found"}, 204)
    
    def user_upload_avatar_model(self, uid, filepath):
        self.cur.execute(f"UPDATE users SET avatar='{filepath}' where id={uid}")
        if self.cur.rowcount > 0:
            return make_response({"message" : "FILE_UPLOADED_SUCCESSFULLY"}, 201)
        else:
            return make_response({"message" : "Nothing to update"}, 202)
        
    def user_login_model(self, data):
        self.cur.execute(f"SELECT id, name, email, phone, avatar, role_id FROM users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.cur.fetchall()
        userdata = result[0]
        exp_time = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_time.timestamp())
        payload = {
            "payload" : userdata,
            "exp" : exp_epoch_time
        }
        jwtoken = jwt.encode(payload, "cypher", algorithm="HS256")
        return make_response({"token" : jwtoken}, 200)