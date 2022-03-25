import sqlite3
import json
from sentiment_analysis import sms_features

def load_iphonebackup(iphone_sms_sqlite_db_fp='exports/iphone_backups/3d0d7e5fb2ce288813306e4d4636395e047a3d28'):
    with open('SenderMap.json') as json_file:
        sender_map = json.load(json_file)
    with open('transform/extract_from_iphone_backup.sql') as file:
        script = file.read()
    sender_list = ','.join(sender_map.keys())
    sql = script.replace('<list>', sender)
    conn = sqlite3.connect(iphone_sms_sqlite_db_fp)
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
