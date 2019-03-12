import sys
import datetime
import set_database_monster

logKind = ['d_log','a01_log']
DAYLY_LOG = []
ALG_LOG_MA1 = []

class monsterLog():
    def __init__(self):
        print('monster log init!')
        self.monsterDB  = set_database_monster.setDatabaseMonster()

    def check_log_table(self, logType, logText, logDate):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                sql = "SELECT * FROM `monster_log` WHERE date='"+logDate+"' AND log_kind='"+logType+"' LIMIT 1"
                curs.execute(sql)
                result = curs.fetchone()
                if result:
                    return False
                else:
                    return True
        finally:
            print("find_date_stock_info")

    def add_log(self, logType, logText):
        sdi_db = self.monsterDB.dbSDI()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        lType = logKind[logType]

        DAYLY_LOG.append(logText)
        log_content = "#".join(DAYLY_LOG)

        if self.check_log_table(lType, logText, today) : #insert
            try:
                with sdi_db.cursor() as curs:
                    sql = "INSERT INTO `monster_log` (date, log_kind, content, error_step, result) values (%s,%s,%s,%s,%s)"
                    curs.execute( sql, (today, lType, log_content, 2, True) )
            finally:
                sdi_db.commit()
        else: #update
            try:
                with sdi_db.cursor() as curs:
                    sql = "UPDATE `monster_log` SET content='"+log_content+":kmk11' WHERE date='"+today+"' AND log_kind='"+lType+"' "
                    curs.execute(sql)
            finally:
                sdi_db.commit()
            
        

