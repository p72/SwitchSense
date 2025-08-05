#!/usr/bin/env python3
"""
SwitchBot Temperature Monitor 起動スクリプト
🌡️ 簡単にアプリを起動できます〜！
"""

import subprocess
import sys
import os
from dotenv import load_dotenv

def main():
    print("🌡️ SwitchBot Temperature Monitor を起動します〜！")
    print("=" * 50)
    
    # .envファイルを読み込み
    try:
        load_dotenv()
        print("✅ .envファイルを読み込みました〜！")
        
        # 環境変数が設定されているかチェック
        token = os.getenv("SWITCHBOT_TOKEN")
        secret = os.getenv("SWITCHBOT_SECRET")
        
        if token == "your_token_here" or secret == "your_secret_here":
            print("⚠️ .envファイルの認証情報を実際の値に設定してください〜！")
            print("SwitchBotアプリの設定 → アプリバージョン → 開発者オプションから取得してください")
        else:
            print("✅ 認証情報が設定されています〜！")
            
    except Exception as e:
        print(f"⚠️ .envファイルの読み込みに失敗しました: {e}")
        print("SwitchBotのAPI認証情報を設定してください〜！")
        return
    
    # Streamlitアプリを起動
    try:
        print("🚀 Streamlitアプリを起動中...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 アプリを終了しました〜！")
    except subprocess.CalledProcessError as e:
        print(f"❌ アプリの起動に失敗しました: {e}")
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main() 