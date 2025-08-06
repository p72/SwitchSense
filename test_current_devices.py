#!/usr/bin/env python3
"""
現在のSwitchBotデバイスで操作テスト
🧪 既存のデバイスで操作機能をテストします〜！
"""

import os
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

def main():
    print("🧪 現在のデバイスで操作テストを実行します...")
    print("=" * 50)
    
    # 環境変数を読み込み
    load_dotenv()
    
    # API認証情報を取得
    token = os.getenv("SWITCHBOT_TOKEN")
    secret = os.getenv("SWITCHBOT_SECRET")
    
    if not token or not secret:
        print("❌ SwitchBot API認証情報が見つかりません")
        return
    
    # APIクライアントを初期化
    api = SwitchBotAPI(token, secret)
    
    try:
        # デバイス一覧を取得
        devices = api.get_devices()
        
        if not devices:
            print("❌ デバイスが見つかりません")
            return
        
        print(f"✅ {len(devices)}個のデバイスが見つかりました")
        print()
        
        # 各デバイスで操作テスト
        for i, device in enumerate(devices, 1):
            device_name = device.get('deviceName', 'Unknown')
            device_id = device.get('deviceId', 'N/A')
            device_type = device.get('deviceType', 'Unknown')
            
            print(f"📱 デバイス {i}: {device_name} ({device_type})")
            print(f"   ID: {device_id}")
            
            # デバイス状態を取得
            try:
                status = api.get_device_status(device_id)
                print(f"   📊 状態: {status}")
            except Exception as e:
                print(f"   ❌ 状態取得エラー: {str(e)}")
            
            # 操作テスト（Hub Miniは制御可能）
            if device_type == "Hub Mini":
                print("   🔧 Hub Mini - 制御可能なデバイスです")
                print("   💡 このデバイスは他のデバイスを制御するハブです")
            elif device_type in ["Meter", "MeterPlus"]:
                print("   📊 センサーデバイス - 読み取り専用です")
                print("   💡 温度・湿度の監視のみ可能です")
            else:
                print("   ❓ 不明なデバイスタイプ")
            
            print()
        
        print("💡 推奨事項:")
        print("   1. SwitchBotアプリでテレビ、エアコン、照明デバイスを追加")
        print("   2. デバイスがオンラインになっていることを確認")
        print("   3. 赤外線リモコン機能を設定")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 