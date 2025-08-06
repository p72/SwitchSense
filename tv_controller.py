import streamlit as st
import os
from datetime import datetime
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# Configure page
st.set_page_config(
    page_title="SwitchBot TV Controller",
    page_icon="📺",
    layout="wide"
)

def display_tv_controls(device_data, api):
    """Display TV control interface"""
    device_name = device_data.get('deviceName', 'Unknown TV')
    device_id = device_data.get('deviceId', 'N/A')
    
    st.subheader(f"📺 {device_name}")
    
    # Power control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔌 Power", key=f"power_{device_id}"):
            try:
                # Check if it's an infrared remote
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "turnOn")
                else:
                    api.tv_power(device_id)
                st.success("Power command sent!")
            except Exception as e:
                st.error(f"Failed to send power command: {str(e)}")
    
    with col2:
        if st.button("🔄 Refresh Status", key=f"refresh_{device_id}"):
            st.rerun()
    
    # Volume controls
    st.write("**Volume Controls**")
    vol_col1, vol_col2, vol_col3 = st.columns(3)
    
    with vol_col1:
        if st.button("🔊 Volume Up", key=f"volup_{device_id}"):
            try:
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "volumeUp")
                else:
                    api.tv_volume_up(device_id)
                st.success("Volume increased!")
            except Exception as e:
                st.error(f"Failed to increase volume: {str(e)}")
    
    with vol_col2:
        if st.button("🔉 Volume Down", key=f"voldown_{device_id}"):
            try:
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "volumeDown")
                else:
                    api.tv_volume_down(device_id)
                st.success("Volume decreased!")
            except Exception as e:
                st.error(f"Failed to decrease volume: {str(e)}")
    
    with vol_col3:
        volume = st.slider("Set Volume", 0, 100, 50, key=f"volume_{device_id}")
        if st.button("Set Volume", key=f"setvol_{device_id}"):
            try:
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "setVolume", str(volume))
                else:
                    api.tv_set_volume(device_id, volume)
                st.success(f"Volume set to {volume}!")
            except Exception as e:
                st.error(f"Failed to set volume: {str(e)}")
    
    # Channel controls
    st.write("**Channel Controls**")
    ch_col1, ch_col2, ch_col3 = st.columns(3)
    
    with ch_col1:
        if st.button("📺 Channel Up", key=f"chup_{device_id}"):
            try:
                api.tv_channel_up(device_id)
                st.success("Channel increased!")
            except Exception as e:
                st.error(f"Failed to increase channel: {str(e)}")
    
    with ch_col2:
        if st.button("📺 Channel Down", key=f"chdown_{device_id}"):
            try:
                api.tv_channel_down(device_id)
                st.success("Channel decreased!")
            except Exception as e:
                st.error(f"Failed to decrease channel: {str(e)}")
    
    with ch_col3:
        channel = st.number_input("Set Channel", 1, 999, 1, key=f"channel_{device_id}")
        if st.button("Set Channel", key=f"setch_{device_id}"):
            try:
                api.tv_set_channel(device_id, channel)
                st.success(f"Channel set to {channel}!")
            except Exception as e:
                st.error(f"Failed to set channel: {str(e)}")
    
    st.divider()

def display_ac_controls(device_data, api):
    """Display AC control interface"""
    device_name = device_data.get('deviceName', 'Unknown AC')
    device_id = device_data.get('deviceId', 'N/A')
    
    st.subheader(f"❄️ {device_name}")
    
    # Power control
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔌 Power", key=f"ac_power_{device_id}"):
            try:
                api.ac_power(device_id)
                st.success("AC power command sent!")
            except Exception as e:
                st.error(f"Failed to send AC power command: {str(e)}")
    
    with col2:
        if st.button("🔄 Refresh Status", key=f"ac_refresh_{device_id}"):
            st.rerun()
    
    # Temperature control
    st.write("**Temperature Control**")
    temp_col1, temp_col2 = st.columns(2)
    
    with temp_col1:
        temperature = st.slider("Set Temperature", 16, 30, 25, key=f"temp_{device_id}")
        if st.button("Set Temperature", key=f"settemp_{device_id}"):
            try:
                api.ac_set_temperature(device_id, temperature)
                st.success(f"Temperature set to {temperature}°C!")
            except Exception as e:
                st.error(f"Failed to set temperature: {str(e)}")
    
    with temp_col2:
        mode = st.selectbox("Set Mode", ["cool", "heat", "auto", "fan", "dry"], key=f"mode_{device_id}")
        if st.button("Set Mode", key=f"setmode_{device_id}"):
            try:
                api.ac_set_mode(device_id, mode)
                st.success(f"Mode set to {mode}!")
            except Exception as e:
                st.error(f"Failed to set mode: {str(e)}")
    
    st.divider()

