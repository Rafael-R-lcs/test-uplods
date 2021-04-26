try:  
    import plotly          
    import plotly.graph_objects as go

    import dash             
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.dependencies import Input, Output
    from dash.exceptions import PreventUpdate
    import pandas 
    import pymysql
except ImportError:
    import subprocess
    subprocess.call('.sh', '.\serverrequierments.sh')
    try:
        import plotly          
        import plotly.graph_objects as go

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
mydb = pymysql.connect(
    host = '172.21.202.200',
    port = '3306',
    user = 'python',
    passwd = 'python',
    db = 'Wetterdaten'
)

curser = mydb.curser()

query = ('SELECT ID, Temperatur, Luftfeuchtigkeit, Time FROM Daten ORDER BY Coll desc Limit 10000')
def data(): 
    df = pd.read_sql(query, con=mydb)
    df.rename(columns = {0: 'ID', 1: 'Temperatur', 2: 'Luftfeuchtigkeit', 3: 'Time'})
    return df 
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
    dcc.Graph(id="mylinechart"),

])

#------------------------------------------------------------------------
@app.callback(
    [Output('output_data', 'df'),
     Output('mylinechart', 'figure')],
    [Input('my_interval', 'n_intervals')]
)
def update_graph(num):
    """update every 3 seconds"""
    if num==0:
        raise PreventUpdate
    else:
        y_data=num
        fig=go.Figure(data=[go.graph(x=data.df['Temperatur'], y=data.df['Time'], color=data.df['ID'])],
                      layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
        )
        fig=go.Figure(data=[go.graph(x=data.df['Luftfeuchtigkeit'], y=data.df['Time'], color=data.df['ID'])],
                      layout=go.Layout(yaxis=dict(tickfont=dict(size=22)))
        )
    return (y_data,fig)

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
        port=3308,
        debug=True)
