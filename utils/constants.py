import gc
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
from dash import html
from dash_iconify import DashIconify
from utils.create_layouts import *

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#DEE2E6",
    "height": "100vh",
    "display": "flex",
    "flexDirection": "column",
    "padding": "2rem 1rem",
    "position": "fixed",
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
    "transition": "all 0.3s",
}

IMAGE_STYLE = {
    'object-fit': 'contain',
    'width': '500px',
    'height': '500px',
    'display': 'block',
}

GITHUB_ICON = html.A(
    [
        DashIconify(icon="mdi:github", width=30, color="black"),
    ],
    href="https://github.com/agus2207",
    target="_blank",
    style={"textDecoration": "none", "color": "black"}
)

LINKEDIN_ICON = html.A(
    [
        DashIconify(icon="mdi:linkedin", width=30, color="black"),
    ],
    href="https://linkedin.com/in/agustin-galindo-reyes-218a25174",
    target="_blank",
    style={"textDecoration": "none", "color": "black"}
)

EMAIL_ICON = html.A(
    [
        DashIconify(icon="mdi:email-outline", width=30, color="black"),
    ],
    href="mailto:agusgalrey22@proton.me",
    target="_blank",
    style={"textDecoration": "none", "color": "black"}
)

WHATSAPP_ICON = html.A(
    [
        DashIconify(icon="mdi:whatsapp", width=30, color="black"),
    ],
    href="https://wa.me/525653560123?text=Hi,%20I%20saw%20your%20CV%20and%20would%20like%20to%20contact%20you.",
    target="_blank",
    style={"textDecoration": "none", "color": "black"}
)

DESCRIPTION_SVM = '''
***Your music. Your movies. Your essence.***

This project combines art, culture, and machine learning to discover which Aztec or Mayan deity best aligns with your personality.

By analyzing your favorite music and film subgenres, the Random Forest model reveals the divine archetype that resonates most with your creative energy.

The core of the project involves a machine learning pipeline that processes user input data to generate accurate and interpretable predictions. This process includes:

##### **1. Data Preparation**
User preferences are transformed into a numerical format using a **MultiLabelBinarizer**, which converts lists of music and film subgenres into a one-hot encoded matrix.
Each column in this matrix represents the presence or absence of a specific subgenre, allowing the model to analyze combinations of artistic preferences in a structured way.

##### **2. Model Training**
The **Random Forest classifier** is trained on a curated dataset that associates Aztec/Mayan deities with distinctive patterns of musical and cinematic tastes.
Unlike single-model approaches, Random Forest builds an *ensemble* of multiple decision trees —each trained on a random subset of the data and features.
During prediction, each tree “votes” for a possible deity, and the forest aggregates these votes to reach a final, consensus-based decision.

This ensemble approach allows the model to:
- Capture **complex, nonlinear relationships** between genres and deities.
- Reduce **overfitting**, improving its ability to generalize to new inputs.
- Maintain strong **predictive performance** even with diverse and categorical data.

##### **3. Prediction and Recommendation**
When a new user submits their favorite genres, the trained model processes these inputs and generates a **probability distribution** across all deities.
Instead of producing a single raw output, Random Forest outputs a **confidence score** for each deity based on the proportion of votes it receives.
The system then recommends the top predicted deities —offering a data-driven yet creative way to connect personal artistic tastes with the symbolic energy of Aztec/Mayan mythology.
'''