def display_light_controls(device_data, api):
    """Display light control interface"""
    device_name = device_data.get('deviceName', 'Unknown Light')
    device_id = device_data.get('deviceId', 'N/A')
    
    st.subheader(f"💡 {device_name}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Turn On", key=f"light_on_{device_id}"):
            try:
                api.turn_on_device(device_id)
                st.success("Light turned on!")
            except Exception as e:
                st.error(f"Failed to turn on light: {str(e)}")
    
    with col2:
        if st.button("💡 Turn Off", key=f"light_off_{device_id}"):
            try:
                api.turn_off_device(device_id)
                st.success("Light turned off!")
            except Exception as e:
                st.error(f"Failed to turn off light: {str(e)}")
    
    with col3:
        if st.button("🔄 Refresh", key=f"light_refresh_{device_id}"):
            st.rerun()
    
    st.divider()

def main():
    st.title("📺 SwitchBot Device Controller")
    st.markdown("Control your SwitchBot devices including TVs, ACs, and lights")
    
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
    col1, col2 = st.columns([3, 1])
    with col1:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
    with col2:
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
        
        # Categorize devices
        tv_devices = []
        ac_devices = []
        light_devices = []
        other_devices = []
        
        # Physical devices
        for device in devices:
            device_type = device.get('deviceType', '')
            if 'TV' in device_type or 'Television' in device_type:
                tv_devices.append(device)
            elif 'AC' in device_type or 'AirConditioner' in device_type:
                ac_devices.append(device)
            elif 'Light' in device_type or 'Bulb' in device_type:
                light_devices.append(device)
            else:
                other_devices.append(device)
        
        # Infrared remote devices
        try:
            infrared_remotes = api.get_infrared_remotes()
            for remote in infrared_remotes:
                remote_type = remote.get('remoteType', '')
                if remote_type == 'TV':
                    tv_devices.append(remote)
                elif remote_type == 'Air Conditioner':
                    ac_devices.append(remote)
                elif remote_type == 'Light':
                    light_devices.append(remote)
                else:
                    other_devices.append(remote)
        except Exception as e:
            st.warning(f"仮想IRリモコンの取得に失敗しました: {str(e)}")
        
        # Display TV devices
        if tv_devices:
            st.header("📺 TV Devices")
            for device in tv_devices:
                display_tv_controls(device, api)
        
        # Display AC devices
        if ac_devices:
            st.header("❄️ AC Devices")
            for device in ac_devices:
                display_ac_controls(device, api)
        
        # Display Light devices
        if light_devices:
            st.header("💡 Light Devices")
            for device in light_devices:
                display_light_controls(device, api)
        
        # Display other devices
        if other_devices:
            st.header("🔧 Other Devices")
            for device in other_devices:
                device_name = device.get('deviceName', 'Unknown Device')
                device_type = device.get('deviceType', 'Unknown Type')
                device_id = device.get('deviceId', 'N/A')
                
                st.write(f"**{device_name}** ({device_type})")
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔌 Turn On", key=f"other_on_{device_id}"):
                        try:
                            api.turn_on_device(device_id)
                            st.success("Device turned on!")
                        except Exception as e:
                            st.error(f"Failed to turn on device: {str(e)}")
                
                with col2:
                    if st.button("🔌 Turn Off", key=f"other_off_{device_id}"):
                        try:
                            api.turn_off_device(device_id)
                            st.success("Device turned off!")
                        except Exception as e:
                            st.error(f"Failed to turn off device: {str(e)}")
                
                st.divider()
        
        # Display device summary
        st.sidebar.header("📊 Device Summary")
        st.sidebar.write(f"📺 TVs: {len(tv_devices)}")
        st.sidebar.write(f"❄️ ACs: {len(ac_devices)}")
        st.sidebar.write(f"💡 Lights: {len(light_devices)}")
        st.sidebar.write(f"🔧 Others: {len(other_devices)}")
        st.sidebar.write(f"📱 Total: {len(devices)}")
    
    except Exception as e:
        st.error(f"Failed to fetch device data: {str(e)}")
        st.markdown("""
        **Possible issues:**
        - Check your internet connection
        - Verify your API credentials are correct
        - Ensure your SwitchBot devices are online and connected
        - Check if you've exceeded API rate limits
        """)

if __name__ == "__main__":
    main() 