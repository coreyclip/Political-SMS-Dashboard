import pandas as pd
import sqlite3

def add_sqlite_date_filter(query, date, since_month=True, since_day=False):
    '''
    adds a date filter to a query against the sms database
    params:
     query: sqlite query
     date: expected format is %y-%B-%d 
    TODO function does not really work with string months need to
    add month in int format to get this to work
    '''
    date_parts = date.split('-')
    year = date_parts[0]
    month = date_parts[1]
    day = date_parts[2]

    if "WHERE" in query:
        date_filter = f"""
        AND year = {year}
        """
    else:
        date_filter = f"""
         WHERE year = {year}
        """
    
    if since_month:
        date_filter = date_filter + f' AND month_name = "{month}" '
    if since_day:
        date_filter = date_filter + f' AND day >= {day}'
    return query + date_filter



def fetch_data(author=None, source='sqlite', top=10,
               date_filter=dt.now().strftime('%Y-%B-%d'), sort_by_date=True, search_text=None):
    '''
    default source is sqlite else old csv file
    '''

    if source == 'sqlite':
        conn = sqlite3.connect('./etl/sms.db')
        if author is not None and author != 'Everyone':
            if search_text not in ['', 'None', None]:
                query = f'SELECT * FROM sms WHERE Sender = "{author}" AND text LIKE "%%{search_text}%%"'
            else:
                query = f'SELECT * FROM sms WHERE Sender = "{author}"'
        else:
            if search_text not in ['', 'None', None]:
                query = f'SELECT * FROM sms WHERE text LIKE "%%{search_text}%%"'
            else:
                query = "SELECT * FROM sms"
        print(f"executing query: {query}")
        df = pd.read_sql(query, conn)

    else:
        df = pd.read_csv('./application/data/ProcessedTexts.csv', index_col='ROWID',
                        usecols=['ROWID','SenderPhoneNumber', 'Sender', 'text', 'month_name',
                                 'day','year', 'polarity','subjectivity', 'negativity', 'neutrality',
                                 'positivity', 'compound', 'date', 'word_count', 'timestamp'
                                 ]
                        )
        if author != None:
            df = df[df['author'] == author]

    if sort_by_date is True:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp', ascending=False)
    if top == None:
        return df.to_dict(orient='records')
    else:
        return df.head(top).to_dict(orient='records')

def fetch_stats(author='Everyone'):
    conn = sqlite3.connect('./etl/sms.db')
    if author == 'Everyone':
        query = f'''
            select 
                Avg(polarity) AS AvgPolarity,
                Avg(subjectivity) AS AvgSubjectivity, 
                Avg(negativity) AS AvgNegativity, 
                Avg(neutrality) AS AvgNeutrality, 
                Avg(positivity) AS AvgPositivity, 
                Avg(compound) As AvgCompound
            from sms
            ;
        '''
    with conn 
