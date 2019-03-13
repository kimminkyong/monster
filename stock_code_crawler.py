import urllib
import time
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import datetime
import set_database_monster
import monster_log
import FinanceDataReader as fdr

pymysql.install_as_MySQLdb()

MARKET_CODE = []
MARKET_TOTAL_CODE={'code': [], 'name': [], 'sector': [], 'industry': []}

class stockCodeCrawler():
    def __init__(self):
        print("stock code crawler init!!")
        self.monsterDB  = set_database_monster.setDatabaseMonster()
        self.monsterLog = monster_log.monsterLog()

    def marketCodeCrawling(self):
        self.codeData = {'code': [], 'name': [], 'sector': [], 'industry': []}

        df_krx = fdr.StockListing('KRX')

        st_code = df_krx.Symbol
        st_name = df_krx.Name
        st_sector= df_krx.Sector
        st_industry = df_krx.Industry

        for i in range(len(df_krx)):
            self.codeData['code'].append(st_code[i])
            self.codeData['name'].append(st_name[i])
            self.codeData['sector'].append(st_sector[i])
            self.codeData['industry'].append(st_industry[i])

            MARKET_TOTAL_CODE['code'].append(st_code[i])
            MARKET_TOTAL_CODE['name'].append(st_name[i])
            MARKET_TOTAL_CODE['sector'].append(st_sector[i])
            MARKET_TOTAL_CODE['industry'].append(st_industry[i])

            MARKET_CODE.append(st_code[i])
            
        df = pd.DataFrame(MARKET_TOTAL_CODE, columns=['code', 'name', 'sector', 'industry'], index=MARKET_TOTAL_CODE['code'])
        engine = create_engine("mysql+pymysql://root:kmk9972026324!@localhost/stock_daily_info", encoding='utf-8')
        conn = engine.connect()
        df.to_sql(name='TOTAL_STOCK_CODE', con=engine, if_exists='replace', index=False) #전체 종목 코드 저장 

        self.makeItemCodeTable() #크롤링 된 시장별 종목 코드로 종목테이블 셋팅 

    def makeItemCodeTable(self):        
        for i in range(len(MARKET_CODE)):
            if self.checkExistItemTable(MARKET_CODE[i]) :
                self.createItemStockTable(MARKET_CODE[i])
            else:
                print("item table exist!")

    def checkExistItemTable(self, tableName):
        sci_db = self.monsterDB.dbSCI()
        curs = sci_db.cursor()
        curs.execute("""SHOW TABLES LIKE %s""", (tableName,))
        result = curs.fetchone()
        if result:
            return False
        else:
            return True
            
    def createItemStockTable(self, tableName):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                curs.execute( "CREATE TABLE IF NOT EXISTS `"+tableName+"` (date  VARCHAR(20), high VARCHAR(100), low VARCHAR(100), open VARCHAR(100), close VARCHAR(100), volume VARCHAR(255), change_per VARCHAR(100))" )
        finally:
            sci_db.commit()
            print("%s 종목 테이블이 생성 되었습니다." %tableName)

    def insert_daily_stock_info(self, tableName, arrayData):
        sci_db = self.monsterDB.dbSCI()
        sdi_db = self.monsterDB.dbSDI()
        if self.find_date_stock_info(arrayData[0], tableName) :
            try:
                with sci_db.cursor() as curs:
                    sql = "INSERT INTO `"+tableName+"` (date, high, low, open, close, volume, change_per) values (%s,%s,%s,%s,%s,%s,%s)"
                    curs.execute( sql, (arrayData[0], int(arrayData[1]), int(arrayData[2]), int(arrayData[3]), int(arrayData[4]), int(arrayData[5]), arrayData[6]) )
            finally:
                sci_db.commit()
        else:
            try:
                with sdi_db.cursor() as curs:
                    sql_today = "INSERT INTO `today_stock_info` (code, date, high, low, open, close, volume, change_per) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                    curs.execute( sql_today, (tableName, arrayData[0], int(arrayData[1]), int(arrayData[2]), int(arrayData[3]), int(arrayData[4]), int(arrayData[5]), arrayData[6]) )
                finally:
                    sdi_db.commit()        
    
    def find_date_stock_info(self, date, tableName):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                sql = "SELECT * FROM `"+tableName+"` WHERE date='"+date+"' LIMIT 1"
                curs.execute(sql)
                result = curs.fetchone()
                if result:
                    return False
                else:
                    return True
        finally:
            print("find_date_stock_info")

    def get_stock_price_info_today(self, itemCode):
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            dspi = fdr.DataReader(itemCode, todayString)
        except KeyError:
            print("KeyError")
        else:
            st_date = dspi.index.strftime("%Y-%m-%d")
            st_high = dspi.High
            st_low = dspi.Low
            st_open = dspi.Open
            st_close = dspi.Close
            st_volume = dspi.Volume
            st_change = dspi.Change

            if st_date[0] == todayString : #요청일과 리턴값의 날짜 MATCH 확인
                arrayInfo = []
                arrayInfo.append(st_date[0])
                arrayInfo.append(st_high[0])
                arrayInfo.append(st_low[0])
                arrayInfo.append(st_open[0])
                arrayInfo.append(st_close[0])
                arrayInfo.append(st_volume[0])
                arrayInfo.append('{:,.2f}'.format(round(st_change[0]*100, 2)) )
                print(arrayInfo)

                self.insert_daily_stock_info(itemCode, arrayInfo)
            else:
                print('day match error')
    
    def get_stock_price(self):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                curs.execute( "TRUNCATE TABLE `today_stock_info`" )
        finally:
            sdi_db.commit()

        num = 0
        for i in range(len(MARKET_CODE)):
            count = str(num)+"/"+str(len(MARKET_CODE))+" (종목코드 : "+MARKET_CODE[i]+")"
            self.get_stock_price_info_today(MARKET_CODE[i])
            num = num+1
            print(count)





    # brilliant start code
    def frist_create_tables(self):
        sdi_db = self.monsterDB.dbSDI()
        # today_stock_info table create
        # monster_log table create
        try:
            with sdi_db.cursor() as curs:
                curs.execute( "CREATE TABLE IF NOT EXISTS `today_stock_info` (code VARCHAR(20), date VARCHAR(20), high VARCHAR(100), low VARCHAR(100), open VARCHAR(100), close VARCHAR(100), volume VARCHAR(255), change_per VARCHAR(100))" )
                curs.execute( "CREATE TABLE IF NOT EXISTS `monster_log` (date VARCHAR(20), log_kind VARCHAR(20), content TEXT, error_step VARCHAR(20), result VARCHAR(20))" )
        finally:
            sdi_db.commit()
    def insert_daily_stock_info_first(self, tableName, arrayData):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                sql_today = "INSERT INTO `today_stock_info` (code, date, high, low, open, close, volume, change_per) values (%s,%s,%s,%s,%s,%s,%s,%s)"
                curs.execute( sql_today, (tableName, arrayData[0], int(arrayData[1]), int(arrayData[2]), int(arrayData[3]), int(arrayData[4]), int(arrayData[5]), arrayData[6]) )        
        finally:
            sdi_db.commit()

    def get_stock_price_info_first(self, itemCode, sDay):
        dspi = fdr.DataReader(itemCode, sDay)
        self.stockDaylyInfo = {'date': [], 'high': [], 'low': [], 'open': [], 'close': [], 'volume': [], 'change_per': []}

        st_date = dspi.index.strftime("%Y-%m-%d")
        st_high = dspi.High
        st_low = dspi.Low
        st_open = dspi.Open
        st_close = dspi.Close
        st_volume = dspi.Volume
        st_change = dspi.Change
        
        for i in range(len(dspi)):
            self.stockDaylyInfo['date'].append(st_date[i])
            self.stockDaylyInfo['high'].append(st_high[i])
            self.stockDaylyInfo['low'].append(st_low[i])
            self.stockDaylyInfo['open'].append(st_open[i])
            self.stockDaylyInfo['close'].append(st_close[i])
            self.stockDaylyInfo['volume'].append(st_volume[i])
            self.stockDaylyInfo['change_per'].append('{:,.2f}'.format(round(st_change[i]*100, 2)))

        #print(self.stockDaylyInfo)

        df = pd.DataFrame(self.stockDaylyInfo, columns=['date', 'high', 'low', 'open', 'close', 'volume', 'change_per' ], index=self.stockDaylyInfo['date'])
        engine = create_engine("mysql+pymysql://root:kmk9972026324!@localhost/stock_code_info", encoding='utf-8')
        conn = engine.connect()
        df.to_sql(name=itemCode, con=engine, if_exists='replace', index=False, index_label='date')

    def today_stock_info_set_today(self, itemCode):
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")
        try:
            dspi = fdr.DataReader(itemCode, todayString)
        except KeyError:
            print("KeyError")
        else:
            st_date = dspi.index.strftime("%Y-%m-%d")
            st_high = dspi.High
            st_low = dspi.Low
            st_open = dspi.Open
            st_close = dspi.Close
            st_volume = dspi.Volume
            st_change = dspi.Change

            if st_date[0] == todayString : #요청일과 리턴값의 날짜 MATCH 확인
                arrayInfo = []
                arrayInfo.append(st_date[0])
                arrayInfo.append(st_high[0])
                arrayInfo.append(st_low[0])
                arrayInfo.append(st_open[0])
                arrayInfo.append(st_close[0])
                arrayInfo.append(st_volume[0])
                arrayInfo.append('{:,.2f}'.format(round(st_change[0]*100, 2)) )
                print(arrayInfo)

                self.insert_daily_stock_info_first(itemCode, arrayInfo)
            else:
                print('day match error')

    def get_stock_price_first(self, startDay):
        num = 0
        tnum = 0
        for i in range(len(MARKET_CODE)):
            count = str(num)+"/"+str(len(MARKET_CODE))+" (종목코드 : "+MARKET_CODE[i]+")"
            self.get_stock_price_info_first(MARKET_CODE[i], startDay)
            num = num+1
            print(count)

        for i in range(len(MARKET_CODE)):
            tcount = str(tnum)+"/"+str(len(MARKET_CODE))+" (종목코드 : "+MARKET_CODE[i]+")"
            self.today_stock_info_set_today(MARKET_CODE[i])
            tnum = tnum+1
            print(tcount)

    





    