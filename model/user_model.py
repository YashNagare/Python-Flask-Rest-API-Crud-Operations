import mysql.connector
import json

class user_model:

    def __init__(self):
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="root", database="flask_tutorial")
            self.cur = self.con.cursor(dictionary=True)
            print("Connection successful")
        except:
            print("Some error")
    
    def user_getall_model(self):
        # Business Logic
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result) > 0:
            return json.dumps(result)
        else:
            return "No data found"