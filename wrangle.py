import pandas as pd
import env
import os


def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
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
        db = 'curriculum_logs'
        user = env.user  # Replace with the actual value
        hostname = env.hostname  # Replace with the actual value
        password = env.password  # Replace with the actual value
        # Create a database connection using SQLAlchemy
        connection_string = get_connection(db, user, hostname, password)
        engine = create_engine(connection_string)
        # Fetch data from the database and convert it into a DataFrame
        logs_df = pd.read_sql(sql_query, get_connection('curriculum_logs'))
        # Convert 'date' and 'time' columns to a single 'datetime' column
        logs_df['date'] = pd.to_datetime(logs_df['date'] + ' ' + logs_df['time'])
        logs_df = logs_df.drop(['time'], axis=1)  # Drop 'time' column
        logs_df = logs_df.set_index('date')
        # Save the DataFrame as a CSV file
        logs_df.to_csv(filename, index=False)
        return logs_df

# # Upload with code
# import wrangle as w
# 
# df = w.get_log_data()






#######################################
# Questions 5 and 6

# Markdown

#
# 5. At some point in 2019, the ability for students and alumni to access both curriculums should have been shut off. Do you see any evidence of that happening?
# - Monthly average logs of data science and web dev students both declined greatly in the second half of 2019, indicating that this may be when this shutoff happened

#
# 6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
# - Data Science: SQL, Classification, Anomaly Detection
# - Web Dev: Spirng, HTML/CSS, Java

def plot_monthly_avg_ds_logs():
    """
    Plots the average monthly logs for Data Science students.
    """
    # Create a new figure
    plt.figure(figsize=(5, 3))

    # Filter logs for Data Science program (program_id == 3)
    ds_logs = df[df['program_id'] == 3]

    # Resample logs to calculate average monthly logs
    ds_monthly_avgs =  ds_logs.resample('M').size()

    # Create a line plot using Seaborn
    sns.lineplot(ds_monthly_avgs)

    # Set the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    # Set plot labels and title
    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Data Science')

    # Set x-axis limits
    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()
    
def plot_monthly_avg_wd_logs():
    """
    Plots the average monthly logs for Web Development students.
    """
    # Create a new figure
    plt.figure(figsize=(5, 3))

    # Filter logs for Web Development program (program_id != 3)
    wd_logs = df[df['program_id'] != 3]

    # Resample logs to calculate average monthly logs
    wd_monthly_avgs = wd_logs.resample('M').size()

    # Create a line plot using Seaborn
    sns.lineplot(wd_monthly_avgs)

    # Set the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    # Set plot labels and title
    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Web Dev Students')

    # Set x-axis limits
    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()


def plot_top_ds_alumni_lessons():
    """
    Plots the top logged lessons for Data Science alumni.
    """
    # Filter logs for Data Science alumni
    ds_alumni_logs = df[(df['program_id'] == 3) &
                        (df.index > df['end_date']) &
                        (df['name'] != 'Staff')]
    
    # Create a bar plot using Seaborn
    plt.figure(figsize=(7, 5))
    sns.barplot(x=ds_alumni_logs['lesson'].value_counts()[2:7].index,
                y=ds_alumni_logs['lesson'].value_counts()[2:7].values,
                color="#D16002")

    # Set plot labels and title
    plt.xlabel('Lessons')
    plt.ylabel('Counts')
    plt.title('Top Logged Lessons for Data Science Alumni')

    plt.xticks(rotation=15, ha='right')

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()
    
    
def plot_top_wb_alumni_lessons():
    """
    Plots the top logged lessons for Web Development alumni.
    """
    # Filter logs for Web Development alumni
    wb_alumni_logs = df[(df['program_id'] != 3) &
                        (df.index > df['end_date']) &
                        (df['name'] != 'Staff')]
    
    # Extract and preprocess the value counts
    value_counts_result = wb_alumni_logs['lesson'].value_counts()[2:8]
    value_counts_result = value_counts_result.drop(value_counts_result.index[2])
    
    # Create a bar plot using Seaborn
    plt.figure(figsize=(7, 5))
    sns.barplot(x=value_counts_result.index, y=value_counts_result.values,
                color="#D16002")

    # Set plot labels and title
    plt.xlabel('Lessons')
    plt.ylabel('Counts')
    plt.title('Top Logged Lessons for Web Dev Alumni')

    # Adjust layout and display plot
    plt.tight_layout()
    sns.despine()
    plt.show()

# Questions 5 and 6
#######################################
