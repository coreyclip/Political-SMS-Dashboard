import sqlite3
import pandas as pd

class SqliteUpserter:
    def __init__(self, sms, sqlite_db_filepath='etl/sms.db'):
        self.sms = sms
        self.conn = self.create_connection(sqlite_db_filepath)
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Exception as e:
            print(e)
            raise e 

        return conn
    
    def check_schema(self):
        check_for_sms_table_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='sms';"
        cur = self.conn.cursor()
        cur.execute(check_for_sms_table_sql)
        return cur.fetchall()
    
    def insert_sms_record(self):
        """
        Inserts record into sms table
        """
        sms = self.sms
        sql = f'''
        INSERT INTO sms(SenderPhoneNumber, Sender, text, timestamp, month_name, day_name, day, hour, weekday, week, year, polarity, subjectivity, negativity, neutrality, positivity,
        compound, nouns, tags)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''

        values = (sms.sender_phone, sms.sender_name, sms.text,sms.received.strftime('%c'), sms.month_name, sms.day_name, sms.day, sms.hour, sms.weekday,
                  sms.week, sms.year, sms.polarity, sms.subjectivity, sms.negativity, sms.neutrality, sms.positivity, sms.compound, sms.nouns, sms.tags)
        cur = self.conn.cursor()
        try:
            cur.execute(sql, values)
        except Exception as e:
            print(f"failed to execute: {sql}")
            self.insert_sms_record_pandas()
            raise e
        self.conn.commit()

        return cur.lastrowid

    def insert_sms_record_pandas(self):
        sms = self.sms
        df = pd.dataframe(
                {

                    "SenderPhoneNumber": sms.sender_phone,
                    "Sender": sms.sender_name,
                    "text": sms.text,
                    "timestamp": sms.received.strftime('%c'), 
                    "month_name": sms.month_name, 
                    "day_name": sms.day_name,
                    "day": sms.day, 
                    "hour": sms.hour, 
                    "weekday": sms.weekday, 
                    "week": sms.week, 
                    "year": sms.year, 
                    "polarity": sms.polarity, 
                    "subjectivity": sms.subjectivity, 
                    "negativity": sms.negativity, 
                    "neutrality": sms.neutrality, 
                    "positivity": sms.positivity,
                    "compound": sms.compound, 
                    "nouns": sms.nouns, 
                    "tags": sms.tags

                }
            )
        df.to_sql('sms', self.conn, if_exists='append', index=False)
    def check_for_existing_record(self):
        sql = f'''
        SELECT Sender, text FROM sms
        WHERE SenderPhoneNumber = {self.sms.sender_phone}
        AND text =:sms
        '''
        sms_text = self.sms.text
        cur = self.conn.cursor()
        try:
            results = cur.execute(sql, {"sms":sms_text})
        except Exception as e:
            print(sql)
            raise e
        if len(results.fetchall()) > 0:
            return False
        else:
            return results
    def main(self):
        """
        method: inserts sms record if not duplicate
        """
        record_exists = self.check_for_existing_record()
        if record_exists:
            print(f"Record Already Exists")
        else:
            self.insert_sms_record()
