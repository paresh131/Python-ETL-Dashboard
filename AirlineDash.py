import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import os

# Configuration
DB_FILE = "airline_operations.db"
TABLE_NAME = "flight_data"

def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
df = load_data()

app.layout = dbc.Container([
    html.H1("Airline Passenger Analysis", className="text-center my-4", style={'color': '#2c3e50'}),
    
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Continent:", className="fw-bold"),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['continents'].unique())] if not df.empty else [],
                value='North America',
                clearable=False
            )
        ], width=4)
    ], className="mb-5 justify-content-center"),

    dbc.Row([
        dbc.Col(dcc.Graph(id='pie-status'), width=6),
        dbc.Col(dcc.Graph(id='bar-nationality'), width=6)
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='hist-age-clean'), width=12)
    ], className="mt-5")
], fluid=True)

@app.callback(
    [Output('pie-status', 'figure'),
     Output('bar-nationality', 'figure'),
     Output('hist-age-clean', 'figure')],
    [Input('continent-dropdown', 'value')]
)
def update_graphs(selected_continent):
    if df.empty:
        return {}, {}, {}

    dff = df[df['continents'] == selected_continent]

    # 1. Donut Pie Chart
    fig_pie = px.pie(dff, names='flight_status', hole=0.5,
                     title=f"Flight Status: {selected_continent}",
                     color_discrete_sequence=px.colors.qualitative.Pastel)

    # 2. Top 10 Nationalities Bar Chart
    top_10 = dff['nationality'].value_counts().nlargest(10).reset_index()
    top_10.columns = ['Country', 'Count']
    fig_bar = px.bar(top_10, x='Country', y='Count', 
                     title="Top 10 Nationalities",
                     color='Count', color_continuous_scale='Blues')

    # 3. BIG SLAB HISTOGRAM (10-Year Intervals)
    fig_hist = px.histogram(dff, x='age', 
                            title="Passenger Age Distribution (10-Year Slabs)",
                            labels={'age': 'Age Group (Decades)', 'count': 'Number of Travelers'},
                            color_discrete_sequence=['#34495e'])
    
    # This specific line sets the "Big Slabs" (size=10 means 0-10, 10-20, etc.)
    fig_hist.update_traces(xbins=dict(start=0, end=100, size=10), 
                           marker_line_color='white', marker_line_width=2)
    
    # Visual Polish for all charts
    for fig in [fig_pie, fig_bar, fig_hist]:
        fig.update_layout(title_x=0.5, template="plotly_white", margin=dict(t=50, b=50, l=50, r=50))

    return fig_pie, fig_bar, fig_hist

if __name__ == "__main__":
    app.run(debug=True)