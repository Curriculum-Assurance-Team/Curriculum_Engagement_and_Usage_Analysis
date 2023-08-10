import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Markdown

#
# 5. At some point in 2019, the ability for students and alumni to access both curriculums should have been shut off. Do you see any evidence of that happening?
# - Monthly average logs of data science and web dev students both declined greatly in the second half of 2019, indicating that this may be when this shutoff happened


# Run in final nb as:
# import explore_56 as e56
# e56.plot_monthly_avg_ds_logs()
# e56.plot_monthly_avg_wd_logs()

def plot_monthly_avg_ds_logs():
    
    plt.figure(figsize=(5, 3))

    ds_logs = df[df['program_id'] == 3]

    ds_monthly_avgs =  ds_logs.resample('M').size()

    sns.lineplot(ds_monthly_avgs)
    # Get the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]

    # Set the x-axis ticks using the tick positions and labels
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Data Science')

    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    plt.tight_layout()
    sns.despine()
    plt.show()
    
    
def plot_monthly_avg_wd_logs():
    plt.figure(figsize=(5, 3))

    wd_logs = df[df['program_id'] != 3]

    wd_monthly_avgs = wd_logs.resample('M').size()

    sns.lineplot(wd_monthly_avgs)
    # Get the x-axis tick positions and labels
    tick_positions = pd.date_range(start='2019-01-01', end='2020-07-01', freq='6M')
    tick_labels = [str(date.date())[:7] for date in tick_positions]

    # Set the x-axis ticks using the tick positions and labels
    plt.xticks(ticks=tick_positions, labels=tick_labels, rotation=30)

    plt.xlabel('Date')
    plt.ylabel('Average Logs')
    plt.title('Average Logs of Web Dev Students')

    plt.xlim(pd.Timestamp('2019-01-01'), pd.Timestamp('2020-07-01'))

    plt.tight_layout()
    sns.despine()
    plt.show()
