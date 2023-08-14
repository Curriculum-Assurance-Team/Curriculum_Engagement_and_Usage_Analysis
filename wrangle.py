# Transform Libraries
import pandas as pd
import numpy as np
import os

#CAT Team Libraries
# import wrangle as w
import env

# Visualization Libraries
import urllib.parse
import gzip
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

# Misc.  Libraries 
from sqlalchemy import create_engine
from io import BytesIO
from io import StringIO
from tabulate import tabulate
import warnings


def get_connection(db, user, hostname, password):
    return f'mysql+pymysql://{user}:{password}@{hostname}/{db}'

def get_logs_data():
    '''Acquire the Curriculum logs from the CodeUp database and preprocess the data.'''
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
        db = 'curriculum_logs'
        user = env.user  # Replace with the actual value
        hostname = env.hostname  # Replace with the actual value
        password = env.password  # Replace with the actual value
        
        # Create a database connection using SQLAlchemy
        connection_string = get_connection(db, user, hostname, password)
        engine = create_engine(connection_string)
        
        # Fetch data from the database and convert it into a DataFrame
        logs_df = pd.read_sql(sql_query, connection_string)
        
        # Convert 'date' and 'time' columns to a single 'datetime' column
        logs_df['date'] = pd.to_datetime(logs_df['date'] + ' ' + logs_df['time'])
        logs_df = logs_df.drop(['time'], axis=1)  # Drop 'time' column
        logs_df = logs_df.set_index('date')
        
        # Additional preprocessing steps
        logs_df['access_day'] = logs_df.index.day_name()
        logs_df['access_month'] = logs_df.index.month
        logs_df['access_year'] = logs_df.index.year
        program_mapping = {1: 'web dev', 2: 'web dev', 3: 'data science', 4: 'frontend'}
        logs_df['program'] = logs_df['program_id'].replace(program_mapping)
        
        # Save the DataFrame as a CSV file
        logs_df.to_csv(filename, index=False)
    
    return logs_df


#######################################
# Questions 1

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
 

#######################################
# Questions 2


def question2_graph(logs_df):
    '''This function groups data by cohort and lesson to determine the lesson with the highest and lowest counts by cohort'''
    # Group data by cohort and lesson, then calculate the size (count of occurrences)
    cohort2 = logs_df.groupby(['cohort', 'lesson']).size()
    # Reset the index and rename the count column
    cohort2 = cohort2.reset_index(name='count')
    # Filter the DataFrame to show only the rows where lesson is '/' and  count in descending order
    cohort2 = cohort2.loc[cohort2['lesson'] == '/'].sort_values(by='count', ascending=False)
    # Plotting
    plt.figure(figsize=(12, 6))
    sns.barplot(data=cohort2, x='cohort', y='count', palette='Oranges')
    plt.xlabel('Cohort')
    plt.ylabel('Lesson / Count')
    plt.title('Lesson with Highest Count by Cohort')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
def question2_2(logs_df):
    '''This function groups data by cohort and lesson to determine the lesson with the highest and lowest counts by cohort'''
    # Group data by cohort and lesson, then calculate the size (count of occurrences)
    cohort2 = logs_df.groupby(['cohort', 'lesson']).size()
    # Reset the index and rename the count column
    cohort2 = cohort2.reset_index(name='count')
    # Filter the DataFrame to show only the rows where lesson is '/' and  count in descending order
    cohort2 = cohort2.loc[cohort2['lesson'] == '/'].sort_values(by='count', ascending=False)
    return cohort2.head(), cohort2.tail()

