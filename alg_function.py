import sys
import os
import datetime
import requests
import set_database_monster

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class algFunctions():
    def __init__(self):
        print('monster algorithm functions!')
        self.monsterDB  = set_database_monster.setDatabaseMonster()
    
    def min_max_price_filter(self, min, max):
        sdi_db = self.monsterDB.dbSDI()
        try:
            with sdi_db.cursor() as curs:
                lst=[]
                sql = "SELECT * FROM `today_stock_info` "
                curs.execute(sql)
                items = curs.fetchall()
                for i in range(len(items)):
                    price = int(items[i][5])
                    print(price)
                    if max > price > min:
                        lst.append(items[i][0])
                return lst
        finally:
            print("min_max_price_filter OK!!")
    
    def over_volume10_30day(self, arry):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                
                lst=[]
                for i in range(len(arry)):
                    in_list = []
                    todayVolume = 0
                    sum29 = 0

                    sql = "SELECT volume,date FROM `"+arry[i]+"` ORDER BY date DESC"
                    curs.execute(sql)
                    items = curs.fetchmany(30)
                    for j in range(len(items)):
                        in_list.append(items[j][0])
                    
                    # 거래일이 30일 이상인지 확인 
                    if len(in_list) < 30 :
                        print("30일이 않됨")
                    else : 
                        todayVolume = int(in_list[0])
                        sum29 = int(sum(in_list)) - int(in_list[0])
                        
                    if( int(todayVolume) > int((sum29/29)*10) ):
                        lst.append(arry[i])
                return lst
        finally:
            print("over_volume10_30day OK!!")
    
    def over_volume10_140day(self, arry):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                
                lst=[]
                for i in range(len(arry)):
                    in_list = []
                    todayVolume = 0
                    sum139 = 0

                    sql = "SELECT volume,date FROM `"+arry[i]+"` ORDER BY date DESC"
                    curs.execute(sql)
                    items = curs.fetchmany(140)
                    for j in range(len(items)):
                        in_list.append(items[j][0])
                    
                    # 거래일이 30일 이상인지 확인 
                    if len(in_list) < 140 :
                        print("30일이 않됨")
                    else : 
                        print(arry[i])
                        print(int(in_list[0]))
                        print(in_list)
                        in_list = list(map(int, in_list))#리스트의 값이 str로 넘겨올 경우 
                        todayVolume = int(in_list[0])
                        sum139 = int(sum(in_list)) - int(in_list[0])
                        
                    if( int(todayVolume) > int((sum139/139)*10) ):
                        lst.append(arry[i])
                return lst
        finally:
            print("over_volume10_140day OK!!")

    def red_colum_check(self, arry):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                lst=[]
                for i in range(len(arry)):
                    start_price = 0
                    end_price = 0

                    sql = "SELECT * FROM `"+arry[i]+"` ORDER BY date DESC"
                    curs.execute(sql)
                    items = curs.fetchone()
                    start_price = items[3]
                    end_price = items[4]

                    if(int(end_price) > int(start_price)):
                        lst.append(arry[i])
                return lst
        finally:
            print("red_colum_check OK!")

    def cross_over_line140(self, arry):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                lst=[]
                for i in range(len(arry)):
                    in_list = []
                    st_p = 0
                    en_p = 0

                    sql = "SELECT close, open FROM `"+arry[i]+"` ORDER BY date DESC"
                    curs.execute(sql)
                    items = curs.fetchmany(140)

                    if len(items) < 140 :
                        print("140Day Data to lack!!")
                    else :
                        for j in range(len(items)):
                            if(j == 0):
                                st_p = int(items[j][1])
                                en_p = int(items[j][0])
                            in_list.append(items[j][0])
                        # print("inlist")
                        # print(in_list)
                        # print(sum(in_list))
                        # print(st_p)
                        # print(en_p)
                        # print( int(sum(in_list)/len(in_list)) )
                        p140 = int(sum(in_list)/len(in_list))
                        if p140 > int(st_p) and p140 < int(en_p):
                            lst.append(arry[i])
                return lst
        finally:
            print("cross_over_line140 OK!!")

    def get_avr_volume(self, code, day):
        sci_db = self.monsterDB.dbSCI()
        print(code)
        try:
            with sci_db.cursor() as curs:
                day_len = int(day)
                avrVolume = 0
                in_list=[]
                sql = "SELECT volume FROM `"+code+"` ORDER BY date DESC"
                curs.execute(sql)
                items = curs.fetchmany(day_len)

                for j in range(len(items)):
                    in_list.append(items[j][0])
                
                in_list = list(map(int, in_list))

                # 거래일이 30일 이상인지 확인 
                if len(in_list) < day_len :
                    print(" 거래일 부족! ")
                else : 
                    print(in_list)
                    sumVolume = int(sum(in_list)) - int(in_list[0])
                    
                    avrVolume = int(sumVolume/day_len)
                return avrVolume
        finally:
            print("get_avr_volume OK!!")

    def get_today_per_close(self, code):
        sci_db = self.monsterDB.dbSCI()
        try:
            with sci_db.cursor() as curs:
                sql = "SELECT close FROM `"+code+"` ORDER BY date DESC"
                curs.execute(sql)
                items = curs.fetchmany(2)
                pcv = round( ( int(items[0][0]) - int(items[1][0]) ) / int(items[1][0]) *100 , 2)
                return pcv
        finally:
            print("get_today_per_close OK!!")

    def min_max_price_between_date(self, code, sdate):
        todayString = datetime.datetime.now().strftime("%Y-%m-%d")

        tomorrows = datetime.datetime.today()+datetime.timedelta(days=1)
        tomorrowsString = tomorrows.strftime("%Y-%m-%d")
        print(tomorrowsString)

        atday = datetime.datetime.today()-datetime.timedelta(days=30)
        atdayString = atday.strftime("%Y-%m-%d")
        print(atdayString)
        
        startday = datetime.datetime( int(sdate[0:4]),int(sdate[5:7]),int(sdate[8:10]),0,0,0,0)+datetime.timedelta(days=1) 
        startdayString = startday.strftime("%Y-%m-%d")
        print(startdayString)

        sci_db = self.monsterDB.dbSCI()
        max_list = []
        min_list = []
        return_list=[]
        last_flag = False
        try:
            with sci_db.cursor() as curs:
                if sdate == todayString:
                    sql = "SELECT close FROM `"+code+"` WHERE date BETWEEN '"+sdate+"' AND '"+tomorrowsString+"' ORDER BY date DESC"
                    print(sql)
                    curs.execute(sql)
                    items = curs.fetchall()
                    print(items)
                    last_flag = True
                    for i in range(len(items)):
                        max_list.append(items[i][0])
                        min_list.append(items[i][0])
                else:
                    sql = "SELECT high,low FROM `"+code+"` WHERE date BETWEEN '"+startdayString+"' AND '"+tomorrowsString+"' ORDER BY date DESC"
                    print(sql)
                    curs.execute(sql)
                    items = curs.fetchall()
                    print(items)
                    for i in range(len(items)):
                        max_list.append(items[i][0])
                        min_list.append(items[i][1])
                
        finally:
            if(len(max_list) == 0 or len(min_list) == 0):
                return_list.append(0)
                return_list.append(0)
                return_list.append(True)
            else:
                print(max_list)
                print(min_list)
                return_list.append(max(max_list))
                return_list.append(min(min_list))
                return_list.append(last_flag)
            print(return_list)
            print("min max price check!")
            return return_list

    def custom_add_colume(self, c_name, after_colume):
        sdi_db = self.monsterDB.dbSDI()

        try:
            with sdi_db.cursor() as curs:
                sql = "ALTER TABLE `MA01` ADD "+c_name+" VARCHAR(255) AFTER "+after_colume+" "
                print(sql)
                curs.execute(sql)
        finally:
            print(c_name)
    
    def custom_add_colume_bool(self, c_name, after_colume):
        sdi_db = self.monsterDB.dbSDI()

        try:
            with sdi_db.cursor() as curs:
                sql = "ALTER TABLE `MA01` ADD "+c_name+" BOOLEAN AFTER "+after_colume+" "
                print(sql)
                curs.execute(sql)
        finally:
            print(c_name)
    
    def delete_table_column(self):
        sdi_db = self.monsterDB.dbSDI()

        try:
            with sdi_db.cursor() as curs:
                sql = "ALTER TABLE `MA01` drop `tracking`"
                print(sql)
                curs.execute(sql)
        finally:
            print("삭제완료")

    def get_max_price_date(self, code, price, flag):
        sci_db = self.monsterDB.dbSCI()
        print("get_max_price_date")
        print(code)
        print(price)
        try:
            with sci_db.cursor() as curs:
                if(flag):
                    sql = "SELECT date FROM `"+code+"` WHERE close = "+price+" ORDER BY date DESC"
                else:
                    sql = "SELECT date FROM `"+code+"` WHERE high = "+price+" ORDER BY date DESC"
                print(sql)
                curs.execute(sql)
                items = curs.fetchone()
                print(items[0])
                m_date = str(items[0])
                return m_date
        finally:
            sci_db.commit()
            print("max date!")
   

    def min_max_price_update(self, date, code, max_p, min_p, flag):
        sdi_db = self.monsterDB.dbSDI()
        if(max_p == '0' or min_p == '0' ):
            max_date = '0000-00-00'
        else:
            max_date = self.get_max_price_date(code, max_p, flag)
        print(max_date)
        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE `MA01` SET max_date = '"+max_date+"', max_price = "+max_p+", min_price = "+min_p+", tracking = 1 WHERE code = '"+code+"' and date = '"+date+"' "
                result = curs.execute( sql )
                print(result)
        finally:
            sdi_db.commit()
            print("종목 트래킹 완료!")
    
    def min_max_price_tracking(self):
        sdi_db = self.monsterDB.dbSDI()
        tomorrows = datetime.datetime.today()+datetime.timedelta(days=1)
        tomorrowsString = tomorrows.strftime("%Y-%m-%d")

        atday = datetime.datetime.today()-datetime.timedelta(days=60)
        atdayString = atday.strftime("%Y-%m-%d")

        try:
            with sdi_db.cursor() as curs:
                sql = "UPDATE `MA01` SET tracking=0"
                curs.execute(sql)
        finally:
            sdi_db.commit()
            print("MA01 테이블 tracking colume 초기화!")

        try:
            with sdi_db.cursor() as curs:
                sql = "SELECT date,code FROM `MA01` WHERE date BETWEEN '"+atdayString+"' AND '"+tomorrowsString+"' ORDER BY date DESC"
                curs.execute(sql)
                result = curs.fetchall()
                if result:
                    for i in range(len(result)):
                        nx_price = self.min_max_price_between_date(result[i][1], result[i][0])
                        self.min_max_price_update(result[i][0], result[i][1], str(nx_price[0]), str(nx_price[1]), nx_price[2])
                else:
                    print("MA01 table list get error")
        finally:
            print("min_max_price_tracking!")

        


    






        
        



