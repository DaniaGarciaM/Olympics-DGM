#Importar paquetes
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd 
import plotly.express as px

#Cargar datasets
atletas = pd.read_csv("registro_olimpico.csv")

#Inicializar app
app = Dash()

#Despliegue de componentes
app.layout = [
    html.Div(children='Prueba con Data'),
    html.Hr(),
    dash_table.DataTable(data=atletas.to_dict('records'), page_size=10),
]

#Ejecutar app
if __name__ == '__main__':
    app.run_server(debug=True)
