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

description_svm = '''
The core of the project involves a machine learning pipeline that processes raw user data to generate a prediction. This process includes:

- Data Preparation: User preferences are transformed into a numerical format using MultiLabelBinarizer, which converts a list of strings (genres, themes) into a one-hot encoded matrix. This matrix represents the presence or absence of a given preference, allowing the model to interpret the data effectively.

- Model Training: The SVM model is trained on a pre-existing dataset that associates deities with various musical and cinematic tastes. The pipeline also incorporates a data scaler to ensure optimal performance, as SVM models are sensitive to the scale of input features.

- Prediction and Recommendation: When a new user's preferences are submitted, the trained model generates a prediction. The system calculates a decision function score for each potential deity. This score represents the model's confidence in the prediction. The application then uses these scores to recommend the most likely deity to the user, providing a more engaging result.
'''
