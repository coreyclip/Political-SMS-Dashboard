import sqlite3
import json

class SqliteUpserter:
    def __init__(self, sms, sqlite_db_filepath='sms.db'):
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
        text = json.dumps(sms.text) \
                          .replace('"', '') \
                          .replace("'", "\'")
        sql = f'''
        INSERT INTO sms(SenderPhoneNumber, Sender, text, timestamp, month_name, day_name, day, hour, weekday, week, year, polarity, subjectivity, negativity, neutrality, positivity, compound, nouns, tags)
        VALUES({sms.sender_phone},"{sms.sender_name}","{text}", "{sms.received.strftime('%c')}", "{sms.month_name}", "{sms.day_name}", "{sms.day}", "{sms.hour}", "{sms.weekday}", "{sms.week}", "{sms.year}", "{sms.polarity}", "{sms.subjectivity}", "{sms.negativity}", "{sms.neutrality}", "{sms.positivity}", "{sms.compound}", "{sms.nouns}", "{sms.tags}")
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            error = str(e)
            error_msg = f"""
            failed to execute this sql statement:
            ---------------
            {sql}
            ---------------

            error: {error}
            """
            print(error_msg)
            import pdb; pdb.set_trace() 
            raise e



        return cur.lastrowid

    def check_for_existing_record(self):
        sql = f'''
        SELECT Sender, text FROM sms
        WHERE SenderPhoneNumber = {self.sms.sender_phone}
        AND text = "{self.sms.text}"
        '''

        cur = self.conn.cursor()
        try:
            results = cur.execute(sql)
        except Exception as e:
            print(sql)
            raise e
        if len(results.fetchall()) > 0:
            return False
        else:
            return True
    def main(self):
        """
        method: inserts sms record if not duplicate
        """
        record_exists = self.check_for_existing_record()
        if record_exists:
            print(f"Record Already Exists: {self.sms.text }")
        else:
            self.insert_sms_record()
