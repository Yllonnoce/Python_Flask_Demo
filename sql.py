import sqlite3
import subprocess
import os
from glob import glob
import time
from datetime import datetime, timedelta
import logging
from unittest import case
logging.basicConfig(filename='myapp.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

database = 'MusicLibrary.db'

def create_table():
    conn = sqlite3.connect(database)
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tblMusic(song_id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, song TEXT, pTimes INTEGER, playedDTTM TEXT, active INTEGER, genre INTEGER , que INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS tblHours(hours_id INTEGER PRIMARY KEY AUTOINCREMENT, startDTTM TEXT, endDTTM TEXT, startTime TEXT, endTime TEXT, gmt INTEGER, active INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS lutGenre(genre_id INTEGER PRIMARY KEY AUTOINCREMENT, genre TEXT, active INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS tblGlobalVar(globalVar_id INTEGER PRIMARY KEY AUTOINCREMENT, varName TEXT, varType TEXT, varValue TEXT, active INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS tbl(globalVar_id INTEGER PRIMARY KEY AUTOINCREMENT, varName TEXT, varType TEXT, varValue TEXT, active INTEGER)")
    conn.commit()
    c.close()
    conn.close()
    
    
def update_data_entry(row):
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    unix = time.time()
    _song_id = row[0]
    _playedDTTM = str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    _pTimes = row[4]
    _pTimes = _pTimes + 1
    _active = row[5]
    _que = 0
    c.execute("UPDATE tblMusic SET pTimes = ?, playedDTTM = ?, active = ?, que = ? where song_ID = ?",(_pTimes, _playedDTTM, _active,  _que, _song_id))
    conn.commit()
    c.close()
    conn.close()

def CRUD_tblHours(row,CRUD):
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    unix = time.time()
    if CRUD == "C":
        _startDTTM = row[1] #str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        _endDTTM = row[2]   #str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        _gmt = row[3]
        _active = row[4]
        c.execute("Insert INTO tblHours(startDTTM, endDTTM, gmt, active) VALUES(?, ?, ?, ?)",(_startDTTM, _endDTTM, _gmt, _active))
        conn.commit()
    elif CRUD == "R":
        _hours_id = row(0)
        c.execute("SELECT hours_id, startDTTM, endDTTM, gmt, active FROM tblHours where hours_id = ?", (_hours_id))
        conn.commit()
    elif CRUD == "U":
        _hours_id = row[0]
        _startDTTM = row[1] #str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        _endDTTM = row[2]   #str(datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        _gmt = row[3]
        _active = row[4]
        c.execute("UPDATE tblHours SET startDTTM = ?, endDTTM = ?, gmt = ?, active = ? where hours_id = ?",(_startDTTM, _endDTTM, _gmt,  _active, _hours_id))
        conn.commit()
    elif CRUD == "D":
        _hours_id = row(0)
        c.execute("Delete From tblHours where hours_id = ?", (_hours_id))
        conn.commit()
    else:
        c.execute("SELECT hours_id, startDTTM, endDTTM, gmt, active FROM tblHours")
        conn.commit()
    c.close()
    conn.close()

def CRUD_tblGlobalVars(row,CRUD):
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    unix = time.time()
    if CRUD == "C":
        _varName = row[1] 
        _varType = row[2]
        _varValue = row[3]
        _active = row[4]
        c.execute("Insert INTO tblGlobalVar(varName, varType, varValue, active)) VALUES(?, ?, ?, ?)",(_varName, _varType, _varValue, _active))
        conn.commit()
    elif CRUD == "R":
        _globalVar_id = row(0)
        c.execute("SELECT globalVar_id, varName, varType, varValue, active FROM tblGlobalVar where globalVar_id = ?", (_globalVar_id))
        conn.commit()
    elif CRUD == "U":
        _varName = row[1] 
        _varType = row[2]
        _varValue = row[3]
        _active = row[4]
        c.execute("UPDATE tblGlobalVar SET varName = ?, varType = ?, varValue = ?, active = ? where _globalVar_id = ?",(_varName, _varType, _varValue,  _active, _globalVar_id))
        conn.commit()
    elif CRUD == "D":
        globalVar_id = row(0)
        c.execute("Delete From tblGlobalVar where _globalVar_id = ?", (globalVar_id))
        conn.commit()
    else:
        c.execute("SELECT globalVar_id, varName, varType, varValue, active FROM tblGlobalVar")
        conn.commit()
    c.close()
    conn.close()

def select_play():
    blnEnd = 0
    while (blnEnd == 0):
        conn = sqlite3.connect(database)
        #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
        c = conn.cursor()
        c.execute("SELECT song_ID, (path || song),path,song,pTimes,active,que FROM tblMusic ORDER BY RANDOM()")
        data = c.fetchall()
        c.close()
        conn.close()
        for row in data:
           print(row[3])
           play_mp3(row[1])
           update_data_entry(row)
        blnEnd = 1 

def update_play_queue(_fn):
    songCount = 0
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("UPDATE tblMusic SET  que = 1 where path like '%" + _fn + "%' or song like '%" + _fn + "%'")
    conn.commit()
    data = c.execute("SELECT count(*) FROM tblMusic where que = 1")
    for row in data:
        songCount = row[0]
    c.close()
    conn.close()
    return songCount

def update_play_queue_selected(_selected):
    songCount = 0
    conn = sqlite3.connect(database)
    c = conn.cursor()
    for i in _selected:
        c.execute("UPDATE tblMusic SET  que = 1 where song_id = " + str(i))
        conn.commit()
    data = c.execute("SELECT count(*) FROM tblMusic where que = 1")
    for row in data:
        songCount = row[0]
    c.close()
    conn.close()
    return songCount

def select_play_queue():
    blnEnd = 0
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    while (blnEnd == 0):
        c.execute("SELECT song_ID, (path || song),path,song,pTimes,active,que FROM tblMusic WHERE que <> 0 ORDER BY RANDOM(), ROWID ASC LIMIT 1")
        data = c.fetchall()
        if len(data) == 0:
            blnEnd = 1
        else:    
            for row in data:
               print(row[3])
               play_mp3(row[1])
               update_data_entry(row)
    c.close()
    conn.close()

def select_play_threadQ():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT song_ID, (path || song),path,song,pTimes,active,que FROM tblMusic WHERE que <> 0 ORDER BY RANDOM(), ROWID ASC LIMIT 1")
    data = c.fetchall()
    c.close()
    conn.close()    
    for row in data:
        #update_data_entry(row)
        return row
    return ""

def queue_kill():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("UPDATE tblMusic SET  que = 0 where que = 1")
    conn.commit() 
    if os.name == "nt":
       #os.system("taskkill /f /im ffplay.exe")
       os.system("taskkill /f /im cmdmp3win.exe")
    else:
       os.system("pkill mpg123")
    c.close()
    conn.close()
    
def queue_next(): 
    if os.name == "nt":
       #os.system("taskkill /f /im ffplay.exe")
       os.system("taskkill /f /im cmdmp3win.exe")
    else:
       os.system("pkill mpg123")

def select_data_all():
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    c.execute("SELECT * FROM tblMusic")
    data = c.fetchall()
    for row in data:
       print(row[0], row[1],row[2],row[3])
    c.close()
    conn.close()
    
def delete_all(_tableName):
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    c.execute("DELETE FROM " + _tableName)
    conn.commit()
    c.close()
    conn.close()

def delete_songs(_selected):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    for i in _selected:
        c.execute("SELECT (path || song) FROM tblMusic where song_id = " + str(i))
        data = c.fetchall()
        for row in data:
            os.remove(row[0])
    for i in _selected:
        c.execute("Delete from tblMusic where song_id = " + str(i))
        conn.commit()
    c.close()
    conn.close()

def addSongToDB(fi):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    _pTimes = 0
    _playedDTTM = ""
    _active = 1
    _genre = 0
    _que = 1
    _path, _song = os.path.split(fi)
    if os.name == 'nt':
        _path = _path + "\\"
        _path.replace("\\","\\\\",0)
    else:
        _path = _path + "/"
    try:
        c.execute("INSERT INTO tblMusic(path, song, pTimes, playedDTTM, active, genre, que) VALUES(?, ?, ?, ?, ?, ?, ?)",(_path, _song, _pTimes, _playedDTTM, _active, _genre, _que))
        conn.commit()
    except Exception as err:
        logger.error(err)
        pass
    c.close()
    conn.close()

    
def find_store_files():
    files = []
    fileslocal = []
    start_dir = ""
    if os.name == 'nt':
        start_local  = os.path.dirname(os.path.realpath(__file__))
    else:
        start_dir  = "/media"
        start_local  = os.path.dirname(os.path.realpath(__file__))
    
    pattern   = "*.mp3"
    
    if os.name != 'nt':
        for dir,_,_ in os.walk(start_dir):
            files.extend(glob(os.path.join(dir,pattern)))

    for dir,_,_ in os.walk(start_local):
        fileslocal.extend(glob(os.path.join(dir,pattern)))

    conn = sqlite3.connect(database)
    c = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    _pTimes = 0
    _playedDTTM = ""
    _active = 1
    _genre = 0
    _que = 0
    if len(files) > 0:
        for file in files:
            _path, _song = os.path.split(file)
            if os.name == 'nt':
                _path = _path + "\\"
                _path.replace("\\","\\\\",0)
            else:
                _path = _path + "/"
            try:
                c.execute("INSERT INTO tblMusic(path, song, pTimes, playedDTTM, active, genre, que) VALUES(?, ?, ?, ?, ?, ?, ?)",(_path, _song, _pTimes, _playedDTTM, _active, _genre, _que))
                conn.commit()
            except Exception as err:
                logger.error(err)
                pass
    else:
        for file in fileslocal:
            _path, _song = os.path.split(file)
            if os.name == 'nt':
                _path = _path + "\\"
                _path.replace("\\","\\\\",0)
            else:
                _path = _path + "/"
            try:
                c.execute("INSERT INTO tblMusic(path, song, pTimes, playedDTTM, active, genre, que) VALUES(?, ?, ?, ?, ?, ?, ?)",(_path, _song, _pTimes, _playedDTTM, _active, _genre, _que))
                conn.commit()
            except Exception as err:
                logger.error(err)
                pass

    c.close()
    conn.close()
    

def play_mp3(fi):
   start_dir = os.path.dirname(os.path.realpath(__file__))
   if os.name == "nt":
      player = start_dir+"\\ffplay.exe"
      player.replace("\\","\\\\",0)
      fi.replace("\\","\\\\",0)
      subprocess.Popen([player, '-autoexit', fi]).wait()
   else:
      subprocess.Popen(['mpg123', '-q', fi]).wait()

def drop_table(_tableName):
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS " + _tableName)
    conn.commit()
    c.close()
    conn.close()
    
def get_table():
    conn = sqlite3.connect(database)
    #conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    data = c.fetchall()
    for row in data:
       print(row)
    c.close()
    conn.close()
    
def select_data_stats(a):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT 'Songs Stored' as T, Count(*) as C FROM tblMusic "
              + "UNION SELECT 'Songs Queued' as T, Count(*) as C FROM tblMusic where que <> 0 "
              + "UNION SELECT 'Total Songs Played' as T, SUM(pTimes) as C FROM tblMusic "
              + "UNION SELECT 'Song Current' as T, song as c FROM tblMusic where song_id = " + str(a[2]) + " "
              + "UNION SELECT 'Song Last' as T, song as c FROM tblMusic where song_id = " + str(a[3]) + " "
              + "UNION SELECT 'Song Volume' as T, " + str(a[1]) + " as c")
    data = c.fetchall()
    c.close()
    conn.close()
    return data

def select_data_allsongs():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT song_id, (path || song) FROM tblMusic ORDER BY path, song")
    data = c.fetchall()
    c.close()
    conn.close()
    return data


#drop_table('tblMusic')
#create_table()
#delete_all('tblMusic')
#find_store_files()
#queue_kill()
#update_play_queue('')
#select_play_queue()
#select_play()
#get_table()
#select_data_all()
#select_data_stats()
#select_data_allsongs()

 
