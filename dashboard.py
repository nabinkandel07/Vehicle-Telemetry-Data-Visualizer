import dash
from dash import html, dcc, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import threading
import time
from data_simulator import CANSimulator  # Or CANReader for hardware
import csv

# Initialize data source
data_source = CANSimulator()  # Switch to CANReader() for real CAN
log_file = 'telemetry_log.csv'

# Start data generation
thread = threading.Thread(target=data_source.generate_data, daemon=True)
thread.start()

# Initialize log
with open(log_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'speed', 'rpm', 'throttle', 'coolant_temp'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Vehicle Telemetry Data Visualizer"),
    dcc.Interval(id='interval-component', interval=500, n_intervals=0),
    html.Div([
        dcc.Graph(id='live-graph'),
        html.Div([
            dcc.Graph(id='gauge-speed', style={'width': '30%'}),
            dcc.Graph(id='gauge-rpm', style={'width': '30%'}),
            dcc.Graph(id='gauge-throttle', style={'width': '30%'})
        ], style={'display': 'flex'}),
    ]),
    html.Div(id='anomaly-alert', style={'color': 'red', 'fontSize': 20}),
    html.Div(id='metrics'),
    dcc.Store(id='data-store'),
    html.Button('Export Log', id='export-btn'),
    dcc.Download(id='download-log')
])

@app.callback(
    [Output('live-graph', 'figure'), Output('gauge-speed', 'figure'), 
     Output('gauge-rpm', 'figure'), Output('gauge-throttle', 'figure'),
     Output('anomaly-alert', 'children'), Output('metrics', 'children'),
     Output('data-store', 'data')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    df = data_source.get_latest_data()
    if df.empty:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), "", "No data", {}
    
    # Log data
    df.to_csv(log_file, mode='a', header=False, index=False)
    
    # Time-series graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['speed'], mode='lines', name='Speed'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['rpm'], mode='lines', name='RPM'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['throttle'], mode='lines', name='Throttle'))
    fig.update_layout(title='Real-Time Telemetry')
    
    # Gauges
    gauge_speed = go.Figure(go.Indicator(mode="gauge+number", value=df['speed'].iloc[-1], 
                                         title={'text': "Speed (km/h)"}, gauge={'axis': {'range': [0, 120]}}))
    gauge_rpm = go.Figure(go.Indicator(mode="gauge+number", value=df['rpm'].iloc[-1], 
                                       title={'text': "RPM"}, gauge={'axis': {'range': [0, 6000]}}))
    gauge_throttle = go.Figure(go.Indicator(mode="gauge+number", value=df['throttle'].iloc[-1], 
                                            title={'text': "Throttle (%)"}, gauge={'axis': {'range': [0, 100]}}))
    
    # Anomaly check
    anomalies = data_source.check_anomalies(df)
    alert = f"Anomalies: {anomalies}" if anomalies else ""
    
    latest = df.iloc[-1]
    metrics = f"Latest: Speed: {latest['speed']:.1f}, RPM: {latest['rpm']:.0f}, Throttle: {latest['throttle']:.1f}, Coolant: {latest['coolant_temp']:.1f}°C"
    
    return fig, gauge_speed, gauge_rpm, gauge_throttle, alert, metrics, df.to_dict('records')

@app.callback(
    Output('download-log', 'data'),
    [Input('export-btn', 'n_clicks')],
    prevent_initial_call=True
)
def export_log(n_clicks):
    return dcc.send_file(log_file)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
