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
    device_type = device_data.get('deviceType', 'Unknown Type')
    remote_type = device_data.get('remoteType', '')
    
    # デバイス情報を表示
    st.subheader(f"📺 {device_name}")
    st.caption(f"**ID**: {device_id} | **Type**: {device_type}")
    if remote_type:
        st.caption(f"**Remote Type**: {remote_type}")
    
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
    vol_col1, vol_col2 = st.columns(2)
    
    with vol_col1:
        if st.button("🔊 Volume Up", key=f"volup_{device_id}"):
            try:
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "volumeAdd")
                else:
                    api.tv_volume_up(device_id)
                st.success("Volume increased!")
            except Exception as e:
                st.error(f"Failed to increase volume: {str(e)}")
    
    with vol_col2:
        if st.button("🔉 Volume Down", key=f"voldown_{device_id}"):
            try:
                if device_data.get('remoteType'):
                    api.send_infrared_command(device_id, "volumeSub")
                else:
                    api.tv_volume_down(device_id)
                st.success("Volume decreased!")
            except Exception as e:
                st.error(f"Failed to decrease volume: {str(e)}")
    
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
    device_type = device_data.get('deviceType', 'Unknown Type')
    remote_type = device_data.get('remoteType', '')
    
    # デバイス情報を表示
    st.subheader(f"❄️ {device_name}")
    st.caption(f"**ID**: {device_id} | **Type**: {device_type}")
    if remote_type:
        st.caption(f"**Remote Type**: {remote_type}")
    
    # Power control
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔌 Power On", key=f"ac_power_on_{device_id}"):
            try:
                if 'remoteType' in device_data:
                    # 仮想IRリモコンの場合: setAllコマンドで電源ON
                    api.send_infrared_command(device_id, "setAll", "26,1,3,on")
                else:
                    api.ac_power(device_id)
                st.success("AC power ON command sent!")
            except Exception as e:
                st.error(f"Failed to send AC power ON command: {str(e)}")
    
    with col2:
        if st.button("🔌 Power Off", key=f"ac_power_off_{device_id}"):
            try:
                if 'remoteType' in device_data:
                    # 仮想IRリモコンの場合: setAllコマンドで電源OFF
                    api.send_infrared_command(device_id, "setAll", "26,1,3,off")
                else:
                    api.ac_power(device_id)  # 物理デバイスの場合は切り替え
                st.success("AC power OFF command sent!")
            except Exception as e:
                st.error(f"Failed to send AC power OFF command: {str(e)}")
    
    with col3:
        if st.button("🔄 Refresh Status", key=f"ac_refresh_{device_id}"):
            st.rerun()
    
    # Temperature control
    st.write("**Temperature Control**")
    temp_col1, temp_col2 = st.columns(2)
    
    with temp_col1:
        temperature = st.slider("Set Temperature", 16, 30, 25, key=f"temp_{device_id}")
        if st.button("Set Temperature", key=f"settemp_{device_id}"):
            try:
                if 'remoteType' in device_data:
                    # 仮想IRリモコンの場合: setAllコマンドで温度設定
                    api.send_infrared_command(device_id, "setAll", f"{temperature},1,3,on")
                else:
                    api.ac_set_temperature(device_id, temperature)
                st.success(f"Temperature set to {temperature}°C!")
            except Exception as e:
                st.error(f"Failed to set temperature: {str(e)}")
    
    with temp_col2:
        mode = st.selectbox("Set Mode", ["cool", "heat", "auto", "fan", "dry"], key=f"mode_{device_id}")
        if st.button("Set Mode", key=f"setmode_{device_id}"):
            try:
                if 'remoteType' in device_data:
                    # 仮想IRリモコンの場合: setAllコマンドでモード設定
                    mode_map = {"auto": 1, "cool": 2, "dry": 3, "fan": 4, "heat": 5}
                    mode_value = mode_map.get(mode, 1)
                    api.send_infrared_command(device_id, "setAll", f"26,{mode_value},3,on")
                else:
                    api.ac_set_mode(device_id, mode)
                st.success(f"Mode set to {mode}!")
            except Exception as e:
                st.error(f"Failed to set mode: {str(e)}")
    
    st.divider()

def display_light_controls(device_data, api):
    """Display light control interface"""
    device_name = device_data.get('deviceName', 'Unknown Light')
    device_id = device_data.get('deviceId', 'N/A')
    device_type = device_data.get('deviceType', 'Unknown Type')
    remote_type = device_data.get('remoteType', '')
    
    # デバイス情報を表示
    st.subheader(f"💡 {device_name}")
    st.caption(f"**ID**: {device_id} | **Type**: {device_type}")
    if remote_type:
        st.caption(f"**Remote Type**: {remote_type}")
    
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

