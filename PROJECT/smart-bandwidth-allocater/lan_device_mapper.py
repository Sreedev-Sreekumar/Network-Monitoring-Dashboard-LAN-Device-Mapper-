import streamlit as st
import subprocess
import pandas as pd
import socket

st.set_page_config(page_title="Network Monitor", layout="wide")

st.title("🛡 Network Monitoring Dashboard")

st.markdown("Monitor devices connected to your local network")

devices = []

def get_network():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    network = ".".join(ip.split(".")[:3])
    return network

def ping(ip):
    try:
        output = subprocess.run(
            ["ping", "-n", "1", "-w", "100", ip],
            capture_output=True,
            text=True
        )
        if "TTL=" in output.stdout:
            return True
    except:
        return False

def detect_device(ip):
    last = int(ip.split(".")[-1])

    if last == 1:
        return "Router / Host"
    elif last < 10:
        return "Computer"
    else:
        return "Mobile Device"

if st.button("🔍 Scan Network"):

    network = get_network()

    st.info(f"Scanning Network: {network}.x")

    for i in range(1, 60):

        ip = f"{network}.{i}"

        if ping(ip):

            devices.append({
                "IP Address": ip,
                "Device Type": detect_device(ip),
                "Status": "Active"
            })

    if devices:

        df = pd.DataFrame(devices)

        col1, col2 = st.columns(2)

        col1.metric("Total Devices Detected", len(devices))
        col2.metric("Network Range", f"{network}.x")

        st.subheader("Connected Devices")

        st.dataframe(df)

    else:

        st.warning("No active devices detected")