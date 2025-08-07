#!/usr/bin/env python3
"""
SwitchBot Monitor - ダッシュボード形式
🏠 統合デバイス管理ダッシュボード
"""

import streamlit as st
import os
from datetime import datetime
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="SwitchBot Monitor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# カスタムCSS
st.markdown("""
<style>
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .device-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .thermometer-card {
        border-left: 4px solid #3498db;
    }
    .tv-card {
        border-left: 4px solid #e74c3c;
    }
    .ac-card {
        border-left: 4px solid #2ecc71;
    }
    .light-card {
        border-left: 4px solid #f39c12;
    }
    .hub-card {
        border-left: 4px solid #9b59b6;
    }
    .other-card {
        border-left: 4px solid #95a5a6;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0.5rem 0;
    }
    .button-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton > button {
        width: 100%;
        font-size: 0.8rem;
        padding: 0.3rem 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def display_summary_cards(devices_summary):
    """サマリーカードを表示"""
    st.markdown("## 📊 デバイス概要")
    
    # シンプルなテキスト表示
    summary_text = []
    for device_type, info in devices_summary.items():
        count_text = f"{info['icon']} {device_type}: {info['count']}台"
        if info.get('status'):
            # 温度の平均値を抽出
            status_text = info['status']
            if '平均:' in status_text:
                avg_temp = status_text.split('平均:')[1].split('°C')[0].strip()
                count_text += f" (平均: {avg_temp}°C)"
        summary_text.append(count_text)
    
    # カンマ区切りで表示
    st.write(" | ".join(summary_text))

def display_thermometer_card(device, api):
    """温度計カードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    
    try:
        device_status = api.get_device_status(device_id)
        if device_status:
            temperature = device_status.get('temperature', 0)
            humidity = device_status.get('humidity', 0)
            battery = device_status.get('battery', 0)
            
            # バッテリー状態の色を取得
            if battery >= 80:
                battery_color = "🟢"
            elif battery >= 50:
                battery_color = "🟡"
            elif battery >= 20:
                battery_color = "🟠"
            else:
                battery_color = "🔴"
            
            st.markdown(f"""
            <div class="device-card thermometer-card">
                <h4>🌡️ {device_name}</h4>
                <div class="metric-row">
                    <span><strong>{temperature:.1f}°C</strong></span>
                    <span>💧 {humidity}%</span>
                    <span>{battery_color} {battery}%</span>
                </div>
                <small>ID: {device_id}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="device-card thermometer-card">
                <h4>🌡️ {device_name}</h4>
                <p>❌ データ取得エラー</p>
                <small>ID: {device_id}</small>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
        <div class="device-card thermometer-card">
            <h4>🌡️ {device_name}</h4>
            <p>❌ エラー: {str(e)}</p>
            <small>ID: {device_id}</small>
        </div>
        """, unsafe_allow_html=True)

def display_tv_card(device, api):
    """テレビカードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    remote_type = device.get('remoteType', '')
    
    # デバイスタイプを判定
    is_virtual_ir = bool(remote_type)
    device_category = "🔌 物理デバイス" if not is_virtual_ir else "🌐 仮想IRデバイス"
    
    st.markdown(f"""
    <div class="device-card tv-card">
        <h4>📺 {device_name}</h4>
        <small>ID: {device_id} | {device_category}</small>
        {f'<small>Remote Type: {remote_type}</small>' if remote_type else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # ボタングリッド
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔌 電源", key=f"tv_power_{device_id}"):
            try:
                if remote_type:
                    api.send_infrared_command(device_id, "turnOn")
                else:
                    api.tv_power(device_id)
                st.success("電源操作完了！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")
    
    with col2:
        if st.button("🔊 音量+", key=f"tv_vol_up_{device_id}"):
            try:
                if remote_type:
                    api.send_infrared_command(device_id, "volumeAdd")
                else:
                    api.tv_volume_up(device_id)
                st.success("音量アップ！")
            except Exception as e:
                st.error(f"音量操作エラー: {str(e)}")
    
    with col3:
        if st.button("🔉 音量-", key=f"tv_vol_down_{device_id}"):
            try:
                if remote_type:
                    api.send_infrared_command(device_id, "volumeSub")
                else:
                    api.tv_volume_down(device_id)
                st.success("音量ダウン！")
            except Exception as e:
                st.error(f"音量操作エラー: {str(e)}")
    
    with col4:
        if st.button("📺 CH+", key=f"tv_ch_up_{device_id}"):
            try:
                api.tv_channel_up(device_id)
                st.success("チャンネルアップ！")
            except Exception as e:
                st.error(f"チャンネル操作エラー: {str(e)}")
    
    with col5:
        if st.button("📺 CH-", key=f"tv_ch_down_{device_id}"):
            try:
                api.tv_channel_down(device_id)
                st.success("チャンネルダウン！")
            except Exception as e:
                st.error(f"チャンネル操作エラー: {str(e)}")

def display_ac_card(device, api):
    """エアコンカードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    remote_type = device.get('remoteType', '')
    
    # デバイスタイプを判定
    is_virtual_ir = bool(remote_type)
    device_category = "🔌 物理デバイス" if not is_virtual_ir else "🌐 仮想IRデバイス"
    
    st.markdown(f"""
    <div class="device-card ac-card">
        <h4>❄️ {device_name}</h4>
        <small>ID: {device_id} | {device_category}</small>
        {f'<small>Remote Type: {remote_type}</small>' if remote_type else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # 仮想IRエアコンの場合は専用UIを表示
    if is_virtual_ir:
        display_virtual_ac_card(device, api)
    else:
        # 物理デバイスの場合は従来のUI
        display_physical_ac_card(device, api)

def display_virtual_ac_card(device, api):
    """仮想IRエアコン専用カードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    
    # 設定UI（4つのカラム）
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**🌡️ 温度設定**")
        st.markdown("16°C - 30°C")
        temp = st.slider("温度", 16, 30, 26, key=f"ac_temp_{device_id}", label_visibility="collapsed")
        st.markdown(f"**{temp}°C**")
    
    with col2:
        st.markdown("**🔄 モード**")
        st.markdown("運転モード選択")
        mode = st.selectbox("モード", 
            ["auto", "cool", "dry", "fan", "heat"], 
            key=f"ac_mode_{device_id}", label_visibility="collapsed")
        mode_display = {"auto": "🔄 自動", "cool": "❄️ 冷房", "dry": "💧 除湿", "fan": "🌪️ 送風", "heat": "🔥 暖房"}
        st.markdown(f"**{mode_display.get(mode, mode)}**")
    
    with col3:
        st.markdown("**🌪️ ファン**")
        st.markdown("風量設定")
        fan = st.selectbox("ファン", 
            ["auto", "low", "medium", "high"], 
            key=f"ac_fan_{device_id}", label_visibility="collapsed")
        fan_display = {"auto": "🔄 自動", "low": "💨 弱風", "medium": "🌪️ 中風", "high": "💨 強風"}
        st.markdown(f"**{fan_display.get(fan, fan)}**")
    
    with col4:
        st.markdown("**🔌 電源**")
        st.markdown("電源状態")
        power = st.selectbox("電源", ["on", "off"], key=f"ac_power_{device_id}", label_visibility="collapsed")
        power_display = {"on": "🔌 ON", "off": "🔌 OFF"}
        st.markdown(f"**{power_display.get(power, power)}**")
    
    # 統合実行ボタン
    st.markdown("---")
    col_center = st.columns([1, 2, 1])[1]
    with col_center:
        if st.button("🎯 設定実行", key=f"ac_set_all_{device_id}", use_container_width=True):
            try:
                # モードとファンのマッピング
                mode_map = {"auto": 1, "cool": 2, "dry": 3, "fan": 4, "heat": 5}
                fan_map = {"auto": 1, "low": 2, "medium": 3, "high": 4}
                
                mode_value = mode_map.get(mode, 1)
                fan_value = fan_map.get(fan, 1)
                
                # setAllコマンドを構築
                command = f"{temp},{mode_value},{fan_value},{power}"
                api.send_infrared_command(device_id, "setAll", command)
                
                # 成功メッセージ
                mode_name = {"auto": "自動", "cool": "冷房", "dry": "除湿", "fan": "送風", "heat": "暖房"}
                fan_name = {"auto": "自動", "low": "弱風", "medium": "中風", "high": "強風"}
                power_name = {"on": "ON", "off": "OFF"}
                
                st.success(f"✅ 設定完了！温度:{temp}°C モード:{mode_name.get(mode, mode)} ファン:{fan_name.get(fan, fan)} 電源:{power_name.get(power, power)}")
                
                # 現在設定表示
                with st.expander("📋 設定詳細", expanded=False):
                    st.markdown(f"**setAll コマンド:** `{command}`")
                    st.markdown(f"**温度:** {temp}°C")
                    st.markdown(f"**モード:** {mode_name.get(mode, mode)} (値: {mode_value})")
                    st.markdown(f"**ファン:** {fan_name.get(fan, fan)} (値: {fan_value})")
                    st.markdown(f"**電源:** {power_name.get(power, power)}")
                    
            except Exception as e:
                st.error(f"❌ 設定エラー: {str(e)}")
    
    # 説明テキスト
    st.markdown("---")
    st.markdown("💡 **仮想IRエアコンは温度・モード・ファン・電源を一括で設定します**")
    st.markdown("🎯 **「設定実行」ボタンで全ての設定を同時に送信します**")

def display_physical_ac_card(device, api):
    """物理エアコンデバイス用カードを表示"""
    device_id = device.get('deviceId', 'N/A')
    
    # 電源制御
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔌 ON", key=f"ac_on_{device_id}"):
            try:
                api.ac_power(device_id)
                st.success("エアコンON！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")
    
    with col2:
        if st.button("🔌 OFF", key=f"ac_off_{device_id}"):
            try:
                api.ac_power(device_id)
                st.success("エアコンOFF！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")
    
    # 温度・モード制御
    col3, col4 = st.columns(2)
    with col3:
        temp = st.slider("温度", 16, 30, 25, key=f"ac_temp_{device_id}")
        if st.button("🌡️ 設定", key=f"ac_set_temp_{device_id}"):
            try:
                api.ac_set_temperature(device_id, temp)
                st.success(f"温度設定: {temp}°C！")
            except Exception as e:
                st.error(f"温度設定エラー: {str(e)}")
    
    with col4:
        mode = st.selectbox("モード", ["auto", "cool", "heat", "fan", "dry"], key=f"ac_mode_{device_id}")
        if st.button("🔄 設定", key=f"ac_set_mode_{device_id}"):
            try:
                api.ac_set_mode(device_id, mode)
                st.success(f"モード設定: {mode}！")
            except Exception as e:
                st.error(f"モード設定エラー: {str(e)}")

def display_light_card(device, api):
    """照明カードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    remote_type = device.get('remoteType', '')
    
    # デバイスタイプを判定
    is_virtual_ir = bool(remote_type)
    device_category = "🔌 物理デバイス" if not is_virtual_ir else "🌐 仮想IRデバイス"
    
    st.markdown(f"""
    <div class="device-card light-card">
        <h4>💡 {device_name}</h4>
        <small>ID: {device_id} | {device_category}</small>
        {f'<small>Remote Type: {remote_type}</small>' if remote_type else ''}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 ON", key=f"light_on_{device_id}"):
            try:
                if remote_type:
                    api.send_infrared_command(device_id, "turnOn")
                else:
                    api.turn_on_device(device_id)
                st.success("照明ON！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")
    
    with col2:
        if st.button("💡 OFF", key=f"light_off_{device_id}"):
            try:
                if remote_type:
                    api.send_infrared_command(device_id, "turnOff")
                else:
                    api.turn_off_device(device_id)
                st.success("照明OFF！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")

def display_hub_card(device):
    """Hubカードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    
    st.markdown(f"""
    <div class="device-card hub-card">
        <h4>🔧 {device_name}</h4>
        <p>ℹ️ 操作対象外デバイス</p>
        <small>ID: {device_id} | 🔌 物理デバイス</small>
    </div>
    """, unsafe_allow_html=True)

def display_other_card(device, api):
    """その他デバイスカードを表示"""
    device_name = device.get('deviceName', 'Unknown')
    device_id = device.get('deviceId', 'N/A')
    device_type = device.get('deviceType', 'Unknown')
    remote_type = device.get('remoteType', '')
    
    # デバイスタイプを判定
    is_virtual_ir = bool(remote_type)
    device_category = "🔌 物理デバイス" if not is_virtual_ir else "🌐 仮想IRデバイス"
    
    st.markdown(f"""
    <div class="device-card other-card">
        <h4>🔧 {device_name}</h4>
        <small>Type: {device_type} | ID: {device_id} | {device_category}</small>
        {f'<small>Remote Type: {remote_type}</small>' if remote_type else ''}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔌 ON", key=f"other_on_{device_id}"):
            try:
                api.turn_on_device(device_id)
                st.success("デバイスON！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")
    
    with col2:
        if st.button("🔌 OFF", key=f"other_off_{device_id}"):
            try:
                api.turn_off_device(device_id)
                st.success("デバイスOFF！")
            except Exception as e:
                st.error(f"電源操作エラー: {str(e)}")

def main():
    st.title("🏠 SwitchBot Monitor")
    st.markdown("統合デバイス管理ダッシュボード")
    
    # 公式ドキュメントへのリンク
    st.markdown("---")
    st.markdown("📖 **参考資料**: [SwitchBot API 公式ドキュメント](https://github.com/OpenWonderLabs/SwitchBotAPI)")
    st.markdown("---")
    
    # API認証情報を取得
    token = os.getenv("SWITCHBOT_TOKEN")
    secret = os.getenv("SWITCHBOT_SECRET")
    
    if not token or not secret:
        st.error("⚠️ SwitchBot API認証情報が見つかりません！")
        st.markdown("""
        `.env`ファイルに以下の認証情報を設定してください：
        - `SWITCHBOT_TOKEN`: SwitchBot APIトークン
        - `SWITCHBOT_SECRET`: SwitchBot APIシークレット
        """)
        return
    
    # APIクライアントを初期化
    api = SwitchBotAPI(token, secret)
    
    # 更新ボタン
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"📅 最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        if st.button("🔄 全体更新"):
            st.rerun()
    
    try:
        with st.spinner("デバイス情報を取得中..."):
            devices = api.get_devices()
            
        if not devices:
            st.warning("デバイスが見つかりません")
            return
        
        # デバイスを分類
        thermometer_devices = []
        tv_devices = []
        ac_devices = []
        light_devices = []
        hub_devices = []
        other_devices = []
        
        # 物理デバイスを分類
        for device in devices:
            device_type = device.get('deviceType', '')
            if 'Meter' in device_type:
                thermometer_devices.append(device)
            elif 'TV' in device_type or 'Television' in device_type:
                tv_devices.append(device)
            elif 'AC' in device_type or 'AirConditioner' in device_type:
                ac_devices.append(device)
            elif 'Light' in device_type or 'Bulb' in device_type:
                light_devices.append(device)
            elif 'Hub Mini' in device_type:
                hub_devices.append(device)
            else:
                other_devices.append(device)
        
        # 仮想IRリモコンを分類
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
            st.warning(f"仮想IRリモコンの取得に失敗: {str(e)}")
        
        # サマリー情報を計算
        devices_summary = {}
        
        if thermometer_devices:
            # 温度の平均を計算
            total_temp = 0
            temp_count = 0
            for device in thermometer_devices:
                try:
                    device_status = api.get_device_status(device['deviceId'])
                    if device_status and device_status.get('temperature'):
                        total_temp += device_status['temperature']
                        temp_count += 1
                except:
                    pass
            
            avg_temp = total_temp / temp_count if temp_count > 0 else 0
            devices_summary['温度計'] = {
                'icon': '🌡️',
                'count': len(thermometer_devices),
                'status': f'<p>平均: {avg_temp:.1f}°C</p>' if temp_count > 0 else ''
            }
        
        if tv_devices:
            devices_summary['テレビ'] = {
                'icon': '📺',
                'count': len(tv_devices)
            }
        
        if ac_devices:
            devices_summary['エアコン'] = {
                'icon': '❄️',
                'count': len(ac_devices)
            }
        
        if light_devices:
            devices_summary['照明'] = {
                'icon': '💡',
                'count': len(light_devices)
            }
        
        if hub_devices:
            devices_summary['Hub'] = {
                'icon': '🔧',
                'count': len(hub_devices)
            }
        
        if other_devices:
            devices_summary['その他'] = {
                'icon': '🔧',
                'count': len(other_devices)
            }
        
        # サマリーカードを表示
        if devices_summary:
            display_summary_cards(devices_summary)
        
        # デバイスグリッドを表示
        st.markdown("## 📱 デバイス一覧")
        
        # 温度計デバイス
        if thermometer_devices:
            st.markdown("### 🌡️ 温度計デバイス")
            cols = st.columns(min(4, len(thermometer_devices)))
            for i, device in enumerate(thermometer_devices):
                with cols[i % len(cols)]:
                    display_thermometer_card(device, api)
        
        # テレビデバイス
        if tv_devices:
            st.markdown("### 📺 テレビデバイス")
            cols = st.columns(min(3, len(tv_devices)))
            for i, device in enumerate(tv_devices):
                with cols[i % len(cols)]:
                    display_tv_card(device, api)
        
        # エアコンデバイス
        if ac_devices:
            st.markdown("### ❄️ エアコンデバイス")
            cols = st.columns(min(3, len(ac_devices)))
            for i, device in enumerate(ac_devices):
                with cols[i % len(cols)]:
                    display_ac_card(device, api)
        
        # 照明デバイス
        if light_devices:
            st.markdown("### 💡 照明デバイス")
            cols = st.columns(min(3, len(light_devices)))
            for i, device in enumerate(light_devices):
                with cols[i % len(cols)]:
                    display_light_card(device, api)
        
        # Hubデバイス
        if hub_devices:
            st.markdown("### 🔧 Hubデバイス")
            cols = st.columns(min(4, len(hub_devices)))
            for i, device in enumerate(hub_devices):
                with cols[i % len(cols)]:
                    display_hub_card(device)
        
        # その他デバイス
        if other_devices:
            st.markdown("### 🔧 その他デバイス")
            cols = st.columns(min(3, len(other_devices)))
            for i, device in enumerate(other_devices):
                with cols[i % len(cols)]:
                    display_other_card(device, api)
    
    except Exception as e:
        st.error(f"デバイス情報の取得に失敗: {str(e)}")
        st.markdown("""
        **考えられる原因:**
        - インターネット接続を確認
        - API認証情報が正しいか確認
        - デバイスがオンラインか確認
        - API制限に達していないか確認
        """)

if __name__ == "__main__":
    main() 