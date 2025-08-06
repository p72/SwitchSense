#!/usr/bin/env python3
"""
SwitchBotデバイス情報デバッグスクリプト
🔍 デバイスの詳細情報を確認します〜！
"""

import os
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

def main():
    print("🔍 SwitchBotデバイス情報を確認します...")
    print("=" * 50)
    
    # 環境変数を読み込み
    load_dotenv()
    
    # API認証情報を取得
    token = os.getenv("SWITCHBOT_TOKEN")
    secret = os.getenv("SWITCHBOT_SECRET")
    
    if not token or not secret:
        print("❌ SwitchBot API認証情報が見つかりません")
        print("   .envファイルに認証情報を設定してください")
        return
    
    # APIクライアントを初期化
    api = SwitchBotAPI(token, secret)
    
    try:
        # デバイス一覧を取得
        print("📱 デバイス一覧を取得中...")
        devices = api.get_devices()
        
        if not devices:
            print("❌ デバイスが見つかりません")
            return
        
        print(f"✅ {len(devices)}個のデバイスが見つかりました")
        print()
        
        # デバイス情報を詳細表示
        for i, device in enumerate(devices, 1):
            print(f"📱 デバイス {i}:")
            print(f"   名前: {device.get('deviceName', 'N/A')}")
            print(f"   ID: {device.get('deviceId', 'N/A')}")
            print(f"   タイプ: {device.get('deviceType', 'N/A')}")
            print(f"   モデル: {device.get('deviceModel', 'N/A')}")
            print(f"   オンライン: {device.get('online', 'N/A')}")
            print(f"   制御可能: {device.get('controllable', 'N/A')}")
            print(f"   設定可能: {device.get('configurable', 'N/A')}")
            print()
        
        # デバイスタイプ別に分類
        print("📊 デバイスタイプ別分類:")
        device_types = {}
        for device in devices:
            device_type = device.get('deviceType', 'Unknown')
            if device_type not in device_types:
                device_types[device_type] = []
            device_types[device_type].append(device)
        
        for device_type, devices_list in device_types.items():
            print(f"   {device_type}: {len(devices_list)}個")
            for device in devices_list:
                print(f"     - {device.get('deviceName', 'N/A')}")
        
        print()
        print("💡 ヒント:")
        print("   - テレビデバイスは 'TV' または 'Television' を含むタイプです")
        print("   - エアコンデバイスは 'AC' または 'AirConditioner' を含むタイプです")
        print("   - 照明デバイスは 'Light' または 'Bulb' を含むタイプです")
        print("   - デバイスがオンラインでない場合、操作できません")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 