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

    def test(self):
        self.algFn.custom_add_colume('max_price', 'alg_step')
        self.algFn.custom_add_colume('min_price', 'max_price')
        self.algFn.custom_add_colume_bool('tracking', 'min_price')
        #self.algFn.min_max_price_tracking()

if __name__=="__main__":
	ma01 = MA01()
	ma01.test()    

