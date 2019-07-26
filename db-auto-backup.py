import os
import time
import datetime


DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'kmk9972026324!'

#DB_NAME = 'stock_code_info'
DB_NAME = ['stock_code_info', 'stock_daily_info']
BACKUP_PATH = '/home/kmk1572/database_backup/'

DATETIME = time.strftime('%Y%m%d')
FOLDER = "monster_backup_database"
TODAYBACKUPPATH = BACKUP_PATH + FOLDER+"/" + DATETIME

#기존 백업 파일 삭제
delcmd = "find "+BACKUP_PATH+" -name 'monster_*' -type d -exec rm -r {} \;"
os.system(delcmd)
print("delete backup folder!!")


print("database backup start!!")
for i in range(len(DB_NAME)):
    if not os.path.exists(TODAYBACKUPPATH):
        os.makedirs(TODAYBACKUPPATH)

    if os.path.exists(DB_NAME[i]):
        file1 = open(DB_NAME[i])
        multi = 1
    else:
        multi = 0

    if multi:
        in_file = open(DB_NAME[i],"r")
        flength = len(in_file.readlines())
        in_file.close()
        p=1
        dbfile = open(DB_NAME[i],"r")

        while p <=flength:
            db = dbfile.readline()
            db = db[:-1]
            #dumpcmd = "mysqldump --login-path=dbautobackup -u "+DB_USER+" -p"+DB_USER_PASSWORD+" "+db+" > "+TODAYBACKUPPATH+"/"+db+".sql"
            dumpcmd = "mysqldump --login-path=dbautobackup "+db+" > "+TODAYBACKUPPATH+"/"+db+".sql"
            os.system(dumpcmd)
            p = p+1
        dbfile.close()
    else:
        db = DB_NAME[i]
        #dumpcmd = "mysqldump --login-path=dbautobackup -u "+DB_USER+" -p"+DB_USER_PASSWORD+" "+db+" > "+TODAYBACKUPPATH+"/"+db+".sql"
        dumpcmd = "mysqldump --login-path=dbautobackup "+db+" > "+TODAYBACKUPPATH+"/"+db+".sql"
        os.system(dumpcmd)

print("backup script complete!!")



