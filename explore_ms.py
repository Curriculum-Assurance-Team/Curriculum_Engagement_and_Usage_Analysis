import pandas as pd
import os
import urllib.parse

#POssible Project Functions

# Import Libraries
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import chi2_contingency
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from IPython.display import display, display_html
from sklearn.dummy import DummyClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import IsolationForest
import env
from sqlalchemy import create_engine


def get_connection(db_name=env.db_name, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

def get_sql_data():
    '''
    If the CSV file exists, it is read and returned as a pandas DataFrame.
    If not, pandas reads in a SQL query that acquires log data from a MySQL database.
    The query is stored into a DataFrame, saved, and returned.
    '''
    filename = 'curriculum_logs.csv'
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        # Define SQL query, database parameters, and filename
        sql_query = """
            SELECT l.date, l.time, l.path as lesson, l.user_id, c.name as cohort, c.program_id,
                   l.ip, c.start_date, c.end_date
            FROM logs l
            JOIN cohorts c ON c.id=l.cohort_id;
        """
        db_name = 'curriculum_logs'
        user = env.user  # Replace with the actual value
        host = env.host # Replace with the actual value
        password = env.password  # Replace with the actual value
        
        # Create a database connection using SQLAlchemy
        connection_string = get_connection(db_name, user, host, password)
        engine = create_engine(connection_string)
        
        # Fetch data from the database and convert it into a DataFrame
        logs_df = pd.read_sql(sql_query, get_connection('curriculum_logs'))
        
        # Convert 'date' and 'time' columns to a single 'datetime' column
        logs_df['date'] = pd.to_datetime(logs_df['date'] + ' ' + logs_df['time'])
        logs_df = logs_df.drop(['time'], axis=1)  # Drop 'time' column
        logs_df = logs_df.set_index('date')
        
        # Replace program_id numbers with program names using the replace method
        program_mapping = {1: 'web dev', 2: 'web dev', 3: 'data science', 4: 'frontend'}
        logs_df['program'] = logs_df['program_id'].replace(program_mapping)
        
        # Save the DataFrame as a CSV file
        logs_df.to_csv(filename, index=False)
        return logs_df


def remove_outliers(data, column_name):
    '''Remove outliers using IQR method for a specified column'''
    Q1 = data[column_name].quantile(0.25)
    Q3 = data[column_name].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column_name] >= lower_bound) & (data[column_name] <= upper_bound)]

    
# Define a function to get top lessons by program across cohorts
def get_top_lessons_by_program(logs_df, program):
    grouped_traffic = logs_df.groupby(['program', 'lesson', 'cohort']) \
                        .size().reset_index(name='count')
    top_lessons = grouped_traffic.sort_values('count', ascending=False)
    
    # Filter for the specified program and remove unwanted lessons
    program_top_lessons = top_lessons[
        (top_lessons['program'] == program) &
        (~top_lessons['lesson'].isin(['/', 'appendix', 'index.html']))
    ]
    
    # Get the top lesson across cohorts for the program
    top_lesson_across_cohorts = program_top_lessons.groupby('lesson')['count'].size().idxmax()
    
    return program_top_lessons.head(10), top_lesson_across_cohorts



# def get_least_accessed_lessons(logs_df, program):
#     # Group data and get counts
#     grouped_traffic = logs_df.groupby(['program', 'lesson', 'cohort']) \
#                         .size().reset_index(name='count')
    
#     # Removing outliers from the count column
#     filtered_traffic = remove_outliers(grouped_traffic, 'count')
    
#     # Sort by count to get least accessed lessons
#     least_accessed_lessons = filtered_traffic.sort_values('count', ascending=True)
    
#     # Filter for the specified program and remove unwanted lessons
#     program_least_accessed_lessons = least_accessed_lessons[
#         (least_accessed_lessons['program'] == program) &
#         (~least_accessed_lessons['lesson'].isin(['/', 'appendix', 'index.html']))
#     ]
    
#     # Get the least accessed lesson across cohorts for the program
#     least_accessed_lesson_across_cohorts = program_least_accessed_lessons.groupby('lesson')['count'].idxmin()
    
#     return program_least_accessed_lessons.head(10), least_accessed_lesson_across_cohorts

def get_least_accessed_lessons_with_anomaly_detection(logs_df, program):
    # Group and count the lesson accesses
    grouped_traffic = logs_df.groupby(['program', 'lesson', 'cohort']) \
                        .size().reset_index(name='count')
    print(f"Initial grouped count: {len(grouped_traffic)}")
    
    # Use Isolation Forest for anomaly detection
    model = IsolationForest(contamination=0.05)
    grouped_traffic['anomaly_score'] = model.fit_predict(grouped_traffic[['count']])
    
    print(f"Anomalies Detected: {sum(grouped_traffic['anomaly_score'] == -1)}")
    print(f"Non-Anomalies Detected: {sum(grouped_traffic['anomaly_score'] == 1)}")
    
    # Remove anomalies and keep only normal data
    filtered_traffic = grouped_traffic[grouped_traffic['anomaly_score'] == 1]
    print(f"Filtered traffic after removing anomalies: {len(filtered_traffic)}")
    
    # Filter for the specified program
    program_traffic = filtered_traffic[filtered_traffic['program'] == program]
    print(f"Program traffic for '{program}': {len(program_traffic)}")
    
    # Remove unwanted lessons
    unwanted_lessons = ['/', 'appendix', 'index.html']
    program_filtered_lessons = program_traffic[~program_traffic['lesson'].isin(unwanted_lessons)]
    print(f"Lessons after removing unwanted ones: {len(program_filtered_lessons)}")
    
    if program_filtered_lessons.empty:
        return None
    
    # Get the least accessed lesson across cohorts for the program
    min_access_count = program_filtered_lessons['count'].min()
    least_accessed_lessons = program_filtered_lessons[program_filtered_lessons['count'] == min_access_count]
    
    least_accessed_lesson_names = least_accessed_lessons['lesson'].head(10).tolist()
    return least_accessed_lesson_names