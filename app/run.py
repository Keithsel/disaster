import sys
import os
import json
import plotly
import nltk
import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
from flask import Flask, render_template, request
from plotly.graph_objs import Bar, Image, Table
from sqlalchemy import create_engine

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../models')))

from train_classifier import POSTagEncoder, NEREncoder

app = Flask(__name__)

nltk.download('stopwords')

pos_tag_encoder = POSTagEncoder()
ner_encoder = NEREncoder()


def tokenize(text):
    """Tokenize, lemmatize, and clean text data with POS and NER features."""
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


# Load data
engine = create_engine('sqlite:////home/ibi/Documents/GitHub/disaster/data/DisasterResponseData.db')
df = pd.read_sql_table('message', engine)

# Load model
model = joblib.load("/home/ibi/Documents/GitHub/disaster/models/classifier.pkl")


@app.route('/')
@app.route('/index')
def index():
    """
    Display visuals and receive user input for the model.

    Renders the main page with various graphs and visualizations.
    """
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    category_counts = df.iloc[:, 4:].sum().sort_values(ascending=False)
    category_names = list(category_counts.index)

    class_counts = df.iloc[:, 4:].sum(axis=1)
    class_counts_distribution = class_counts.value_counts().sort_index()
    class_counts_values = list(class_counts_distribution.index)
    class_counts_freq = list(class_counts_distribution.values)

    # word cloud
    stop_words = set(stopwords.words('english'))
    words = ' '.join(df['message'])
    wordcloud = WordCloud(stopwords=stop_words, max_words=100,
                          background_color="white").generate(words)
    wordcloud_image = wordcloud.to_array()

    overall_metrics = pd.read_sql_table(
        'overall_metrics', engine).iloc[0]

    overall_metrics = overall_metrics.apply(lambda x: format(x, '.2f'))

    overall_table = {
        'data': [
            Table(
                header=dict(
                    values=['Metric', 'Score'],
                    fill_color='paleturquoise',
                    align='left'
                ),
                cells=dict(
                    values=[
                        ['Precision', 'Recall', 'F1 Score', 'Accuracy'],
                        [
                            overall_metrics['average_precision'],
                            overall_metrics['average_recall'],
                            overall_metrics['average_f1_score'],
                            overall_metrics['average_accuracy']
                        ]
                    ],
                    fill_color='lavender',
                    align='left'
                )
            )
        ],
        'layout': {
            'title': 'Overall Performance Metrics'
        }
    }

    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],
            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=category_names,
                    y=category_counts
                )
            ],
            'layout': {
                'title': 'Number of Messages Classified in Each Category',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Category",
                    'tickangle': -45
                }
            }
        },
        {
            'data': [
                Bar(
                    x=class_counts_values,
                    y=class_counts_freq
                )
            ],
            'layout': {
                'title': 'Distribution of the Number of Classes per Message',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Number of Classes"
                }
            }
        },
        {
            'data': [
                Image(
                    z=wordcloud_image
                )
            ],
            'layout': {
                'title': 'Word Cloud of Messages',
                'xaxis': {
                    'visible': False
                },
                'yaxis': {
                    'visible': False
                }
            }
        }
    ]

    performance_graphs = [overall_table]

    graph_ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    performance_ids = ["performance-{}".format(i) for i, _ in enumerate(
        performance_graphs)]
    graphJSON = json.dumps(graphs + performance_graphs,
                           cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('master.html', ids=graph_ids + performance_ids,
                           graphJSON=graphJSON, results_page=False)


@app.route('/go')
def go():
    """
    Handle user query and display model results.

    Renders the classification results page for the user's input message.
    """
    query = request.args.get('query', '')

    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results,
        results_page=True
    )


def main():
    """Run the Flask app."""
    app.run(host='0.0.0.0', port=3000, debug=True)


if __name__ == '__main__':
    main()
