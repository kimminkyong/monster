import sys
import time
import pandas as pd
from pandas import DataFrame
import datetime
import stock_code_crawler #종목 코드 크롤링 클래스
import alg_function as algFn
import ma01_monster
import monster_log


class PyMonster():
	def __init__(self):
		self.codeCrawler = stock_code_crawler.stockCodeCrawler()
		self.MA01 = ma01_monster.MA01()
		self.monsterLog = monster_log.monsterLog()

	def stock_item_code_crawling(self):
		self.monsterLog.add_log( 0, '종목 코드 찾기 시작!' )
		self.codeCrawler.marketCodeCrawling()

	def monster_brilliant_start(self):
		self.monster_first_setting()
		self.stock_item_code_crawling()
		self.monsterLog.add_log( 0, '설정기간동안의 일별정보 저장' )
		self.codeCrawler.get_stock_price_first('2018-06-01')
	
	def monster_daily_doit(self):
		log_today = datetime.datetime.now().strftime("%Y-%m-%d")
		log_text = str(log_today)+" MONSTER 종목별 정보 수집 시작!"
		self.monsterLog.add_log( 0, log_text )

		self.stock_item_code_crawling()
		self.codeCrawler.get_stock_price()

	def monster_first_setting(self):
		self.codeCrawler.frist_create_tables()
		self.monsterLog.add_log( 0, 'monster first setting DO!' )
		#today_stock_info 테이블 생성 
		#crawling_log 크롤링 로그 테이블 생성 
	
	def monster_alg_do(self):
		self.MA01.do_classification_algorithm()
	
		

if __name__=="__main__":
	pymonster = PyMonster()

	#pymonster.monster_brilliant_start()
	pymonster.monster_daily_doit()
	
	time.sleep(120) #내 컴은 소중하니깐(2분간 휴식)
	pymonster.monster_alg_do()
	

