import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import plotly.express as px

from dash import Dash, dcc, html, Input, Output




app = Dash(__name__, external_stylesheets= ['asdas\assets\style.css', 'https://use.typekit.net/hyc4drk.css'])


app.layout = html.Div(className="content tk-poppins" , children=[

    html.Div(className='selector' ,children=[
        html.P("graph:" , className="titulo tk-poppins"),
        dcc.Dropdown(
            className="dropdown tk-poppins",
            id="ticker",
            options=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                    'Diabetes', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth',
                    'DiffWalk', 'Age'],
            value="BMI",
            clearable=False,
        ),
    ]),


    html.Div(children=[
        dcc.Graph(id="time-series-chart"),
    ]),
])

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))

def display_time_series(ticker):
    data = pd.read_csv('datos4.csv')

    bmi_data = data[ticker]
    time_axis = range(len(bmi_data))
    time_step = 1
    years = [str(year) for year in range(0, len(bmi_data) , time_step)]

    # Separate the target labels (y) from the features (X)
    X = data.iloc[:, :-1]  # Assuming the last column contains labels (target)
    y = data.iloc[:, -1]  # Assuming the last column contains labels (target)

    # Split the dataset into features (X) and target labels (y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # Standardize the input features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Create a neural network model
    model = keras.Sequential([
        keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')  # Binary classification (ill or not ill)
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=150, batch_size=32, validation_split=0.1)

    # Evaluate the model on the test set
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print(f'Test accuracy: {test_acc}')

    color_palette = ['#008080', '#2E8B57', '#3CB371', '#90EE90']

    # Plot the "BMI" values over time
    fig = px.line(data , time_axis, bmi_data, labels={'x': 'Months worked'}, color_discrete_sequence=color_palette)
    fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            'font_color' : 'rgb(225,225,225)'
    })

    return fig

app.run_server(debug=True)