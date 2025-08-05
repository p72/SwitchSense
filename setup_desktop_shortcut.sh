#!/bin/bash

# デスクトップショートカットを作成する最も簡単な方法
echo "🖥️ SwitchBot Temperature Monitor のデスクトップショートカットを作成します..."

# 現在のディレクトリを取得
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# デスクトップにシンボリックリンクを作成
ln -sf "$CURRENT_DIR/launch_switchsense.sh" ~/Desktop/SwitchSense.command

echo "✅ デスクトップに SwitchSense.command を作成しました！"
echo "🖱️ ダブルクリックでアプリを起動できます〜！"
echo "🌐 ブラウザで http://localhost:8501 にアクセスしてください"
echo ""
echo "📝 使い方："
echo "1. デスクトップの SwitchSense.command をダブルクリック"
echo "2. ターミナルが開いてアプリが起動します"
echo "3. ブラウザで http://localhost:8501 にアクセス"
echo "4. 終了するにはターミナルで Ctrl+C を押してください" 