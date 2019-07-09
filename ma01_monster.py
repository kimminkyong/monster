import sys
import time
import pandas as pd
from pandas import DataFrame
import datetime

import set_database_monster
import alg_function
import monster_log

MA01_ALGORITHM_LIST = []
MA01_ALGORITHM_TABLE = "MA01"
DUPLICATE_LIST = []

class MA01():
    def __init__(self):
        print("MA01 INIT!!")
        self.monsterDB  = set_database_monster.setDatabaseMonster()
        self.monsterLog = monster_log.monsterLog()
        self.algFn = alg_function.algFunctions()

    def createAlgorithmTable(self, tableName):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                curs.execute( "CREATE TABLE IF NOT EXISTS `"+tableName+"` (date  VARCHAR(20), code  VARCHAR(20), today_volume VARCHAR(255), avr30_volume VARCHAR(255), avr60_volume VARCHAR(255), change_per VARCHAR(100), alg_step VARCHAR(20), max_price VARCHAR(255), min_price VARCHAR(255), tracking BOOLEAN, base_price VARCHAR(255) )" )
        finally:
            sdi_db.commit()
            print("%s 테이블이 생성 되었습니다." %tableName)
    
    def createDailyAlgorithmListTable(self, tableName):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                curs.execute( "CREATE TABLE IF NOT EXISTS `"+tableName+"` (date  VARCHAR(20), step1  VARCHAR(20), step2 VARCHAR(20) )" )
        finally:
            sdi_db.commit()
            print("%s 테이블이 생성 되었습니다." %tableName)
    
    def initTableLowsToday(self):
        sdi_db = self.monsterDB.dbSDI()
        initToday = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            with sdi_db.cursor() as curs:
                curs.execute( "delete from "+MA01_ALGORITHM_TABLE+" where date='"+initToday+"'" )
        finally:
            sdi_db.commit()
            print("init table lows delete")
        
    
    def insertAlgorithmFilteringList(self, tableName, arrayData, algStep):
        sdi_db = self.monsterDB.dbSDI()
        
        for i in range(len(arrayData)):
            try:
                with sdi_db.cursor() as curs:
                    sql = "SELECT * FROM `today_stock_info` WHERE code='"+arrayData[i]+"' "
                    curs.execute(sql)
                    result = curs.fetchone()
                    if result:
                        self.insertListData(tableName, result, algStep)
                    else:
                        print("??")
            finally:
                print("find_date_stock_info")

    def insertListData(self, tableName, arrayData, algStep):
        sdi_db = self.monsterDB.dbSDI()
        avr30_vol = self.algFn.get_avr_volume(arrayData[0], 30)
        avr140_vol = self.algFn.get_avr_volume(arrayData[0], 140)
        
        try:
            with sdi_db.cursor() as curs:
                sql = "INSERT INTO `"+tableName+"` (code, date, today_volume, avr30_volume, avr60_volume, change_per, alg_step, base_price) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                curs.execute( sql, (arrayData[0], arrayData[1], int(arrayData[6]), int(avr30_vol), int(avr140_vol),  arrayData[7], algStep, int(arrayData[5]) ) )
        finally:
            sdi_db.commit()
    
    def insertDailyListDataInfo(self, step, lng):
        sdi_db = self.monsterDB.dbSDI()
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            with sdi_db.cursor() as curs:
                sql = "INSERT INTO `MA01_daily_list` (date, step1) values (%s,%s)"
                print(sql)
                curs.execute( sql, (todayString, lng ) )
        finally:
            sdi_db.commit()
    
    def updateAlgorithmFilteringList(self, arrayData, algStep):
        sdi_db = self.monsterDB.dbSDI()
        
        for i in range(len(arrayData)):
            try:
                with sdi_db.cursor() as curs:
                    sql = "SELECT * FROM `today_stock_info` WHERE code='"+arrayData[i]+"' "
                    curs.execute(sql)
                    result = curs.fetchone()
                    if result:
                        self.updateListData(result, algStep)
                    else:
                        print("find_date_stock_info")
            finally:
                print("find_date_stock_info")
    
    def updateListData(self, arrayData, algStep):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE "+MA01_ALGORITHM_TABLE+" SET alg_step = '"+algStep+"' WHERE code = '"+arrayData[0]+"' and date = '"+arrayData[1]+"' "
                print(sql)
                curs.execute( sql )
        finally:
            sdi_db.commit()
    
    def updateDailyListDataInfo(self, step, lng):
        sdi_db = self.monsterDB.dbSDI()
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE `MA01_daily_list` SET step2 = '"+str(lng)+"' WHERE date = '"+todayString+"' "
                print(sql)
                curs.execute( sql )
        finally:
            sdi_db.commit()

    def updateDailyListDataInfo3(self, step, lng):
        sdi_db = self.monsterDB.dbSDI()
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE `MA01_daily_list` SET step3 = '"+str(lng)+"' WHERE date = '"+todayString+"' "
                print(sql)
                curs.execute( sql )
        finally:
            sdi_db.commit()

    def duplicateDelete(self, arrayData):
        sdi_db = self.monsterDB.dbSDI()
        newArray = []
        for i in range(len(arrayData)):
            try:
                with sdi_db.cursor() as curs:
                    sql = "SELECT code FROM "+MA01_ALGORITHM_TABLE+" WHERE tracking = '1' AND code='"+arrayData[i]+"' "
                    curs.execute(sql)
                    result = curs.fetchone()
                    if result:
                        newArray.append(arrayData[i])
                    else:
                        print("tracking data")
            finally:
                print("duplicateDelete end")
        return newArray

    def do_anything(self):
        print("special doing")
        self.algFn.custom_add_colume('base_price', 'tracking')


    def do_classification_algorithm(self):
        print("MA01!! Do Classification Algorithm!")
        self.createAlgorithmTable(MA01_ALGORITHM_TABLE)
        self.createDailyAlgorithmListTable('MA01_daily_list')

        self.monsterLog.add_log( 1, 'MA01 알고리즘 검색 시작!!' )
        #최고가 최저가 범위 내의 종목 검색 
        MA01_ALGORITHM_LIST = self.algFn.min_max_price_filter(500, 50000)
        
        self.monsterLog.add_log( 1, '140거래일 동안의 거래량 10 이상의 종목 검색' )
        MA01_ALGORITHM_LIST = self.algFn.over_volume10_140day(MA01_ALGORITHM_LIST)
        print(MA01_ALGORITHM_LIST)
        
        self.monsterLog.add_log( 1, '양봉 종목 검색' )
        MA01_ALGORITHM_LIST = self.algFn.red_colum_check(MA01_ALGORITHM_LIST)
        print(MA01_ALGORITHM_LIST)
        
        self.monsterLog.add_log( 1, 'MA01 알고리즘 테이블 초기화 및 데이터 저장 시작!' )
        self.initTableLowsToday() #algorithm data table init before save data list


        DUPLICATE_LIST = self.duplicateDelete(MA01_ALGORITHM_LIST) #중복 종목 추출 
        self.monsterLog.add_log( 1, 'MA01 알고리즘 중복 종목 추출 완료!' )

        self.insertAlgorithmFilteringList(MA01_ALGORITHM_TABLE, MA01_ALGORITHM_LIST, 'step1')
        self.insertDailyListDataInfo('step01',len(MA01_ALGORITHM_LIST))
        print(MA01_ALGORITHM_LIST)
        self.monsterLog.add_log( 1, 'MA01 알고리즘 STEP1 저장 완료!' )
        
        #종가기준 140선을 통과한 종목 검색
        MA01_ALGORITHM_LIST = self.algFn.cross_over_line140(MA01_ALGORITHM_LIST)
        print(MA01_ALGORITHM_LIST)
        self.monsterLog.add_log( 1, 'MA01 알고리즘 검색 종료!!' )
        self.updateAlgorithmFilteringList(MA01_ALGORITHM_LIST, 'step2')
        self.monsterLog.add_log( 1, 'MA01 알고리즘 STEP2 업데이트 완료!' )
        self.updateDailyListDataInfo('step02',len(MA01_ALGORITHM_LIST))
        
        #중복 종목 update
        self.updateAlgorithmFilteringList(DUPLICATE_LIST, 'step3')
        self.updateDailyListDataInfo3('step03',len(DUPLICATE_LIST))

        self.monsterLog.add_log( 1, 'MA01 알고리즘 리스트 Tracking Start!!' )
        self.algFn.min_max_price_tracking()
        self.monsterLog.add_log( 1, 'MA01 알고리즘 리스트 Tracking End!!' )
        

