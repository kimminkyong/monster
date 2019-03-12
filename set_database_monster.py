import urllib
import pymysql
import datetime
import monster_log

class setDatabaseMonster():
    def __init__(self):
        print("monster database setting init!!")

    def dbSCI(self):
        sc_db = pymysql.connect(
            host="localhost",  # DATABASE_HOST
            port=3306,
            user="root",  # DATABASE_USERNAME
            passwd="kmk9972026324!",  # DATABASE_PASSWORD
            db="stock_code_info",  # DATABASE_NAME
            charset='utf8'
        )
        return sc_db

    def dbSDI(self):
        sd_db = pymysql.connect(
            host="localhost",  # DATABASE_HOST
            port=3306,
            user="root",  # DATABASE_USERNAME
            passwd="kmk9972026324!",  # DATABASE_PASSWORD
            db="stock_daily_info",  # DATABASE_NAME
            charset='utf8'
        )
        return sd_db

    


    





