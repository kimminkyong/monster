import sys
import time
import pandas as pd
from pandas import DataFrame
import datetime

import set_database_monster
import alg_function


MA01_ALGORITHM_LIST = []
MA01_ALGORITHM_TABLE = "MA01"

class MA01():
    def __init__(self):
        print("MA01 INIT!!")
        self.monsterDB  = set_database_monster.setDatabaseMonster()
        self.algFn = alg_function.algFunctions()

    def insertDailyListDataInfo(self, step, lng, da):
        sdi_db = self.monsterDB.dbSDI()
        todayString = da
        try:
            with sdi_db.cursor() as curs:
                sql = "INSERT INTO `MA01_daily_list` (date, step1) values (%s,%s)"
                print(sql)
                curs.execute( sql, (todayString, lng ) )
        finally:
            sdi_db.commit()
    
    def updateDailyListDataInfo(self, step, lng, da):
        sdi_db = self.monsterDB.dbSDI()
        todayString = da
        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE `MA01_daily_list` SET step2 = '"+lng+"' WHERE date = '"+todayString+"' "
                print(sql)
                curs.execute( sql )
        finally:
            sdi_db.commit()
    
    def deleteDailyListDataInfo(self, da):
        sdi_db = self.monsterDB.dbSDI()
        todayString = da
        try:
            with sdi_db.cursor() as curs:
                sql = "DELETE FROM `MA01_daily_list` WHERE date = '"+todayString+"' "
                print(sql)
                curs.execute( sql )
        finally:
            sdi_db.commit()

    def test(self):
        #self.algFn.custom_add_colume('max_price', 'alg_step')
        #self.algFn.custom_add_colume('min_price', 'max_price')
        #self.algFn.custom_add_colume_bool('tracking', 'min_price')
        #self.algFn.min_max_price_tracking()
        self.insertDailyListDataInfo('step01',len(MA01_ALGORITHM_LIST),'2019-03-13')
        self.updateDailyListDataInfo('step01',len(MA01_ALGORITHM_LIST),'2019-03-13')
        self.deleteDailyListDataInfo('2019-03-13')

if __name__=="__main__":
	ma01 = MA01()
	ma01.test()    