def question2_1(logs_df):
    '''This function determines which lesson was most and least refered to by cohort'''
    #Find lesson counts"
    lesson_counts = logs_df.groupby('lesson')[['cohort', 'start_date','user_id']].nunique()
    lesson_counts = lesson_counts.sort_values(by='cohort', ascending=False)
    # Find the lesson that was refered to the most 
    most_referred_cohort = lesson_counts['cohort'].idxmax()
    most_referred_count = lesson_counts.loc[most_referred_cohort, 'cohort']
    
    # Find the lesson that referred to the the least
    least_referred_cohort = lesson_counts['cohort'].idxmin()
    least_referred_count = lesson_counts.loc[least_referred_cohort, 'cohort']
    
    print(f"The lesson that was referred to the the most: {most_referred_cohort} with {most_referred_count} referrals.")
    print(f"The lesson that referred to the the least: {least_referred_cohort} with {least_referred_count} referrals.")





#######################################
# Questions 3

def question3_list_graph(logs_df):
    '''This graph finds user error and creates a threshold of 3 so any user with less than 3 will be filtered for low engagement'''
    # Calculate engagement for each user by counting unique lessons
    user_engagement = logs_df.groupby('user_id')['lesson'].nunique()
    
    # Set a threshold for low engagement (e.g., fewer than 3 unique lessons)
    threshold = 3
    
    # Filter for students with low engagement
    low_engagement_students = user_engagement[user_engagement < threshold]
    
    # Create a bar plot with h-line with threshold
    plt.figure(figsize=(10, 6))
    le = plt.hist(user_engagement, bins=20, color='orange', edgecolor='black', alpha=0.7, label='Engagement Distribution')
    plt.axhline(y=threshold, color='red', linestyle='dashed', linewidth=2, label='Threshold')
    plt.scatter(low_engagement_students.index, [0] * len(low_engagement_students), color='red', label='Low Engagement Students')
    plt.xlabel('Number of Unique Lessons')
    plt.ylabel('Number of Students')
    plt.title('Anomaly Detection: Engagement Distribution and Low Engagement Students')
    plt.legend()
    
    # Add count numbers on bars (same as before)
    for p in le[2]:
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        offset = width * 0.02
        plt.annotate(format(height, '.0f'), (x + width / 2., y + height), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    
    plt.tight_layout()
    plt.show()

    # List all low engagement students by unique 'user_id' using tabulate
    low_engagement_students_list = low_engagement_students.index.tolist()
    
    # Calculate the count of times '/' was accessed for each low engagement student
    les_curriculum_access_count = logs_df[logs_df['user_id'].isin(low_engagement_students_list) & (logs_df['lesson'] == '/')].groupby('user_id').size().reset_index(name='curriculum access ct')
    
    # Merge with the main DataFrame to add cohort information
    low_engagement_students_info = pd.merge(les_curriculum_access_count, logs_df[['user_id', 'cohort']], on='user_id', how='left')
    
    # Sort the table by 'curriculum access ct' in ascending order
    low_engagement_students_info = low_engagement_students_info.sort_values(by='curriculum access ct', ascending=True)
    
    # Print the head of the sorted information using tabulate
    print("Low Engagement Students List:")
    print(tabulate(low_engagement_students_info.head(), headers='keys', tablefmt='grid'))
    


#######################################
# Questions 4

# 4. Are there any suspicious IP addresses?


def explore_ip_addresses(logs_df):
    logs_df['ip_network_portion'] = logs_df['ip'].str.split('.').str[0]
    
    result1 = logs_df['ip_network_portion'].value_counts().head(10).to_frame().reset_index()
    result1.rename(columns={'index': 'ip_network_portion',
                            'ip_network_portion': 'log_count'}, inplace=True)
    print('Most Common IP addresses (network portion)')
    display(result1, '\n')    
    
    result2 = logs_df['ip_network_portion'].value_counts().tail(10).to_frame().reset_index()
    result2.rename(columns={'index': 'ip_network_portion',
                            'ip_network_portion': 'log_count'}, inplace=True)
    print('Least Common IP addresses (network portion)')
    display(result2)


#######################################
# Questions 5 


# 5. At some point in 2019, the ability for students and alumni to access both curriculums should have been shut off. Do you see any evidence of that happening?
# - Monthly average logs of data science and web dev students both declined greatly in the second half of 2019, indicating that this may be when this shutoff happened

def plot_monthly_avg_ds_logs(logs_df):
    """
    Plots the average monthly logs for Data Science students.
    """
    # Create a new figure
    plt.figure(figsize=(5, 3))

    # Filter logs for Data Science program (program_id == 3)
    ds_logs = logs_df[logs_df['program'] == 'data science']

    # Resample logs to calculate average monthly logs
    ds_monthly_avgs =  ds_logs.resample('M').size()

    # Create a line plot using Seaborn
    sns.lineplot(ds_monthly_avgs, color = '#D16002')

    # Set the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    # Set plot labels and title
    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Data Science Students')

    # Set x-axis limits
    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()
    
def plot_monthly_avg_wd_logs(logs_df):
    """
    Plots the average monthly logs for Web Development students.
    """
    # Create a new figure
    plt.figure(figsize=(5, 3))

    # Filter logs for Web Development program (program_id != 3)
    wd_logs = logs_df[logs_df['program'] != 'data science']

    # Resample logs to calculate average monthly logs
    wd_monthly_avgs = wd_logs.resample('M').size()

    # Create a line plot using Seaborn
    sns.lineplot(wd_monthly_avgs, color = '#D16002')

    # Set the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    # Set plot labels and title
    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Web Development Students')

    # Set x-axis limits
    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()

    
#### Question 6
#
# 6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
# - Data Science: SQL, Classification, Anomaly Detection
# - Web Dev: Spirng, HTML/CSS, Java


def plot_top_ds_alumni_lessons(logs_df):
    """
    Plots the top logged lessons for Data Science alumni.
    """
    logs_df['end_date'] = pd.to_datetime(logs_df['end_date'])
    
    # Filter logs for Data Science alumni
    ds_alumni_logs = logs_df[(logs_df['program'] == 'data science') &
                             (logs_df.index > logs_df['end_date']) &
                             (logs_df['cohort'] != 'Staff')]
    
    # Create a bar plot using Seaborn
    plt.figure(figsize=(7, 5))
    ds = sns.barplot(x=ds_alumni_logs['lesson'].value_counts()[2:7].index,
                     y=ds_alumni_logs['lesson'].value_counts()[2:7].values,
                     color="#D16002")

    # Set plot labels and title
    plt.xlabel('Lessons')
    plt.ylabel('Counts')
    plt.title('Top Logged Lessons for Data Science Alumni')
    
    for p in ds.patches:  # Use ds.patches to access individual bars
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        offset = width * 0.02
        plt.annotate(format(height, '.0f'), (x + width / 2., y + height), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    
    plt.xticks(rotation=45, ha='right')

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()

    
    
def plot_top_wb_alumni_lessons(logs_df):
    """
    Plots the top logged lessons for Web Development alumni.
    """
    logs_df['end_date'] = pd.to_datetime(logs_df['end_date'])
    # Filter logs for Web Development alumni
    wb_alumni_logs = logs_df[(logs_df['program'] != 'data science') &
                             (logs_df.index > logs_df['end_date']) &
                             (logs_df['cohort'] != 'Staff')]
    
    # Extract and preprocess the value counts
    value_counts_result = wb_alumni_logs['lesson'].value_counts()[2:8]
    value_counts_result = value_counts_result.drop(value_counts_result.index[2])
    
    # Create a bar plot using Seaborn
    plt.figure(figsize=(7, 5))
    wb = sns.barplot(x=value_counts_result.index, y=value_counts_result.values,
                     color="#D16002")

    # Set plot labels and title
    plt.xlabel('Lessons')
    plt.ylabel('Counts')
    plt.title('Top Logged Lessons for Web Development Alumni')

    for p in wb.patches:  # Use wb.patches to access individual bars
        width = p.get_width()
        height = p.get_height()
        x, y = p.get_xy()
        offset = width * 0.02
        plt.annotate(format(height, '.0f'), (x + width / 2., y + height), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
    
    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()

#######################################
# Questions 1

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
#######################################
# Questions 7
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

