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
import env
from sqlalchemy import create_engine


# def get_connection(db_name):
#     '''
#     This function uses my info from my env file to
#     create a connection URL to access the Codeup db.
#     '''
#     return f'mysql+pymysql://{user}:{password}@{host}/{db_name}'

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


# Define a function to get top lessons by program_id
def get_top_lessons_by_program(logs_df, program):
    grouped_traffic = logs_df.groupby(['program', 'lesson', 'cohort']) \
                        .size().reset_index(name='count')
    top_lessons = grouped_traffic.sort_values('count', ascending=False)
    
    return top_lessons[
        (top_lessons['program'] == program) &
        (~top_lessons['lesson'].isin(['/', 'appendix', 'index.html']))].head(10)







# def load_data(file_path):
#     # Load the data into a DataFrame
#     df = pd.read_csv(file_path)
#     return df

# def most_traffic_lesson_per_program(df):
#     # Group data by program and lesson, then count the access frequency
#     program_most_traffic = df.groupby(['program', 'lesson']).size().reset_index(name='access_count')
    
#     # Find the lesson with the highest access count per program
#     most_traffic_per_program = program_most_traffic.groupby('program').apply(lambda x: x[x.access_count == x.access_count.max()])
#     return most_traffic_per_program

# def cohort_with_significantly_different_lesson(df):
#     # Calculate the mean access count per lesson for each cohort
#     cohort_lesson_mean = df.groupby(['cohort', 'lesson'])['access_count'].mean().reset_index()
    
#     # Find cohorts with significantly different access counts for a lesson compared to other cohorts
#     cohorts_with_difference = cohort_lesson_mean.groupby('lesson').apply(lambda x: x[x.access_count > x.access_count.mean() + x.access_count.std()])
#     return cohorts_with_difference

# def low_activity_students(df, threshold=5):
#     # Find students with low activity based on the specified threshold
#     low_activity_students = df[df.access_count < threshold]
#     return low_activity_students

# def identify_suspicious_activity(df):
#     # Identify IP addresses with unusually high access counts
#     suspicious_ips = df.groupby('ip').size().reset_index(name='access_count').sort_values('access_count', ascending=False)
#     return suspicious_ips

# def curriculum_access_changes(df, program_1, program_2):
#     # Identify students who accessed both curriculums
#     dual_access_students = df[(df.program == program_1) & (df.student_id.isin(df[df.program == program_2].student_id))]
#     return dual_access_students

# def frequently_referenced_topics(df, program):
#     # Group data by program and lesson, then calculate mean access count
#     program_lesson_mean = df[df.program == program].groupby('lesson')['access_count'].mean().reset_index()
    
#     # Find lessons with above-average access counts
#     frequent_lessons = program_lesson_mean[program_lesson_mean.access_count > program_lesson_mean.access_count.mean()]
#     return frequent_lessons

# def least_accessed_lessons(df):
#     # Group data by lesson and calculate mean access count
#     lesson_mean_access = df.groupby('lesson')['access_count'].mean().reset_index()
    
#     # Find lessons with the lowest mean access counts
#     least_accessed = lesson_mean_access.nsmallest(5, 'access_count')
#     return least_accessed

# # Load the data
# data_file_path = "/Users/miattas/Downloads/anonymized-curriculum-access.csv"
# data = load_data(data_file_path)

# # Answer the questions
# most_traffic = most_traffic_lesson_per_program(data)
# significant_difference = cohort_with_significantly_different_lesson(data)
# low_activity = low_activity_students(data)
# suspicious_activity = identify_suspicious_activity(data)
# dual_curriculum_access = curriculum_access_changes(data, 'web_dev', 'data_science')
# frequent_topics = frequently_referenced_topics(data, 'web_dev')
# least_accessed = least_accessed_lessons(data)

# # Print or return the results as needed
# print("Most Traffic Lesson per Program:\n", most_traffic)
# print("\nCohorts with Significant Lesson Difference:\n", significant_difference)
# print("\nLow Activity Students:\n", low_activity)
# print("\nSuspicious Activity:\n", suspicious_activity)
# print("\nStudents with Dual Curriculum Access:\n", dual_curriculum_access)
# print("\nFrequently Referenced Topics:\n", frequent_topics)
# print("\nLeast Accessed Lessons:\n", least_accessed)
