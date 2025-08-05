#!/bin/bash

# SwitchBot Temperature Monitor 起動スクリプト
# 🌡️ デスクトップから簡単に起動できます〜！

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境をアクティベート
source .venv/bin/activate

# 環境変数を読み込み
if [ -f .env ]; then
    echo "✅ .envファイルを読み込みました〜！"
else
    echo "⚠️ .envファイルが見つかりません。"
    echo "SwitchBotのAPI認証情報を設定してください〜！"
    read -p "続行しますか？ (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Streamlitアプリを起動
echo "🚀 SwitchBot Temperature Monitor を起動中..."
echo "URL: http://localhost:8501"
echo "終了するには Ctrl+C を押してください"
echo ""

python -m streamlit run app.py --server.port 8501 