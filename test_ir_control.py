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
    
    print("🌡️ 温度設定 (16°C - 30°C)")
    try:
        temp = int(input("温度を入力してください (16-30): "))
        if temp < 16 or temp > 30:
            print("❌ 温度は16-30の範囲で入力してください")
            return
    except ValueError:
        print("❌ 数字を入力してください")
        return
    
    print("\n🔄 モード選択")
    print("1. 🔄 自動 (auto)")
    print("2. ❄️ 冷房 (cool)")
    print("3. 💧 除湿 (dry)")
    print("4. 🌪️ 送風 (fan)")
    print("5. 🔥 暖房 (heat)")
    
    try:
        mode_choice = int(input("モードを選択してください (1-5): "))
        mode_map = {1: "auto", 2: "cool", 3: "dry", 4: "fan", 5: "heat"}
        if mode_choice not in mode_map:
            print("❌ 1-5の数字を入力してください")
            return
        mode = mode_map[mode_choice]
    except ValueError:
        print("❌ 数字を入力してください")
        return
    
    print("\n🌪️ ファン設定")
    print("1. 🔄 自動 (auto)")
    print("2. 💨 弱風 (low)")
    print("3. 🌪️ 中風 (medium)")
    print("4. 💨 強風 (high)")
    
    try:
        fan_choice = int(input("ファンを選択してください (1-4): "))
        fan_map = {1: "auto", 2: "low", 3: "medium", 4: "high"}
        if fan_choice not in fan_map:
            print("❌ 1-4の数字を入力してください")
            return
        fan = fan_map[fan_choice]
    except ValueError:
        print("❌ 数字を入力してください")
        return
    
    print("\n🔌 電源設定")
    print("1. 🔌 ON (on)")
    print("2. 🔌 OFF (off)")
    
    try:
        power_choice = int(input("電源を選択してください (1-2): "))
        power_map = {1: "on", 2: "off"}
        if power_choice not in power_map:
            print("❌ 1-2の数字を入力してください")
            return
        power = power_map[power_choice]
    except ValueError:
        print("❌ 数字を入力してください")
        return
    
    # モードとファンのマッピング（SwitchbotMoniter.pyと同じ）
    mode_value_map = {"auto": 1, "cool": 2, "dry": 3, "fan": 4, "heat": 5}
    fan_value_map = {"auto": 1, "low": 2, "medium": 3, "high": 4}
    
    mode_value = mode_value_map.get(mode, 1)
    fan_value = fan_value_map.get(fan, 1)
    
    # setAllコマンドを構築
    command = f"{temp},{mode_value},{fan_value},{power}"
    
    print(f"\n🎮 設定を実行中...")
    print(f"📋 設定内容:")
    print(f"   温度: {temp}°C")
    print(f"   モード: {mode} (値: {mode_value})")
    print(f"   ファン: {fan} (値: {fan_value})")
    print(f"   電源: {power}")
    print(f"   setAllコマンド: {command}")
    
    try:
        api.send_infrared_command(device_id, "setAll", command)
        print(f"✅ エアコン設定が正常に送信されました！")
    except Exception as e:
        print(f"❌ エアコン設定の送信に失敗しました: {str(e)}")

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