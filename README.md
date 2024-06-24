# Disaster Response Pipeline Project

- [Disaster Response Pipeline Project](#disaster-response-pipeline-project)
  - [Description](#description)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Dependencies](#dependencies)
    - [Executing Program:](#executing-program)

<a name="descripton"></a>
## Description

The project aim is to build a Natural Language Processing (NLP) model to categorize messages on a real time basis.

The dataset includes annotations for 36 intent and content class labels, represented as binary values (1 = present, 0 = absent).

<a name="project_structure"></a>
## Project Structure
```
README.md
├── app
│   ├── run.py
│   └── templates
│       ├── go.html
│       └── master.html
├── data
│   ├── DisasterResponseData.db
│   ├── disaster_categories.csv
│   ├── disaster_messages.csv
│   └── process_data.py
├── environment.yml
├── models
│   ├── classifier.pkl
│   └── train_classifier.py
└── notebooks
    ├── ETL Pipeline Preparation.ipynb
    └── ML Pipeline Preparation.ipynb
```

<a name="getting_started"></a>
## Getting Started

<a name="dependencies"></a>
### Dependencies
* Python 3
* NumPy, SciPy, Pandas, Sciki-Learn for machine learning related tasks
* NLTK for NLP processing
* SQLalchemy for database
* Pickle and joblib for model storage
* Flask, Plotly for web app and data visualization

To install the required packages, create a new environment and install the packages from the environment.yml file by running the following commands:
    
    ```bash
    conda env create -f environment.yml -n <env_name>
    conda activate <env_name>
    ```

<a name="execution"></a>
### Executing Program:
1. You can run the following commands in the project's directory to set up the database, train model and save the model.

    - To clean data and store the processed data in the database, run the file `process_data.py` in the `data` directory.
        ```bash
        python process_data.py <path/to/messages/csv/file> <path/to/categories/csv/file> <path/to/database>
        ```
    - To train the classifier and save the model, run the file `train_classifier.py` in the `models` directory.
        ```bash
        python train_classifier.py <path/to/database> <path/to/model>
        ```

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/