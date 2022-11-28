from sklearn import preprocessing
from random import randint
import pandas as pd
import numpy as np
import uuid


def create_hourly_rate(category):
    payRange = {'Advocate': (15, 30),
                'Arts': (12, 30),
                'Automation Testing': (15, 40),
                'Blockchain': (25, 80),
                'Business Analyst': (15, 50),
                'Civil Engineer': (20, 45),
                'Data Science': (25, 70),
                'Database': (20, 50),
                'DevOps Engineer': (25, 45),
                'DotNet Developer': (22, 60),
                'ETL Developer': (20, 80),
                'Electrical Engineering': (18, 45),
                'HR': (12, 40),
                'Hadoop': (25, 80),
                'Health and fitness': (19, 30),
                'Java Developer': (20, 50),
                'Mechanical Engineer': (18, 50),
                'Network Security Engineer': (23, 60),
                'Operations Manager': (25, 55),
                'PMO': (35, 70),
                'Python Developer': (25, 80),
                'SAP Developer': (23, 50),
                'Sales': (20, 40),
                'Testing': (25, 50),
                'Web Designing': (30, 55)}
    range = payRange[category]
    return randint(range[0], range[1])


def generate_dataset(df):
    label_encoder = preprocessing.LabelEncoder()
    df['Applicant_ID'] = df.Category.apply(lambda x: str(uuid.uuid4())[-5:])
    df['Category_Labeled'] = label_encoder.fit_transform(df['Category'])
    df['Hourly_Rate'] = df.Category.apply(create_hourly_rate)
    df['Notice_Period'] = df.Category.apply(lambda x: randint(0, 4))
    # on-site-0 remote-1 hybrid-2
    df['Operation_Mode'] = df.Category.apply(lambda x: randint(0, 2))
    df_count = df.groupby('Category').size().reset_index(name='Count')
    df_count['Good'] = (df_count.Count * 0.2).apply(np.ceil)
    df_count['Avg'] = (df_count.Count * 0.4).apply(np.ceil)
    df_count['Low'] = (df_count.Count * 0.4).apply(np.ceil)
    # adjusting scores
    df['Test_Score'] = 0
    df['Interview_Score'] = 0
    df['Hired'] = 0

    for i, outter_row in df_count.iterrows():
        hired_staff = int(outter_row[1] * 0.3)
        for j, inner_row in df.iterrows():
            if (outter_row[0] == inner_row[0]):
                if (outter_row[2] >= 0):
                    df.loc[j, 'Test_Score'] = randint(71, 100)
                    df.loc[j, 'Interview_Score'] = randint(8, 10)
                    outter_row[2] -= 1
                elif (outter_row[3] >= 0):
                    df.loc[j, 'Test_Score'] = randint(51, 70)
                    df.loc[j, 'Interview_Score'] = randint(6, 7)
                    outter_row[3] -= 1
                else:
                    df.loc[j, 'Test_Score'] = randint(20, 50)
                    df.loc[j, 'Interview_Score'] = randint(2, 5)
                    outter_row[4] -= 1
                if (hired_staff >= 0):
                    df.loc[j, 'Hired'] = 1
                    hired_staff -= 1

    return df
