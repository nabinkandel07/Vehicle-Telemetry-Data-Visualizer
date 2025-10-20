import can
import cantools
import pandas as pd
from datetime import datetime
import threading

class CANReader:
    def __init__(self, interface='socketcan', channel='can0', dbc_file='vehicle.dbc'):
        self.bus = can.interface.Bus(channel=channel, interface=interface)
        self.db = cantools.database.load_file(dbc_file)
        self.data = pd.DataFrame(columns=['timestamp', 'speed', 'rpm', 'throttle', 'coolant_temp'])
        self.anomaly_thresholds = {'coolant_temp': 95}
        self.listener_thread = threading.Thread(target=self.listen, daemon=True)
        self.listener_thread.start()
    
    def listen(self):
        """Listen and decode CAN messages."""
        for msg in self.bus:
            timestamp = datetime.now()
            try:
                decoded = self.db.decode_message(msg.arbitration_id, msg.data)
                speed = decoded.get('Vehicle_Speed', 0)
                rpm = decoded.get('Engine_RPM', 0)
                throttle = decoded.get('Throttle_Position', 0)
                coolant_temp = decoded.get('Coolant_Temperature', 0)
                
                new_row = pd.DataFrame([[timestamp, speed, rpm, throttle, coolant_temp]], 
                                       columns=self.data.columns)
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                if len(self.data) > 1000:
                    self.data = self.data.tail(1000)
            except:
                pass  # Skip undecodable messages
    
    def get_latest_data(self):
        return self.data.tail(10) if not self.data.empty else pd.DataFrame()
    
    def check_anomalies(self, df):
        """Check for anomalies based on thresholds."""
        anomalies = {}
        for col, threshold in self.anomaly_thresholds.items():
            if col in df.columns and not df.empty:
                latest_val = df[col].iloc[-1]
                if latest_val > threshold:
                    anomalies[col] = latest_val
        return anomalies
