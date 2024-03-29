import sqlite3
import sys
import json
import os
from pathlib import Path
import pandas as pd
import sqlite3
from sentiment_analysis import sms_features
from upsert_to_sqlite import SqliteUpserter

sys.path.append('..')
sys.path.append('etl/SenderMap.json')

def load_iphonebackup(iphone_sms_sqlite_db_fp='etl/exports/iphone_backups/3d0d7e5fb2ce288813306e4d4636395e047a3d28'):
    with open('etl/SenderMap.json') as json_file:
        sender_map = json.load(json_file)
    with open('etl/transform/extract_from_iphone_backup.sql') as file:
        script = file.read()
    sender_list = ','.join(sender_map.keys())
    sql = script.replace('<list>', sender_list)
    conn = sqlite3.connect(iphone_sms_sqlite_db_fp)
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        sender = row[1]
        msg = row[2].replace('corey', '<recipient name>')
        timestamp = pd.to_datetime(row[7], infer_datetime_format=True) + pd.offsets.DateOffset(years=31)
        sms = sms_features(msg, timestamp.to_pydatetime(), sender)
        upserter = SqliteUpserter(sms)
        upserter.main()

def extract_sqlite():
    conn = sqlite3.connect('etl/sms.db')
    query = "SELECT * FROM sms;"
    df = pd.read_sql(query,conn)
    Path('../../political_sms_extracts').mkdir(parents=True, exist_ok=True)
    df.to_csv('../../political_sms_extracts/sms_extract.csv')
    print("saving extract to " + os.path.abspath('../../political_sms_extracts/sms_extract.csv'))


