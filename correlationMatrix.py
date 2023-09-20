from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

data = pd.read_csv('datos3.csv')
corr = data.corr()



app = Dash(__name__ ,
                external_stylesheets= ['asdas\assets\style.css', 'https://use.typekit.net/hyc4drk.css'])


app.layout = html.Div(children=[

    html.Div(className="content", children=[

        dcc.Checklist(
            id='variables',
            className= "check tk-poppins",

        options=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                'Diabetes', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth',
                'DiffWalk', 'Age'],

        value=['HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
                'Diabetes', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth',
                'DiffWalk', 'Age'],
    ),

    dcc.Graph(id="graph", className="graph tk-poppins"),

    ]),


    

])


@app.callback(
    Output("graph", "figure"), 
    Input("variables", "value"))
def filter_heatmap(cols):
    fig = px.imshow(corr[cols] , color_continuous_scale = "Tealgrn" )
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'font_color' : 'rgb(225,225,225)'
    })

    return fig


app.run_server(debug=True)