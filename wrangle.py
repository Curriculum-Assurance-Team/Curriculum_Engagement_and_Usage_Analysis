import pandas as pd
import env
import os


def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_log_data():
    '''
    If the csv file exists, it is read and returned as a pandas DataFrame
    If not, pandas reads in a SQL query that acquires log data from a MySQL database.
    The query is stored into a DataFrame, saved, and returned.
    '''
    filename = 'logs.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col='date', parse_dates=True)
    
    df = pd.read_sql("""SELECT l.date, l.time,
                                l.path as lesson,
                                l.user_id, c.name,
                                l.ip, c.start_date,
                                c.end_date, c.program_id
                        FROM logs l
                        JOIN cohorts c ON c.id=l.cohort_id;""",
                     get_connection('curriculum_logs'))
    # Assuming 'data' is your DataFrame with the provided data
    df['date'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    
    # Drop the 'time' column
    df = df.drop(['time'], axis=1)
    df = df.set_index('date')
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['access_day'] = df.index.day_name()
    df['access_month'] = df.index.month
    df['access_year'] = df.index.year
    
    df.to_csv(filename)
    
    return df


# # Upload with code
# import wrangle as w
# 
# df = w.get_log_data()
