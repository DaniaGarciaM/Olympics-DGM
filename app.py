#Importar paquetes
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd 
import plotly.express as px

#Cargar datasets
atletas = pd.read_csv("datasets/athlete_events.csv", index_col=0)

#Inicializar app
app = Dash()

#Despliegue de componentes
app.layout = [
    html.Div(children='Prueba con Data'),
    html.Hr(),
    dash_table.DataTable(data=atletas.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.bar(atletas, x='Height', y='Weight'))
]

#Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)
