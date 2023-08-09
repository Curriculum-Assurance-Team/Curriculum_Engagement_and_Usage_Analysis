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




def load_data(file_path):
    # Load the data into a DataFrame
    df = pd.read_csv(file_path)
    return df

def most_traffic_lesson_per_program(df):
    # Group data by program and lesson, then count the access frequency
    program_most_traffic = df.groupby(['program', 'lesson']).size().reset_index(name='access_count')
    
    # Find the lesson with the highest access count per program
    most_traffic_per_program = program_most_traffic.groupby('program').apply(lambda x: x[x.access_count == x.access_count.max()])
    return most_traffic_per_program

def cohort_with_significantly_different_lesson(df):
    # Calculate the mean access count per lesson for each cohort
    cohort_lesson_mean = df.groupby(['cohort', 'lesson'])['access_count'].mean().reset_index()
    
    # Find cohorts with significantly different access counts for a lesson compared to other cohorts
    cohorts_with_difference = cohort_lesson_mean.groupby('lesson').apply(lambda x: x[x.access_count > x.access_count.mean() + x.access_count.std()])
    return cohorts_with_difference

def low_activity_students(df, threshold=5):
    # Find students with low activity based on the specified threshold
    low_activity_students = df[df.access_count < threshold]
    return low_activity_students

def identify_suspicious_activity(df):
    # Identify IP addresses with unusually high access counts
    suspicious_ips = df.groupby('ip').size().reset_index(name='access_count').sort_values('access_count', ascending=False)
    return suspicious_ips

def curriculum_access_changes(df, program_1, program_2):
    # Identify students who accessed both curriculums
    dual_access_students = df[(df.program == program_1) & (df.student_id.isin(df[df.program == program_2].student_id))]
    return dual_access_students

def frequently_referenced_topics(df, program):
    # Group data by program and lesson, then calculate mean access count
    program_lesson_mean = df[df.program == program].groupby('lesson')['access_count'].mean().reset_index()
    
    # Find lessons with above-average access counts
    frequent_lessons = program_lesson_mean[program_lesson_mean.access_count > program_lesson_mean.access_count.mean()]
    return frequent_lessons

def least_accessed_lessons(df):
    # Group data by lesson and calculate mean access count
    lesson_mean_access = df.groupby('lesson')['access_count'].mean().reset_index()
    
    # Find lessons with the lowest mean access counts
    least_accessed = lesson_mean_access.nsmallest(5, 'access_count')
    return least_accessed

# Load the data
data_file_path = "/Users/miattas/Downloads/anonymized-curriculum-access.csv"
data = load_data(data_file_path)

# Answer the questions
most_traffic = most_traffic_lesson_per_program(data)
significant_difference = cohort_with_significantly_different_lesson(data)
low_activity = low_activity_students(data)
suspicious_activity = identify_suspicious_activity(data)
dual_curriculum_access = curriculum_access_changes(data, 'web_dev', 'data_science')
frequent_topics = frequently_referenced_topics(data, 'web_dev')
least_accessed = least_accessed_lessons(data)

# Print or return the results as needed
print("Most Traffic Lesson per Program:\n", most_traffic)
print("\nCohorts with Significant Lesson Difference:\n", significant_difference)
print("\nLow Activity Students:\n", low_activity)
print("\nSuspicious Activity:\n", suspicious_activity)
print("\nStudents with Dual Curriculum Access:\n", dual_curriculum_access)
print("\nFrequently Referenced Topics:\n", frequent_topics)
print("\nLeast Accessed Lessons:\n", least_accessed)
