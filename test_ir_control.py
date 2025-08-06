#!/usr/bin/env python3
"""
仮想IRリモコン操作テストスクリプト
🎮 実際にIRリモコンを操作してみます〜！
"""

import os
import time
from switchbot_api import SwitchBotAPI
from dotenv import load_dotenv

def main():
    print("🎮 仮想IRリモコン操作テストを開始します...")
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
        # 仮想IRリモコン一覧を取得
        print("📺 仮想IRリモコン一覧を取得中...")
        infrared_remotes = api.get_infrared_remotes()
        
        if not infrared_remotes:
            print("❌ 仮想IRリモコンが見つかりません")
            return
        
        print(f"✅ {len(infrared_remotes)}個の仮想IRリモコンが見つかりました")
        print()
        
        # 各リモコンの情報を表示
        for i, remote in enumerate(infrared_remotes, 1):
            device_name = remote.get('deviceName', 'Unknown')
            device_id = remote.get('deviceId', 'N/A')
            remote_type = remote.get('remoteType', 'Unknown')
            
            print(f"📺 IRリモコン {i}: {device_name}")
            print(f"   ID: {device_id}")
            print(f"   タイプ: {remote_type}")
            print()
        
        # 操作対象を選択
        print("🎯 操作したいリモコンを選択してください:")
        for i, remote in enumerate(infrared_remotes, 1):
            device_name = remote.get('deviceName', 'Unknown')
            remote_type = remote.get('remoteType', 'Unknown')
            print(f"   {i}. {device_name} ({remote_type})")
        
        try:
            choice = int(input("\n番号を入力してください (1-{}): ".format(len(infrared_remotes))))
            if 1 <= choice <= len(infrared_remotes):
                selected_remote = infrared_remotes[choice - 1]
                device_name = selected_remote.get('deviceName', 'Unknown')
                device_id = selected_remote.get('deviceId', 'N/A')
                remote_type = selected_remote.get('remoteType', 'Unknown')
                
                print(f"\n🎮 選択されたリモコン: {device_name} ({remote_type})")
                print(f"   ID: {device_id}")
                print()
                
                # リモコンタイプ別の操作メニュー
                if remote_type == 'TV':
                    test_tv_controls(api, device_id, device_name)
                elif remote_type == 'Air Conditioner':
                    test_ac_controls(api, device_id, device_name)
                elif remote_type == 'Light':
                    test_light_controls(api, device_id, device_name)
                else:
                    test_generic_controls(api, device_id, device_name)
            else:
                print("❌ 無効な選択です")
        except ValueError:
            print("❌ 数字を入力してください")
        except KeyboardInterrupt:
            print("\n👋 操作をキャンセルしました")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")

def test_tv_controls(api, device_id, device_name):
    """テレビリモコンの操作テスト"""
    print("📺 テレビリモコン操作テスト")
    print("=" * 30)
    
    commands = [
        ("🔌 電源", "turnOn"),
        ("🔊 音量アップ", "volumeAdd"),
        ("🔉 音量ダウン", "volumeSub"),
        ("📺 チャンネルアップ", "channelAdd"),
        ("📺 チャンネルダウン", "channelSub"),
    ]
    
    for i, (name, command) in enumerate(commands, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("\n実行するコマンドを選択してください (1-{}): ".format(len(commands))))
        if 1 <= choice <= len(commands):
            command_name, command = commands[choice - 1]
            print(f"\n🎮 {command_name}を実行中...")
            
            try:
                api.send_infrared_command(device_id, command)
                print(f"✅ {command_name}が正常に送信されました！")
            except Exception as e:
                print(f"❌ {command_name}の送信に失敗しました: {str(e)}")
        else:
            print("❌ 無効な選択です")
    except ValueError:
        print("❌ 数字を入力してください")
    except KeyboardInterrupt:
        print("\n👋 操作をキャンセルしました")

def test_ac_controls(api, device_id, device_name):
    """エアコンリモコンの操作テスト"""
    print("❄️ エアコンリモコン操作テスト")
    print("=" * 30)
    
    commands = [
        ("🔌 電源", "turnOn"),
        ("❄️ 冷房", "setAll"),
        ("🔥 暖房", "setAll"),
        ("🌪️ 送風", "setAll"),
        ("💧 除湿", "setAll"),
    ]
    
    for i, (name, command) in enumerate(commands, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("\n実行するコマンドを選択してください (1-{}): ".format(len(commands))))
        if 1 <= choice <= len(commands):
            command_name, command = commands[choice - 1]
            print(f"\n🎮 {command_name}を実行中...")
            
            try:
                if command == "setAll":
                    # エアコンのモード設定
                    mode = input("モードを入力してください (cool/heat/fan/dry): ")
                    api.send_infrared_command(device_id, command, f"25,25,{mode}")
                else:
                    api.send_infrared_command(device_id, command)
                print(f"✅ {command_name}が正常に送信されました！")
            except Exception as e:
                print(f"❌ {command_name}の送信に失敗しました: {str(e)}")
        else:
            print("❌ 無効な選択です")
    except ValueError:
        print("❌ 数字を入力してください")
    except KeyboardInterrupt:
        print("\n👋 操作をキャンセルしました")

def test_light_controls(api, device_id, device_name):
    """照明リモコンの操作テスト"""
    print("💡 照明リモコン操作テスト")
    print("=" * 30)
    
    commands = [
        ("💡 電源オン", "turnOn"),
        ("💡 電源オフ", "turnOff"),
    ]
    
    for i, (name, command) in enumerate(commands, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("\n実行するコマンドを選択してください (1-{}): ".format(len(commands))))
        if 1 <= choice <= len(commands):
            command_name, command = commands[choice - 1]
            print(f"\n🎮 {command_name}を実行中...")
            
            try:
                api.send_infrared_command(device_id, command)
                print(f"✅ {command_name}が正常に送信されました！")
            except Exception as e:
                print(f"❌ {command_name}の送信に失敗しました: {str(e)}")
        else:
            print("❌ 無効な選択です")
    except ValueError:
        print("❌ 数字を入力してください")
    except KeyboardInterrupt:
        print("\n👋 操作をキャンセルしました")

def test_generic_controls(api, device_id, device_name):
    """汎用リモコンの操作テスト"""
    print("🔧 汎用リモコン操作テスト")
    print("=" * 30)
    
    commands = [
        ("🔌 電源", "turnOn"),
        ("🔌 電源オフ", "turnOff"),
    ]
    
    for i, (name, command) in enumerate(commands, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("\n実行するコマンドを選択してください (1-{}): ".format(len(commands))))
        if 1 <= choice <= len(commands):
            command_name, command = commands[choice - 1]
            print(f"\n🎮 {command_name}を実行中...")
            
            try:
                api.send_infrared_command(device_id, command)
                print(f"✅ {command_name}が正常に送信されました！")
            except Exception as e:
                print(f"❌ {command_name}の送信に失敗しました: {str(e)}")
        else:
            print("❌ 無効な選択です")
    except ValueError:
        print("❌ 数字を入力してください")
    except KeyboardInterrupt:
        print("\n👋 操作をキャンセルしました")

if __name__ == "__main__":
    main() 