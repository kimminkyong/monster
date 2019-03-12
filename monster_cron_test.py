#! /usr/lib/python3.5

import sys
import time
import datetime
import monster_log

class PyMonster():
	def __init__(self):
		self.monsterLog = monster_log.monsterLog()
	
	def test(self):
		self.monsterLog.add_log( 0, str(datetime.date.today().isoformat()) )
		self.monsterLog.add_log( 0, '주말 정기작업 테스트' )
		
if __name__=="__main__":
	pymonster = PyMonster()
	pymonster.test()