ABOUT_ME = '''
***"Solve mentum a molestis. mentum ad concretum dirige" (Epica, 2007, Samadhi)***

Hi!😎🤘 I'm Agustin Galindo Reyes, a Data Systems Engineer with a Bachelor's degree from IPN ESCOM. My passion lies at the intersection of rigorous programming and robust data infrastructure.

I'm grounded in strong technical fundamentals, comfortable with Object-Oriented Programming (OOP) principles using languages like Python and Java, alongside core SQL data management.

**My Focus: Data, Scale, and Automation**

My expertise is centered on transforming raw data into actionable business solutions. I specialize in Python for Data Engineering and analysis, with a high degree of enthusiasm for high-performance libraries like Pandas, Dask, and PySpark.

My experience allows me to manage the complete data lifecycle:

- **Data Engineering**: I build and manage scalable, reliable Python Data Pipelines, leveraging the Apache ecosystem (Pyspark, Airflow) and specialized enterprise tools like AB Initio or Adobe Campaing for complex ETL/ELT processes.

- **Cloud & DevOps**: Working knowledge of major cloud platforms (AWS and Google Cloud) for supporting data workloads. I also experienced in automate critical system tasks and streamline CI/CD using Jenkins and low-level Linux/UNIX scripts.

- **Business Intelligence & Visualization**: Experienced in transforming complex datasets into clear, actionable insights for stakeholders. I design and build interactive executive dashboards using industry-leading BI platforms (PowerBI and Looker Studio), complemented by dynamic reporting tools like Plotly, Matplotlib, and Streamlit for real-time data storytelling.

**Full Stack Versatility and Global Vision**

My profile is unique because I also cover end-to-end development:

- **Web Development**: I deliver Full Stack applications, building Backend APIs (Flask/Django) and dynamic user dashboards with Dash or Streamlit.

- **Business Alignment**: I excel at gathering and translating complex business requirements from global clients into precise technical specifications, ensuring project alignment with strategic goals.

I'm driven by a constant curiosity to stay up-to-date with new technologies and commit to finding the most efficient and scalable solution for every technical challenge.
'''

MY_HOBBIES = '''
Continuous Learning & Culture: Away from technical work, I maintain a strong commitment to continuous growth by regularly taking courses in emerging technologies. I fuel my curiosity by exploring diverse narratives and cultures: I am a dedicated fan of action movies and superhero sagas, and I have a deep fascination with cultural history.

My interest in Maya and Aztec mythology and cosmology is complemented by tourism and visiting museums that house artifacts from these civilizations.

To unwind, I enjoy the creative and focused hobby of collecting LEGO sets and action figures. I also maintain an appreciation for the unique cultural spectacle of Wrestling.

Finally, I dedicate time to intellectual pursuits, engaging with readings and podcasts that explore the intriguing combination of science and spirituality. Musically, I am a devoted follower of the metal genre, frequently attending concerts and music festivals to experience the music live.
'''

MODEL = joblib.load('assets/datasets/rf_model_gods.joblib')
MLB = joblib.load('assets/datasets/mlb_gods.joblib')

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
df_me = pd.read_csv("assets/datasets/experience.csv", encoding="latin-1", low_memory=False)
df_me['Finish'] = np.where(df_me['Place'].str.contains('Digitas', case=False, na=False), today_str, df_me['Finish'])
df_me['Start_str'] = pd.to_datetime(df_me['Start'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
df_me['Finish_str'] = pd.to_datetime(df_me['Finish'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
df_skills = pd.read_csv("assets/datasets/skills.csv", encoding="latin-1", low_memory=False)
df_gods = pd.read_csv("assets/datasets/gods.csv", low_memory=False)
music_subgenres = ['Black metal', 'Lo-fi hip hop', 'Gothic metal', 'Thrash metal', 'Symphonic metal', 'Reggaeton', 'Indie pop', 'Industrial metal', 'World fusion', 'Classical crossover', 'Cumbia', 'Melodic death metal', 'Folk metal', 'Death metal', 'Groove metal', 'Symphonic black metal', 'Nu metal', 'Dream pop', 'Salsa brava', 'Latin rock', 'Power metal', 'Trip hop', 'Ambient', 'Chillwave', 'Punk rock', 'Electro swing', 'Neo classical', 'Doom metal', 'Progressive metal']
film_subgenres = ['Spirituality', 'Comedy', 'Feel-good', 'Psychological thriller', 'Animation', 'Action', 'Dark fantasy', 'Detective mystery', 'Drama', 'Musical', 'Rom-com', 'Adventure', 'Cyberpunk', 'Fantasy', 'Mythological epic', 'Epic adventure', 'Surreal drama', 'Satirical comedy', 'Historical', 'Superhero', 'Gothic horror', 'Romance', 'Epic', 'Horror']
gods_dict = dict(zip(df_gods['Deity'], zip(df_gods['Personality Description'], df_gods['Image URL'], df_gods['General Description'])))

MY_DATA = {

    'df_gods': gods_dict,
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