def display_thermometer_controls(device_data, api):
    """Display thermometer interface with temperature, humidity, and battery"""
    device_name = device_data.get('deviceName', 'Unknown Thermometer')
    device_id = device_data.get('deviceId', 'N/A')
    device_type = device_data.get('deviceType', 'Unknown Type')
    
    # デバイス情報を表示
    st.subheader(f"🌡️ {device_name}")
    st.caption(f"**ID**: {device_id} | **Type**: {device_type}")
    
    # 温度単位の選択
    temp_unit = st.radio(
        "温度単位",
        ["摂氏 (°C)", "華氏 (°F)"],
        horizontal=True,
        key=f"temp_unit_{device_id}"
    )
    
    try:
        # デバイス状態を取得
        device_status = api.get_device_status(device_id)
        
        if device_status:
            # 温度と湿度を取得
            temperature = device_status.get('temperature', 0)
            humidity = device_status.get('humidity', 0)
            battery = device_status.get('battery', 0)
            
            # 温度単位を変換
            if temp_unit == "華氏 (°F)":
                temp_display = (temperature * 9/5) + 32
                temp_unit_display = "°F"
            else:
                temp_display = temperature
                temp_unit_display = "°C"
            
            # バッテリー状態の色を取得
            if battery >= 80:
                battery_color = "🟢"
            elif battery >= 50:
                battery_color = "🟡"
            elif battery >= 20:
                battery_color = "🟠"
            else:
                battery_color = "🔴"
            
            # データをカード形式で表示
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="🌡️ 温度",
                    value=f"{temp_display:.1f}{temp_unit_display}",
                    delta=None
                )
            
            with col2:
                st.metric(
                    label="💧 湿度",
                    value=f"{humidity}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    label=f"{battery_color} バッテリー",
                    value=f"{battery}%",
                    delta=None
                )
            
            # 更新時刻を表示
            st.caption(f"📅 最終更新: {datetime.now().strftime('%H:%M:%S')}")
            
        else:
            st.warning("❌ デバイス状態を取得できませんでした")
            
    except Exception as e:
        st.error(f"デバイス状態の取得に失敗: {str(e)}")
    
    # 手動更新ボタン
    if st.button("🔄 手動更新", key=f"thermo_refresh_{device_id}"):
        st.rerun()
    
    st.divider()

def display_hub_info(device_data):
    """Display Hub device information (no controls)"""
    device_name = device_data.get('deviceName', 'Unknown Hub')
    device_id = device_data.get('deviceId', 'N/A')
    device_type = device_data.get('deviceType', 'Unknown Type')
    
    # デバイス情報を表示（操作ボタンなし）
    st.subheader(f"🔧 {device_name}")
    st.caption(f"**ID**: {device_id} | **Type**: {device_type}")
    st.info("ℹ️ このデバイスは操作対象外です（Hub Mini）")
    
    st.divider()

def main():
    st.title("📺 SwitchBot Device Controller")
    st.markdown("Control your SwitchBot devices including TVs, ACs, lights, and thermometers")
    
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
        thermometer_devices = []
        hub_devices = []
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
            elif 'Meter' in device_type:  # Meter, MeterPlus, Outdoor Meter など
                thermometer_devices.append(device)
            elif 'Hub Mini' in device_type:
                # Hub Miniは情報表示のみ
                hub_devices.append(device)
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
        
        # Display Thermometer devices
        if thermometer_devices:
            st.header("🌡️ Thermometer Devices")
            for device in thermometer_devices:
                display_thermometer_controls(device, api)
        
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
        
        # Display Hub devices (info only)
        if hub_devices:
            st.header("🔧 Hub Devices")
            for device in hub_devices:
                display_hub_info(device)
        
        # Display other devices
        if other_devices:
            st.header("🔧 Other Devices")
            for device in other_devices:
                device_name = device.get('deviceName', 'Unknown Device')
                device_type = device.get('deviceType', 'Unknown Type')
                device_id = device.get('deviceId', 'N/A')
                
                st.write(f"**{device_name}** ({device_type})")
                st.caption(f"**ID**: {device_id}")
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
        st.sidebar.write(f"🌡️ Thermometers: {len(thermometer_devices)}")
        st.sidebar.write(f"📺 TVs: {len(tv_devices)}")
        st.sidebar.write(f"❄️ ACs: {len(ac_devices)}")
        st.sidebar.write(f"💡 Lights: {len(light_devices)}")
        st.sidebar.write(f"🔧 Hubs: {len(hub_devices)}")
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