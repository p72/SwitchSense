#!/usr/bin/env python3
"""
仮想IRリモコン情報確認スクリプト
📺 infraredRemoteListの詳細を確認します〜！
"""

import os
import json
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

def main():
    print("📺 仮想IRリモコン情報を確認します...")
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
        # 全デバイス情報を取得
        print("📱 全デバイス情報を取得中...")
        result = api._make_request('/devices')
        
        if not result:
            print("❌ デバイス情報が取得できませんでした")
            return
        
        print("✅ デバイス情報を取得しました")
        print()
        
        # 利用可能なキーを確認
        print("🔍 利用可能なキー:")
        for key in result.keys():
            print(f"   - {key}")
        print()
        
        # infraredRemoteListを確認
        if 'infraredRemoteList' in result:
            infrared_remotes = result['infraredRemoteList']
            print(f"📺 仮想IRリモコン: {len(infrared_remotes)}個")
            print()
            
            for i, remote in enumerate(infrared_remotes, 1):
                print(f"📺 IRリモコン {i}:")
                print(f"   名前: {remote.get('deviceName', 'N/A')}")
                print(f"   ID: {remote.get('deviceId', 'N/A')}")
                print(f"   タイプ: {remote.get('deviceType', 'N/A')}")
                print(f"   モデル: {remote.get('deviceModel', 'N/A')}")
                print(f"   オンライン: {remote.get('online', 'N/A')}")
                print(f"   制御可能: {remote.get('controllable', 'N/A')}")
                print(f"   設定可能: {remote.get('configurable', 'N/A')}")
                
                # 詳細情報があれば表示
                if 'remoteType' in remote:
                    print(f"   リモコンタイプ: {remote.get('remoteType', 'N/A')}")
                if 'hubDeviceId' in remote:
                    print(f"   ハブデバイスID: {remote.get('hubDeviceId', 'N/A')}")
                
                print()
        else:
            print("❌ infraredRemoteListが見つかりません")
            print("💡 仮想IRリモコンが設定されていない可能性があります")
            print()
        
        # deviceListも確認
        if 'deviceList' in result:
            devices = result['deviceList']
            print(f"📱 物理デバイス: {len(devices)}個")
            
            # Hub Miniを探す
            hub_devices = [d for d in devices if d.get('deviceType') == 'Hub Mini']
            if hub_devices:
                print("🔧 Hub Miniデバイス:")
                for hub in hub_devices:
                    print(f"   - {hub.get('deviceName', 'N/A')} (ID: {hub.get('deviceId', 'N/A')})")
                print()
                print("💡 Hub Miniで仮想IRリモコンを設定できます")
                print("   1. SwitchBotアプリを開く")
                print("   2. Hub Miniを選択")
                print("   3. 仮想リモコンを追加")
                print("   4. テレビやエアコンのリモコンを学習")
            else:
                print("❌ Hub Miniデバイスが見つかりません")
        
        print()
        print("📋 全レスポンス情報:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 