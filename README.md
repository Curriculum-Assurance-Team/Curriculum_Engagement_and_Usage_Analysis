# Curriculum Engagement and Usage Analysis
- Team: Annie Carter, Miatta Sinayoko, and Martin Reyes
- Sourced by CodeUp, LLC

![image](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgG55eAx6SYJA0sh2VfEBE60TYLs6K_hKcVQjL-0J8rEDVmMkcTCRLf8C4Je3Gd5xCWi0&usqp=CAU)

## **Project Description:**
In preparation for the upcoming board meeting on Thursday afternoon, we are conducting an analysis of our educational curriculum's usage patterns and identifying any potential anomalies or concerns. The purpose of this project is to provide insights into the engagement levels of different cohorts with our curriculum, detect any suspicious activities, and uncover trends related to post-graduation knowledge retention. By addressing the specific questions provided, we aim to equip you with comprehensive information to discuss and make informed decisions during the board meeting.

## **Project Goals:**
The primary objectives are:
1. Analyze lesson popularity across programs, cohort engagement differences, and low engagement student profiles to enhance curriculum effectiveness.
2. Investigate anomalies, security breaches, and cross-curriculum access, while assessing post-graduation knowledge impact.
3. Uncover insights from underutilized lessons and unexpected trends, providing comprehensive data for informed decision-making.

## **Initial Questions**
1. Identify the lesson that consistently garners the highest traffic across cohorts within each program?
2. Is there a particular cohort that has demonstrated significantly higher engagement with a specific lesson than other cohorts, warranting further investigation?
3. Identify instances of active students who exhibit minimal interaction with the curriculum? If so,provide insights into these students' behavior and engagement patterns?
4. Detect any potentially unauthorized access or suspicious activities, including unusual access patterns or indications of web scraping? Are there any indications of suspicious IP addresses?
5. Has the access for students and alumni to both curriculums (web development to data science, data science to web development) been disabled as intended at some point in 2019? Confirm if this change was implemented and if so, when?
6. Outline the topics that graduates continue to reference beyond their graduation and into their professional roles for both programs?
7. Which lessons have recorded the lowest levels of access?
8. Is there any additional information or insights that you believe would be pertinent for me to be aware of?

## **Data Dictionary**
The data was acquired from CodeUP, LLC's 'curricular_logs' dataset, initially containing 847,330 rows and 7 columns. The team distributed tasks to effectively utilize and manipulate the original dataframe in order to address the specified questions.

|    Original Column Name     |   Target    |       Data Type          |       Definition              |
|-----------------------------|-------------|--------------------------|------------------------------ |
|        Various              |  Various    |      Various             | Target dependent on Question  |
                                               


|    Original Columns Name    |   Feature    |       Data Type         |     Definition                |
|-----------------------------|--------------|------------------------ |------------------------------ |
|date                         |date          | 847330 non-null Datetime| Date of access                |
|time                         |time          | 847330 non-null  object | Time                          |
|l.path                       |lesson        | 847330 non-null  object | Lesson path                   | 
|user_ID                      |user_ID       | 847330 non-null  int64  | user identification           |    
|c.name                       |cohort        | 847330 non-null  object |Cohort name (e.g. Darden)/Staff|
|program_ID                   |program       | 847330 non-null  int64  |Program name(e.g. Data Science)|
|ip                           |ip            | 847330 non-null  object | Used for feature engineering  |
|start_date                   |start_date    | 847330 non-null  object | Program Start Date            |
|end_date                     |end_date      | 847330 non-null  object | Graduation Date               |


## **Instructions to Reproduce the Final Project Notebook**
To successfully run/reproduce the final project notebook, please follow these steps:

- Read this README.md document to familiarize yourself with the project details and key findings.
- Before proceeding, ensure that you have the necessary database credentials. Get data set from csv  Create .gitignore for privacy if necessary
- Clone the classification_project repository from my GitHub or download the following files: wrange.py and final_report.ipynb. -  - You can find these files in the project repository.
- Open the final_report.ipynb notebook in your preferred Jupyter Notebook environment or any compatible Python environment.
- Ensure that all necessary libraries or dependent programs are installed (e.g IO String). You may need to install additional packages if they are not already present in your environment.
- Run the final_report.ipynb notebook to execute the project code and generate the results. By following these instructions, you will be able to reproduce the analysis and review the project's final report. Feel free to explore the code, visualizations, and conclusions presented in the notebook.

**Approach:**
To achieve these goals, we will conduct a comprehensive analysis of our curriculum data, including user engagement logs, access timestamps, IP addresses, and cohort information. We will utilize data analysis techniques, such as data visualization, statistical analysis, and anomaly detection, to answer the specified questions and identify any patterns or anomalies. The results will be presented in a clear and concise manner, with visualizations and explanations to facilitate understanding.


## **Key Findings**
- **Anomaly Detection and Engagement Analysis:**
  - Anomalies were uncovered by contrasting engagement levels with the '/' lesson, revealing unexpected cohort-specific trends.
  - The 'Darden' cohort exhibited remarkable engagement with the '/' lesson, indicating a potential anomaly that necessitates in-depth exploration.
  - Further qualitative research is recommended to delve into factors such as curriculum content, teaching methodologies, and cohort dynamics to uncover the root causes behind these anomalies.

- **Low Engagement Student Profiles:**
  - Analysis identified students with minimal curriculum interaction, engaging with fewer than three unique lessons.
  - These low engagement profiles indicate potential learning challenges or missed opportunities.
  - Limited lesson diversity was noted among the Low Engagement Students List, particularly in interactions with the curriculum 
  '/'.
- **Monthly Average Logs Analysis:**
  - The data science and web development programs experienced a substantial decline in monthly average logs during the latter half of 2019.
- **Decline in Data Science and Web Development Engagement:**
  - Specific topics such as SQL, Classification, Anomaly Detection for Data Science and Spring, HTML/CSS, Java for Web Development exhibited decreased engagement.

These findings collectively underscore the importance of ongoing monitoring, proactive interventions, and continuous curriculum refinement to ensure optimal learning experiences and outcomes for students across diverse cohorts and programs.


## **Conclusion**
The comprehensive analysis conducted to assess lesson popularity across programs, cohort engagement differences, and low engagement student profiles has provided valuable insights into curriculum effectiveness. The methodology employed in this study successfully identified anomalies and trends that warrant further investigation, enhancing our understanding of student behavior and curriculum utilization. The observations made concerning engagement discrepancies within specific cohorts and the prevalence of low engagement students offer crucial avenues for targeted interventions and improvements. The integration of both quantitative and qualitative approaches has furnished a holistic perspective, enabling informed decision-making for curriculum enhancement.
'/'.


## **Recommendations**
  - Further qualitative research is recommended to delve into factors such as curriculum content, teaching methodologies, and cohort dynamics to uncover the root causes behind these anomalies.

  - Detecting low engagement early can facilitate timely support and tailored interventions to improve student outcomes.
  - To enhance engagement and promote effective learning, proactive measures like personalized assistance and supplementary resources should be considered for students displaying minimal curriculum interaction
  

## **Client Deliverables**
The outcome of this project will be a detailed in an report addressing each of the provided questions, along with any additional insights we uncover during our analysis. The report will provide you with the necessary information to discuss curriculum engagement, anomalies, and post-graduation trends during the upcoming board meeting, enabling informed decision-making and strategic planning. Please feel free to provide any additional guidance or clarification, and we will ensure that our analysis aligns with your expectations and needs.




