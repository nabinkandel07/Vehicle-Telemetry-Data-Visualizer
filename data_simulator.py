import random
import time
import pandas as pd
from datetime import datetime
import can

class CANSimulator:
    def __init__(self):
        self.bus = can.interface.Bus(bustype='virtual')  # Virtual bus for simulation
        self.data = pd.DataFrame(columns=['timestamp', 'speed', 'rpm', 'throttle', 'coolant_temp'])
        self.anomaly_thresholds = {'coolant_temp': 95}  # Example thresholds
    
    def generate_data(self):
        """Simulate CAN messages."""
        while True:
            timestamp = datetime.now()
            speed = random.uniform(0, 120)
            rpm = random.uniform(800, 6000)
            throttle = random.uniform(0, 100)
            coolant_temp = random.uniform(70, 100)  # Simulate with occasional anomalies
            
            # Simulate CAN messages (mimic DBC signals)
            msg_speed = can.Message(arbitration_id=0x123, data=int(speed * 10).to_bytes(2, 'big'))
            msg_rpm = can.Message(arbitration_id=0x456, data=int(rpm).to_bytes(2, 'big'))
            msg_throttle = can.Message(arbitration_id=0x789, data=bytes([int(throttle)]))
            msg_coolant = can.Message(arbitration_id=0xABC, data=bytes([int(coolant_temp)]))
            
            # Send to virtual bus
            self.bus.send(msg_speed)
            self.bus.send(msg_rpm)
            self.bus.send(msg_throttle)
            self.bus.send(msg_coolant)
            
            time.sleep(0.1)
    
    def get_latest_data(self):
        return self.data.tail(10) if not self.data.empty else pd.DataFrame()
