# -*- coding: utf-8 -*-
try:
    import pymysql
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    import plotly.express as px
    import plotly.graph_objs as go
    import pandas as pd
    import cdata as mod
except ImportError:
    import subprocess
    subprocess.call('sh', './Serverrequierments.sh')
    try:
        import pymysql
        import dash
        import dash_core_components as dcc
        import dash_html_components as html
        from dash.dependencies import Input, Output
        import plotly.express as px
        import plotly.graph_objs as go
        import pandas as pd
        import cdata as mod
    except ImportError:
            raise ImportError "es Konnten nicht alle libraries korekt insterliert werden bitte kontroliren sie das sie das program als root ausgeführet haben Fals dies nich hilft führen sie bitter dei Serverrequierment.sh manuel alls root aus "
"""setzt die zugangs daten vom SQL server in die Variable 
Muss manuel vom user angepasst werden"""
mydb = pymysql.connect(host = '172.21.202.200',
                       port = 3306,
                       user = 'python',
                       passwd = 'python',
                       db = 'Wetterdaten'
    )

cursor = mydb.cursor()
query = ("SELECT ID, Temperatur, Luftfeuchtigkeit, Time From Daten ORDER BY Coll desc LIMIT 10000")
def wert():
    df = pd.read_sql(query, con=mydb)
    #print(df)
    df.rename(columns = {0: 'ID', 1: 'Temperatur', 2: 'Luftfeuchtigkeit', 3: 'Time'})





app = dash.Dash(__name__)
app.titel = 'Temperatur'

#trace = px.line(x = df['Time'], y = df['Temperatur'],color = df['ID'],
#"""px.line legt die form des graphen fest """
#                labels={
#                    """ Legt die bezeichtnug der x axce und y axce fest und die bezeichnug der einelnene zeilen"""
#                    "x": "Datetime",
#                    "y": "Temperatur in °C",
#                    "color": "Station"
#                    }
#                )
#tracel = px.line(x = df['Time'], y = df['Luftfeuchtigkeit'], color = df['ID'],
#                labels= {
#                    'x': "Datetime",
#                    'y': "Luftfeuctigkeit",
#                    'color': "Station" 
#                })
#    



app.layout = html.Div([
   # dcc.Graph(id = "Temp", figure = trace),
   # dcc.Graph(id = "Luftf", figure = tracel),
    """erstellt die graphen """
   # html.Pre(
    #    """vormatirung der graphen """
     #   id = 'structer',
      #  style = {
       #     'border': 'thin grey solid',  
        #    'overflowY': 'scroll',
         #   'height': '275px'
          #  }
    
        #),
    dcc.Interval(
        """legt den aktualisirung interval fest """
        id = 'graph-update',
        interval = 1000,
        n_intervals = 0 
        )
        
    ])
@app.callback(Output("Temp", "figure"),
            events=[Event('graph-update', "interval")])
def update_graph_scatter():
    X.append(wert['Time'])
    Y.append(wert['Temperatur'])
    data = plotly.graph_ogjs.Scatter(
        x = wert()['Time'],
        y = wert()['Temperatur'],
        color = wert()['ID'],
        name = 'scatter',
        mode = 'lines+markers'

    )
    return {'data': [data],
            'layout' go.layout()}

@app.callback(Output("luftf", "figure"),
            events=[Event('graph-update', "interval")])
def update_graph_scatterl():
    X.append(wert['Time'])
    Y.append(wert['Luftfeuchtigkeit'])
    data = plotly.graph_ogjs.Scatter(
        x = wert()['Time'],
        y = wert()['Luftfeuchtigkeit'],
        color = wert()['ID'],
        name = 'scatter',
        mode = 'lines+markers'

    )
    return {'data': [data],
            'layout' go.layout()}

try:
    """legt die daten der webseite fest Host muss soweit ich es weis eine IPv4 addresse sein (zumindest wenn es nicht die enterprise version von plotly ist) """
    app.run_server(host = "172.19.202.200",
                   port = 8050,
                   debug = False)    
except KeyboardInterrupt:
    exit(-1)
