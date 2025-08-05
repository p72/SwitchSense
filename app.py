import streamlit as st
import time
import os
from datetime import datetime
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# Configure page
st.set_page_config(
    page_title="SwitchBot Temperature Monitor",
    page_icon="🌡️",
    layout="wide"
)

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def format_temperature(temp_c):
    """Format temperature in both Celsius and Fahrenheit"""
    temp_f = celsius_to_fahrenheit(temp_c)
    return f"{temp_c}°C ({temp_f:.1f}°F)"

def get_battery_status_color(battery_level):
    """Get color for battery status based on level"""
    if battery_level >= 80:
        return "green"
    elif battery_level >= 50:
        return "orange"
    elif battery_level >= 20:
        return "red"
    else:
        return "darkred"

def display_device_card(device_data):
    """Display a card for each thermometer device"""
    device_name = device_data.get('deviceName', 'Unknown Device')
    device_id = device_data.get('deviceId', 'N/A')
    temperature = device_data.get('temperature')
    humidity = device_data.get('humidity')
    battery = device_data.get('battery')
    
    with st.container():
        st.subheader(f"🌡️ {device_name}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if temperature is not None:
                st.metric(
                    label="Temperature",
                    value=format_temperature(temperature)
                )
            else:
                st.error("Temperature data unavailable")
        
        with col2:
            if humidity is not None:
                st.metric(
                    label="Humidity",
                    value=f"{humidity}%"
                )
            else:
                st.info("Humidity data unavailable")
        
        with col3:
            if battery is not None:
                battery_color = get_battery_status_color(battery)
                st.metric(
                    label="Battery",
                    value=f"{battery}%"
                )
                # Display battery status with color
                if battery >= 20:
                    st.success(f"Battery: {battery}% - Good")
                else:
                    st.error(f"Battery: {battery}% - Low")
            else:
                st.info("Battery data unavailable")
        
        # Device details
        st.caption(f"Device ID: {device_id}")
        st.divider()

def main():
    st.title("🌡️ SwitchBot Temperature Monitor")
    st.markdown("Real-time temperature monitoring from your SwitchBot thermometer devices")
    
    # Get API credentials from environment variables
    token = os.getenv("SWITCHBOT_TOKEN")
    secret = os.getenv("SWITCHBOT_SECRET")
    
    if not token or not secret:
        st.error("⚠️ SwitchBot API credentials not found!")
        st.markdown("""
        Please set the following environment variables:
        - `SWITCHBOT_TOKEN`: Your SwitchBot API token
        - `SWITCHBOT_SECRET`: Your SwitchBot API secret
        
        You can obtain these from the SwitchBot app under Settings → App Version → Developer Options.
        """)
        return
    
    # Initialize SwitchBot API
    api = SwitchBotAPI(token, secret)
    
    # Auto-refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
    with col2:
        refresh_interval = st.selectbox("Refresh interval", [10, 30, 60, 120], index=1)
    with col3:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Display last updated time
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"Last updated: {last_updated}")
    
    # Fetch and display device data
    try:
        with st.spinner("Fetching device data..."):
            devices = api.get_devices()
            
        if not devices:
            st.warning("No SwitchBot devices found in your account.")
            return
        
        # Filter for thermometer devices
        thermometer_devices = [
            device for device in devices 
            if device.get('deviceType') in ['Meter', 'MeterPlus', 'Outdoor Meter']
        ]
        
        if not thermometer_devices:
            st.warning("No SwitchBot thermometer devices found.")
            st.info("Make sure you have SwitchBot Meter, Meter Plus, or Outdoor Meter devices registered in your account.")
            return
        
        st.success(f"Found {len(thermometer_devices)} thermometer device(s)")
        
        # Display each thermometer device
        for device in thermometer_devices:
            device_id = device.get('deviceId')
            if device_id:
                try:
                    # Get detailed device status
                    device_status = api.get_device_status(device_id)
                    if device_status:
                        # Merge device info with status
                        device_data = {**device, **device_status}
                        display_device_card(device_data)
                    else:
                        st.error(f"Could not retrieve status for device: {device.get('deviceName', 'Unknown')}")
                except Exception as e:
                    st.error(f"Error fetching data for device {device.get('deviceName', 'Unknown')}: {str(e)}")
    
    except Exception as e:
        st.error(f"Failed to fetch device data: {str(e)}")
        st.markdown("""
        **Possible issues:**
        - Check your internet connection
        - Verify your API credentials are correct
        - Ensure your SwitchBot devices are online and connected
        - Check if you've exceeded API rate limits
        """)
    
    # Auto-refresh logic
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
