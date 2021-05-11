try:
    import plotly          
    import plotly.graph_objects as go
    import plotly.express as px
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    from dash.exceptions import PreventUpdate
    import pandas as pd 
    import pymysql
except ImportError:
    import subprocess
    subprocess.call('.sh', '.\serverrequierments.sh')
    try:
        import plotly
        import plotly.graph_objects as go
        import plotly.express as px
        import dash
        import dash_core_components as dcc
        import dash_html_components as html
        from dash.dependencies import Input, Output
        from dash.exceptions import PreventUpdate
        import pandas 
        import pymysql
    except ImportError:
        raise ImportError()


app = dash.Dash(__name__)


#curser = mydb.cursor()

query = ('SELECT ID, Temperatur, Luftfeuchtigkeit, Time FROM Daten ORDER BY Coll desc Limit 10000')

def data():
    mydb = pymysql.connect(
    host = '172.19.202.200',
    port = 3306,
    user = 'plotly',
    passwd = 'plotly',
    db = 'Wetterdaten'
)
    print('1')
    #curser = mydb.cursor
    print('1,5')
    df1 = pd.read_sql(query, con=mydb)
    print('2')
    print(df1)
    print('3')
    #curser.close()
    mydb.close()
    print('4')
    #df1.rename(columns = {0: 'ID', 1: 'Temperatur', 2: 'Luftfeuchtigkeit', 3: 'Time'})
    print('5')
    return df1
#------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Interval(
                id='my_interval',
                disabled=False,     #if True, the counter will no longer update
                interval=15*1000,    #increment the counter n_intervals every interval milliseconds
                n_intervals=-1,      #number of times the interval has passed
                max_intervals=-1,    #number of times the interval will be fired.
                                    #if -1, then the interval has no limit (the default)
                                    #and if 0 then the interval stops running.
    ),

    html.Div(id='output_data', style={'font-size':36}),
    dcc.Input(id="input_text",type='text'),
    dcc.Graph(id="mylinechart", figure={'data':[{ 'y': "Temperatur",'x': 'Uhrzeit', 'type': 'line+dot'}]} ),
    dcc.Graph(id="Luftfeuchtigkeit", figure={'data':[{ 'y': 'Luftfeuchtigkeit','x': 'Uhrzeit', 'type': 'line+dot'}]} ),

])

#------------------------------------------------------------------------
@app.callback(
    [Output('output_data','children'),
     Output('mylinechart', 'figure'),
     Output('Luftfeuchtigkeit','figure')],
    [Input('my_interval', 'n_intervals')]
)
def update_graph(num):
    """update every 15 seconds"""
    df = data()
    if num==0:
        raise PreventUpdate
    else:
        fig = px.line(df, x = df['Time'],y = df['Temperatur'], color = df['ID'],)
        fig1 = px.line(df, x = df['Time'],y = df['Luftfeuchtigkeit'], color = df['ID'],) 
        y_data=num
       # fig=go.Figure(data=[go.Line(y=df['Temperatur'], x=df['Time'])],
       #               layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
       # )
       # fig1=go.Figure(data=[go.Line(y=df['Luftfeuchtigkeit'], x=df['Time'])],
       #               layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
       # )
    return (y_data,fig,fig1)
#------------------------------------------------------------------------
@app.callback(
    Output('my_interval', 'max_intervals'),
    [Input('input_text', 'value')]
)
def stop_interval(retrieved_text):
    if retrieved_text == 'stop':
        max_intervals = 0
    else:
        raise PreventUpdate

    return (max_intervals)
#------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(host='172.19.202.200',
        port='3308',
        debug=True)
