#Importar paquetes
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd 
import plotly.express as px
import dash_bootstrap_components as dbc

#Cargar datasets
atletas = pd.read_csv("registro_olimpico.csv")
years = sorted([int(year) for year in atletas['Año'].unique()], reverse=True)

#Inicializar app
external_stylesheets = [dbc.themes.QUARTZ]
app = Dash(__name__, external_stylesheets=external_stylesheets, title='Olimpiadas')

#Despliegue de componentes
app.layout = dbc.Container([
    dbc.Row([
        html.H1('REGISTRO DE JUEGOS OLÍMPICOS', className="text-secondary text-center fs-3")
    ]),
    dbc.Row([   
        dbc.Col([
            dbc.Row([
                html.H5('Top 5 de Países por Medallas')
            ]),
             dbc.Row([
                dbc.RadioItems(
                    options=[
                        {'label': 'Oro', 'value': 'Gold'},
                        {'label': 'Plata', 'value': 'Silver'},
                        {'label': 'Bronce', 'value': 'Bronze'}
                    ],
                    value='Gold',
                    inline = True,
                    id='control-medalla'
                )
            ]),
            dbc.Row([
                dcc.Graph(figure={}, id='graph-medalla')
            ])
        ], width=6),
        dbc.Col([
            dbc.Row([
                html.H5('Top de Participaciones por País')
            ]),
            dbc.Row([
                dbc.Select(
                    id='participacion-select',
                    options=[
                        {'label': '3', 'value': 3},
                        {'label': '5', 'value': 5},
                        {'label': '10', 'value': 10}
                    ],
                    value=5,
                    className="form-select"
                )
            ]),
            dbc.Row([
                dcc.Graph(figure={}, id='graph-participacion')
            ])   
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H5('Participación Anual por Género')
            ]),
            dbc.Row([
                dbc.Select(
                    id='year-select',
                    options=years,
                    value=2016,
                    className="form-select"
                )
            ]),
            dbc.Row([
                dcc.Graph(figure={}, id='graph-sex-year')
            ]) 
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.P(
                "©Dania Garcia 2024",
                className="text-center text-muted"
            )
        ], width=12)
    ])
])


@callback(
    Output(component_id='graph-medalla', component_property='figure'),
    Input(component_id='control-medalla', component_property='value')
)
def update_graph(col_chosen):
    medalla = ''
    if col_chosen == 'Gold':
        medalla = 'Oro'
    elif col_chosen == 'Silver':
        medalla = 'Plata'
    else:
        medalla = 'Bronce'

    df = atletas[atletas['Medalla'] == col_chosen]
    top_5 = df['País'].value_counts().sort_values(ascending=False).head(5).reset_index()
    top_5.columns = ['País', 'Total']
    fig = px.bar(
        top_5, 
        x='País', 
        y='Total',
        title=f'Top 5 países con más medallas de {medalla}',
        color='País')
    fig.update_layout(showlegend=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo general del gráfico
        plot_bgcolor='rgba(0,0,0,0)' ,
        font=dict(color='white'),           # Color blanco para todos los textos
        title_font=dict(color='white', size=20),  # Color blanco para el título del gráfico
        legend=dict(font=dict(color='white')),   # Color blanco para la leyenda
        xaxis=dict(tickfont=dict(color='white'), titlefont=dict(color='white')),  # Eje X (si aplica)
        yaxis=dict(tickfont=dict(color='white'), titlefont=dict(color='white'))   # Eje Y (si aplica)   # Fondo del área de la trama
    )
    return fig

@callback(
    Output(component_id='graph-participacion', component_property='figure'),
    Input(component_id='participacion-select', component_property='value')
)
def update_graph(col_chosen):
    col_chosen = int(col_chosen)
    df = atletas['País'].value_counts().sort_values(ascending=False).head(col_chosen).reset_index()
    df.columns = ['País', 'Participaciones']
    fig = px.bar(
        df, 
        x='Participaciones', 
        y='País',
        title=f'Top {col_chosen} de Participaciones por País',
        color='País',
        orientation='h')
    fig.update_layout(showlegend=False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo general del gráfico
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),           # Color blanco para todos los textos
        title_font=dict(color='white', size=20),  # Color blanco para el título del gráfico
        legend=dict(font=dict(color='white')),   # Color blanco para la leyenda
        xaxis=dict(tickfont=dict(color='white'), titlefont=dict(color='white')),  # Eje X (si aplica)
        yaxis=dict(tickfont=dict(color='white'), titlefont=dict(color='white'))   # Eje Y (si aplica)
    )
    return fig

@callback(
    Output(component_id='graph-sex-year', component_property='figure'),
    Input(component_id='year-select', component_property='value')
)
def update_graph(col_chosen):
    col_chosen = int(col_chosen)
    df = atletas[atletas['Año'] == col_chosen]
    df['Sexo'] = df['Sexo'].replace({'M': 'Masculino', 'F': 'Femenino'})
    sexo_counts = df['Sexo'].value_counts().reset_index()
    sexo_counts.columns = ['Sexo', 'Total']
    fig = px.pie(
        sexo_counts,
        values='Total',
        names='Sexo',
        hole=.3,
        color='Sexo',
        color_discrete_map={
            'Masculino': '#1616a7',
            'Femenino': '#fe00fa'
        }
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Fondo general del gráfico
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),           # Color blanco para todos los textos
        title_font=dict(color='white', size=20),  # Color blanco para el título del gráfico
        legend=dict(font=dict(color='white')),   # Color blanco para la leyenda
    )
    return fig


#Ejecutar app
if __name__ == '__main__':
    app.run_server(debug=True)
