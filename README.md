# Vehicle Telemetry Data Visualizer
This is a complete implementation for the Vehicle Telemetry Data Visualizer project. It simulates or captures CAN Bus data (speed, RPM, throttle) using Python-CAN (with a fallback simulator), processes it with Pandas, and displays it on an interactive, real-time web dashboard using Plotly Dash. The dashboard updates live for engineering diagnostics, showing graphs and metrics. It's designed for automotive testing without requiring actual vehicle hardware (simulator included).

| Detail | Description |
| :--- | :--- |
| **Project Title** | Vehicle Telemetry Data Visualizer |
| **Discipline** | Automotive Engineering, Data Engineering, Embedded Systems (CAN Bus) |
| **Goal** | To create a real-time, interactive web dashboard for monitoring and diagnosing critical vehicle parameters by capturing and interpreting raw CAN Bus data, with added features for anomaly detection, logging, and engineering diagnostics. |
| **Python Libraries** | `pandas`, `plotly`, `Dash`, `python-can`, `cantools`, `numpy`, `csv` (built-in) |
| **Hardware** | **Real:** PC/Raspberry Pi, CAN Bus Interface (e.g., Kvaser, CANable, or PiCAN board). **Simulated:** None (Python only). |

# Requirements
Hardware: Optional CAN Bus interface (e.g., USB CAN adapter like Peak CAN). If not available, use the simulator.
Software: Python 3.7+, libraries: pandas, plotly, dash, python-can (install via pip install python-can if hardware is used; otherwise, skip).
Installation: Run pip install pandas plotly dash. For CAN: pip install python-can (requires system CAN drivers if using hardware).
Code Files
Save these in a directory (e.g., vehicle-telemetry-visualizer). The main script is dashboard.py, with a simulator for testing.

## Setup and Usage
Install Dependencies: Run pip install pandas plotly dash.
Run the Dashboard: Execute python dashboard.py. Open http://localhost:8050 in a browser for the live dashboard.
Data Source: Uses the simulator by default. For real CAN data, replace CANSimulator with CANReader in dashboard.py and ensure your CAN interface is set up (e.g., sudo ip link set can0 up type can bitrate 500000).
Customization: Adjust data parsing in can_reader.py for your specific CAN messages. Add more metrics (e.g., fuel level) by extending the DataFrame.
Performance: Simulator runs at 10Hz; real CAN depends on bus speed. Dashboard updates every second.
Testing: With the simulator, you'll see fluctuating graphs. For hardware, connect and test with a vehicle or emulator.

## Enhanced Features
- DBC decoding with `cantools`.
- Anomaly detection and alerts.
- Gauge charts for diagnostics.
- CSV logging and export.
- Real-time filtering.

### Technical Breakdown and Step-by-Step Implementation

This project is implemented in three main stages: Data Acquisition, Data Processing, and Visualization, with enhancements for diagnostics and logging.

#### Stage 1: Data Acquisition (The CAN Bus Interface)
The CAN Bus is the vehicle's communication network. Data is captured as raw packets.

- **Implementation Options:**
  - **Simulation (Pure Python):** Uses `python-can` to create a virtual bus and generate simulated CAN messages (e.g., for speed, RPM, throttle, coolant temp) at 10Hz intervals. A thread continuously sends `can.Message` objects.
  - **Real Hardware Capture (Advanced):** Connects to a physical CAN interface via ODB-II. The script listens for real messages using `python-can`.

#### Stage 2: Data Processing and Decoding
Raw CAN data is decoded using a DBC file for scaling and units.

- **Steps:**
  - **Decoding:** `cantools` parses raw messages based on DBC rules, extracting signals like `Vehicle_Speed` (scaled from bytes).
  - **Structuring:** Decoded data is stored in `pandas` DataFrames for time-series analysis.
  - **Buffering:** Uses a rolling buffer (last 1000 points) with `collections.deque` for efficiency.
  - **Anomaly Detection:** Checks values against thresholds (e.g., coolant temp > 95°C) and flags anomalies.

#### Stage 3: Visualization and Interactivity (The Dash Dashboard)
Dash creates a web-based dashboard with real-time updates.

- **Features:**
  - **Layout:** Uses `dash.html` for a professional diagnostic screen.
  - **Plotting:** `plotly` for line charts (time-series) and gauge charts (instant values like RPM).
  - **Live Updates:** `dcc.Interval` triggers callbacks every 500ms to refresh data from the buffer.
  - **Diagnostics:** Gauges highlight anomalies (e.g., red for high temp). Add sliders for filtering (e.g., speed > 60 km/h).
  - **Logging:** Data is appended to a CSV file; export via Dash button.

### Engineering Value and Diagnostics

- **Real-Time Diagnostics:** Gauges show instant values; charts reveal trends (e.g., throttle vs. RPM correlation).
- **Fault/Anomaly Detection:** Alerts for thresholds; logs enable post-analysis.
- **Performance Analysis:** Visualize engine response during acceleration.

### Key Python Libraries Detail

| Library | Role in Project | Why it's Used |
| :--- | :--- | :--- |
| **`python-can`** | Hardware Interface/Simulation | Unified interface for CAN buses, virtual or real. |
| **`cantools`** | CAN DBC Decoding | Decodes raw messages into engineering units using DBC files. |
| **`pandas`** | Data Structuring | Manages time-series data efficiently for analysis. |
| **`Plotly Dash`** | Front-end Visualization | Builds interactive web dashboards in Python. |
| **`numpy`** | Numerical Operations | Fast computations for data scaling. |
| **`csv`** | Logging | Built-in for exporting data to CSV files. |

### Code Files Summary
- **data_simulator.py:** Generates virtual CAN data.
- **can_reader.py:** Reads/decodes real or simulated CAN data with anomalies.
- **dashboard.py:** Dash app with graphs, gauges, alerts, and logging.

### Setup and Usage
- Install libraries: `pip install pandas plotly dash python-can cantools numpy`.
- Run `python dashboard.py` and visit `http://localhost:8050`.
- For hardware, use `CANReader` and a DBC file.