"""

def min_max_price_filter(min, max):
    print("min_max_price_filter")
    list = []
    query_st = "select * from stock_item_info"
    conn = sqlite3.connect("c:/stock/daily_stock_item_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()
    for i in range(len(items)):
        price = int(items[i][5].replace(",",""))
        if max > price > min:
            list.append(items[i][0])
    print(list)
    return list

def daily_items_total_info(code):
    info_list = []
    query = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query)
    item_info = cur.fetchone()

    query_st = "select * from stock_item_info where item_code='"+code+"'"
    conn_st = sqlite3.connect("c:/stock/daily_stock_item_info.db")
    cur_st = conn_st.cursor()
    cur_st.execute(query_st)
    items_h30 = cur_st.fetchone()

    info_list.append(code)
    for i, val in enumerate(item_info):
        info_list.append(val)
    info_list.append(items_h30[8])
    print(info_list)
    return info_list

def over_volume10_30day(code):
    mk_list = []
    query_st = "select volume from '"+code+"'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchmany(30)
    for item in items:
        mk_list.append(item[0])

    if len(mk_list) < 30 :
        print("30일이 않됨")
        return False
    print("111")
    today_value = 0
    manydays_value = 0

    query_st_per = "select * from '"+code+"'"
    cur_per = conn.cursor()
    cur_per.execute(query_st_per)
    items_per = cur_per.fetchone()

    tcp_org = items_per[6].replace(",","")
    print(tcp_org)

    if tcp_org[0] == "+":
        tcp_val = int(tcp_org.replace("+", "")) / (int(items_per[4].replace(",","")) - int(tcp_org.replace("+",""))) * 100
        tcp_val = round(tcp_val, 2)
    else:
        tcp_val = int(tcp_org.replace("-", "")) / (int(items_per[4].replace(",","")) + int(tcp_org.replace("-", ""))) * 100
        tcp_val = round(tcp_val, 2)
    print(tcp_val)

    for i, val in enumerate(mk_list):
        val = val.replace(",","")
        if i ==0 :
            today_value = int(val)
        else:
            manydays_value = manydays_value + int(val)

    if today_value == 0 or manydays_value == 0 :# 신규종목 제외
        return False

    if today_value > round(manydays_value/29)*10 :
        avr = manydays_value/29
        alg1StockDetailInfo[code] = {"tdv":today_value, "arv":round(avr), "cnt":round(today_value/avr), "hlt":"#ffffff", "tcp":tcp_val, "cls":items_per[4], "code":code}
        #alg1StockDetailInfo[code] = {"tdv":today_value, "arv":round(avr), "cnt":round(today_value/avr), "hlt":"#ffffff"}
        return True
    else :
        return False

def price_highest_200day(code):
    high_list = []
    today_close = 0
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for i in range(len(items)):
        if i == 0:
            today_close = int(items[0][4].replace(",",""))
        else:
            high_list.append(int(items[i][2].replace(",","")))

    high_close = max(high_list)

    if today_close > high_close :
        return True
    else:
        return False

def price_highest_100day(code):
    high_list = []
    today_close = 0
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    if len(items) > 100:
        list_len = 100
    else:
        list_len = len(items)

    for i in range(list_len):
        if i == 0:
            today_close = int(items[0][4].replace(",",""))
        else:
            high_list.append(int(items[i][2].replace(",","")))

    high_close = max(high_list)

    if today_close > high_close :
        return True
    else:
        return False

def max_high_price200(code):
    high_list = []
    high_price = 0
    query_st = "select high from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        high_list.append(int(item[0].replace(",","")))

    high_price = max(high_list)
    return high_price

def max_high_price30(code):
    high_list = []
    high_price = 0
    query_st = "select high from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchmany(30)

    for item in items:
        high_list.append(int(item[0].replace(",","")))

    high_price = max(high_list)
    return high_price

def cross_over_line140(code):
    avr_query = "select * from '" + code + "'"
    avr_conn = sqlite3.connect("c:/stock/daily_stock_move_average.db")
    avr_cur = avr_conn.cursor()
    avr_cur.execute(avr_query)
    avr_price = avr_cur.fetchone()

    today_query = "select * from '" + code + "'"
    today_conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    today_cur = today_conn.cursor()
    today_cur.execute(today_query)
    today_price = today_cur.fetchone()

    if price_to_number(today_price[1]) < int(avr_price[6]) < price_to_number(today_price[4]):
        return True
    else:
        return False

def before_cross_over_line140(code):
    avr_query = "select * from '" + code + "'"
    avr_conn = sqlite3.connect("c:/stock/daily_stock_move_average.db")
    avr_cur = avr_conn.cursor()
    avr_cur.execute(avr_query)
    avr_price = avr_cur.fetchone()

    today_query = "select * from '" + code + "'"
    today_conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    today_cur = today_conn.cursor()
    today_cur.execute(today_query)
    today_price = today_cur.fetchone()

    if int(avr_price[6]) > price_to_number(today_price[4]) > int(round(avr_price[6]*0.9)):
        return True
    else:
        return False


def red_colum_check(code):
    print("red_colum_check")
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchone()
    start_price = items[1]
    end_price = items[4]

    print(price_to_number(start_price))
    print(price_to_number(end_price))

    if price_to_number(start_price) < price_to_number(end_price):
        print("red colum")
        return True
    else:
        print("blue colum")
        return False

def stock_code_table_exist_check(code):
    # 실제 데이터 테이블이 있는지 확인
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur_table = conn.cursor()
    cur_table.execute('select name from sqlite_master where type="table" and name="' + code + '"')
    all_list = cur_table.fetchall()
    if len(all_list) > 0:
        return True
    else :
        return False

def price_to_number(in_str):
    int_value = int(in_str.replace(",",""))
    return int_value

def black_list_remove(org_list, remove_list):
    for i, lst in enumerate(remove_list):
        if lst in org_list:
            org_list.remove(lst)
    return org_list

def daily_stock_info_comfirm(last_day, list):
    error_code_list = []
    not_exist_code_table = []
    for i, code in enumerate(list):
        print(code)
        if stock_code_table_exist_check(code):
            query_st = "select * from '" + code + "'"
            conn = sqlite3.connect("c:/stock/daily_stock_info.db")
            cur = conn.cursor()
            cur.execute(query_st)
            items = cur.fetchone()
            save_last_day = items[0]
            if last_day != save_last_day:
                error_code_list.append(code)
        else:
            not_exist_code_table.append(code)
    error_code_list = error_code_list+not_exist_code_table
    msg = "일별 데이터 중 오류 데이터는 총 "+str(len(error_code_list))+"개가 확인 되었습니다."
    print(msg)
    return error_code_list

def today_now():
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    nowDate = nowDate.replace("-",".")
    return nowDate

def today_now_bar_type():
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    return nowDate

def db_file_remove(file_path):
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except:
            print('파일이 삭제되지 않았습니다')
    else:
        print('파일이 존재하지 않습니다')


def make_rising_stock_list():
    list = []
    query_st = "select * from before_line140_item"
    conn = sqlite3.connect("c:/stock/daily_stock_before_item_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        inner_list = []
        inner_list.append(item[0])
        inner_list.append(item[1])
        list.append(inner_list)

    return list

def make_rising_stock_str():
    rising_str = ""
    query_st = "select * from before_line140_item"
    conn = sqlite3.connect("c:/stock/daily_stock_before_item_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        rising_str = rising_str+str(item[0])+";"

    return rising_str

def make_rising_stock_dic():
    dic = {}
    query_st = "select * from before_line140_item"
    conn = sqlite3.connect("c:/stock/daily_stock_before_item_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        dic[item[0]] = item[1]

    return dic

def make_rising_stock_check_list():
    list = []
    query_st = "select * from before_line140_item"
    conn = sqlite3.connect("c:/stock/daily_stock_before_item_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        list.append(item[0])

    return list

def del_up_down_mark(num):
    renum = num.replace("+","").replace("-","")
    return renum

def firestore_save_stock_info(code):
    list = []

    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for item in items:
        inner_list = []
        inner_list.append(item[0])
        inner_list.append(item[1])
        inner_list.append(item[2])
        inner_list.append(item[3])
        inner_list.append(item[4])
        inner_list.append(item[5])
        list.append(inner_list)

    return list

def firestore_save_stock_info_5day(code):
    list = []

    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchmany(5)

    for item in items:
        inner_list = []
        inner_list.append(item[0])
        inner_list.append(item[1])
        inner_list.append(item[2])
        inner_list.append(item[3])
        inner_list.append(item[4])
        inner_list.append(item[5])
        list.append(inner_list)

    return list

def firestore_save_stock_info_day(code):
    list = []

    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchmany(1)

    for item in items:
        inner_list = []
        inner_list.append(item[0])
        inner_list.append(item[1])
        inner_list.append(item[2])
        inner_list.append(item[3])
        inner_list.append(item[4])
        inner_list.append(item[5])
        list.append(inner_list)

    return list


def mmd_200day_save(code, name):
    #print('mk2 mmd_200day_save')
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchall()

    for i in range(len(items)):
        high = items[i][2].replace(",","")
        low = items[i][3].replace(",", "")
        start = items[i][1].replace(",", "")
        end = items[i][4].replace(",", "")
        volum = items[i][5].replace(",", "")
        day = items[i][0]
        dayPriceUrl = 'http://kmk6324.cafe24.com/monster/save_stock_info.html?code='+code+'&name='+name+'&high='+high+'&low='+low+'&start='+start+'&end='+end+'&volum='+volum+'&date='+day
        r = requests.get(dayPriceUrl)

def mmd_5day_save(code, name):

    sQuery = "select count(*) from sqlite_master Where Name = '" + code + "'" #table 존재 체크 쿼리
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")

    cur_ex = conn.cursor()
    cur_ex.execute(sQuery)
    ex_que = cur_ex.fetchone()

    if(ex_que[0] == 1):
        cur = conn.cursor()
        cur.execute(query_st)
        items = cur.fetchmany(5)

        for i in range(len(items)):
            high = items[i][2].replace(",", "")
            low = items[i][3].replace(",", "")
            start = items[i][1].replace(",", "")
            end = items[i][4].replace(",", "")
            volum = items[i][5].replace(",", "")
            day = items[i][0]
            dayPriceUrl = 'http://kmk6324.cafe24.com/monster/save_stock_info.html?code=' + code + '&name=' + name + '&high=' + high + '&low=' + low + '&start=' + start + '&end=' + end + '&volum=' + volum + '&date=' + day
            r = requests.get(dayPriceUrl)


def mmd_day_save(code, name):
    # print('mk2 mmd_200day_save')
    query_st = "select * from '" + code + "'"
    conn = sqlite3.connect("c:/stock/daily_stock_info.db")
    cur = conn.cursor()
    cur.execute(query_st)
    items = cur.fetchone()

    for i in range(len(items)):
        high = items[i][2].replace(",", "")
        low = items[i][3].replace(",", "")
        start = items[i][1].replace(",", "")
        end = items[i][4].replace(",", "")
        volum = items[i][5].replace(",", "")
        day = items[i][0]
        dayPriceUrl = 'http://kmk6324.cafe24.com/monster/save_stock_info.html?code=' + code + '&name=' + name + '&high=' + high + '&low=' + low + '&start=' + start + '&end=' + end + '&volum=' + volum + '&date=' + day
        r = requests.get(dayPriceUrl)


################################### email ##################################

def sendMail(title, text, target):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('mk2monster1572@gmail.com', 'kmk9972026324')

    msg = MIMEText(text)
    msg['Subject'] = title
    msg['To'] = 'kmk1572@gmail.com'
    smtp.sendmail('mk2monster1572@gmail.com', target, msg.as_string())
    smtp.quit()

def sendStockMultiMail(title, target, list):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login('mk2monster1572@gmail.com', 'kmk9972026324')

    list_text = ""
    list_text += "<table border='1' style='width:100%;border-collapse:collapse;border-spacing:0;border:1px solid #ddd; border-right:0;border-bottom:0;font-size:11px'>"
    list_text += "<colgroup><col style='width:20%'><col style='width:20%'><col style='width:10%'><col style='width:20%'><col style='width:20%'><col style='width:10%'></colgroup>"
    list_text += "<thead>"
    list_text += "<tr>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>종목</th>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>종가</th>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>상승률</th>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>오늘 거래량</th>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>평균 거래량</th>"
    list_text += "<th style='border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:#f6f6f6'>대비</th>"
    list_text += "</tr>"
    list_text += "</thead>"
    list_text += "<tbody>"
    for i in range(len(list)):
        color = str(list[i][4])
        list_text += "<tr>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:center;background:"+color+"'>"+list[i][0]+"</td>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:right;background:"+color+"'>"+list[i][6]+"원</td>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:right;background:"+color+"'>"+list[i][5]+"% </td>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:right;background:"+color+"'>"+list[i][1]+"주</td>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:right;background:"+color+"'>"+list[i][2]+"주</td>"
        list_text += "<td style='padding:5px;border-right:1px solid #ddd;border-bottom:1px solid #ddd;text-align:right;background:"+color+"'>"+list[i][3]+"배</td>"
        list_text += "</tr>"
    list_text += "</tbody>"
    list_text +="</table>"

    text = \"""
        <html>
          <head></head>
          <body>
            <p>안녕하십니까?!</p>
            <strong>금일[\"""+today_now()+\"""] 검색 종목을 안내드립니다.</strong>
            <br>
            \"""+list_text+\"""
          </body>
        </html>
    \"""
    msg1 = MIMEText(text, 'html')
    msg = MIMEMultipart('alternative')
    msg.attach(msg1)
    msg['Subject'] = title
    msg['To'] = 'kmk1572@gmail.com'
    smtp.sendmail('mk2monster1572@gmail.com', target, msg.as_string())
    smtp.quit()


"""