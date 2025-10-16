import gc
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
from utils.create_layouts import *

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE_HIDDEN = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "transition": "all 0.3s"
}

DESCRIPTION_SVM = '''
The core of the project involves a machine learning pipeline that processes raw user data to generate a prediction. This process includes:

- Data Preparation: User preferences are transformed into a numerical format using MultiLabelBinarizer, which converts a list of strings (genres, themes) into a one-hot encoded matrix. This matrix represents the presence or absence of a given preference, allowing the model to interpret the data effectively.

- Model Training: The SVM model is trained on a pre-existing dataset that associates deities with various musical and cinematic tastes. The pipeline also incorporates a data scaler to ensure optimal performance, as SVM models are sensitive to the scale of input features.

- Prediction and Recommendation: When a new user's preferences are submitted, the trained model generates a prediction. The system calculates a decision function score for each potential deity. This score represents the model's confidence in the prediction. The application then uses these scores to recommend the most likely deity to the user, providing a more engaging result.
'''

MODEL = joblib.load('assets/datasets/svm_model_gods.pkl')
MLB = joblib.load('assets/datasets/mlb_gods.pkl')

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
df_me = pd.read_csv("assets/datasets/experience.csv", encoding="latin-1", low_memory=False)
df_me['Finish'] = np.where(df_me['Place'].str.contains('Digitas', case=False, na=False), today_str, df_me['Finish'])
df_me['Start_str'] = pd.to_datetime(df_me['Start'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
df_me['Finish_str'] = pd.to_datetime(df_me['Finish'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
df_skills = pd.read_csv("assets/datasets/skills.csv", encoding="latin-1", low_memory=False)
df_gods = pd.read_csv("assets/datasets/gods.csv", encoding="latin-1", low_memory=False)
df_gods['music subgenres'] = df_gods['music subgenres'].str.split(', ')
df_gods['film subgenres'] = df_gods['film subgenres'].str.split(', ')
music_subgenres = [item for sublist in df_gods['music subgenres'] for item in sublist]
music_subgenres = list(set(music_subgenres))
film_subgenres = [item for sublist in df_gods['film subgenres'] for item in sublist]
film_subgenres = list(set(film_subgenres))
gods_dict = dict(zip(df_gods['god'], zip(df_gods['descriptive text'], df_gods['Image URL'], df_gods['personality'])))

MY_DATA = {

    'df_gods': gods_dict,#df_gods[['god', 'descriptive text', 'Image URL', 'personality']],
    'music_subgenres':music_subgenres,
    'film_subgenres':film_subgenres,
    'fig_edu':create_timeline(df_me[df_me['Type'] == 'School']),
    'fig_work':create_timeline(df_me[df_me['Type'] == 'Work']),
    'fig_pl':create_radar(df_skills[df_skills['Type'] == 'Programming Languages'], 'Programming Languages Domain'),
    'fig_bi':create_bar(df_skills[df_skills['Type'] == 'BI'], 'BI Domain'),
    'fig_li':create_map(df_skills[df_skills['Type'] == 'Libraries'], 'Python Libraries Domain', 'Python Libraries'),
    'fig_apache':create_pie(df_skills[df_skills['Type'] == 'Apache'], 'Apache Knowleadge'),
    'fig_sql':create_radar(df_skills[df_skills['Type'] == 'DBMS'], 'DBMS Domain'),
    'fig_cloud':create_map(df_skills[df_skills['Type'] == 'Cloud'], 'Cloud Computing Domain', 'Cloud Computing'),
    'fig_learning':create_pie(df_skills[df_skills['Type'] == 'Learning'], 'Tech Learning'),
    'fig_tech':create_bar(df_skills[df_skills['Type'] == 'Tech'], 'Tech Knowleadge'),
    'fig_agile':create_pie(df_skills[df_skills['Type'] == 'Agile'], 'Known Agile Methodologies'),
    'fig_lan':create_bar(df_skills[df_skills['Type'] == 'Languages'], 'Spoken Languages'),
    'fig_marketing':create_pie(df_skills[df_skills['Type'] == 'Marketing'], 'Marketing'),
}

del df_skills
del df_me
del df_gods
gc.collect()
