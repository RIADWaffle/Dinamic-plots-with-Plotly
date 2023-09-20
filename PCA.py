from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph"),
    html.P("Number of components:", className="titulo tk-poppins"),

    html.Div(className= 'slider', children=[
        dcc.Slider(
        id='slider',
        min=2, max=6, value=4, step=1)
    ])
])


@app.callback(
    Output("graph", "figure"), 
    Input("slider", "value"))

def run_and_plot(components):

     #Load your dataset (replace 'your_data.csv' with your actual data file)
    data = pd.read_csv('datos3.csv')

    #Separate the features from the dataset (adjust the columns as needed)
    X = data.iloc[:, 1:]  # Assuming the first column contains labels or IDs

    #Standardize the features (if needed)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    #Perform PCA with the desired number of components (e.g., 4)
    pca = PCA(n_components=components)
    X_pca = pca.fit_transform(X_scaled)

    #Create a DataFrame with PCA components
    pca_df = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(components)])

    #Add the target variable (e.g., "species") to the PCA DataFrame
    pca_df['Age'] = data['BMI']  # Replace 'species' with your target variable name

    #Create a scatter matrix plot using Plotly Express with custom colors
    color_discrete_map = {label: color for label, color in zip(pca_df['Age'].unique(), px.colors.qualitative.Plotly)}



    nPca = [f"PC{i+1}" for i in range(components)]

    labels = {str(i): f"PC {i+1}" 
              for i in range(components)}
    labels['color'] = 'Age'

    fig = px.scatter_matrix(
        pca_df,
        color='Age',
        dimensions= nPca,
        color_continuous_scale = "Tealgrn",
        color_discrete_map=color_discrete_map,  # Assign custom colors to target variable
        title='PCA Scatter Matrix Plot'
    )

    fig.update_layout({
        'plot_bgcolor': 'rgb(51, 51, 51)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_color' : 'rgb(225,225,225)'
    })

    return fig


app.run_server(debug=True)