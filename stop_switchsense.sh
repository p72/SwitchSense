#!/bin/bash

# SwitchBot Temperature Monitor 停止スクリプト
# 🛑 アプリを安全に停止します〜！

echo "🛑 SwitchBot Temperature Monitor を停止します..."

# ポート8501を使用しているプロセスを検索
PID=$(lsof -ti:8501)

if [ -z "$PID" ]; then
    echo "✅ アプリは既に停止しています"
    exit 0
fi

echo "📋 停止するプロセス: PID $PID"

# プロセスを停止
kill $PID

# 停止を確認
sleep 2
if lsof -ti:8501 > /dev/null 2>&1; then
    echo "⚠️ プロセスが停止しませんでした。強制終了します..."
    kill -9 $PID
    sleep 1
fi

# 最終確認
if lsof -ti:8501 > /dev/null 2>&1; then
    echo "❌ プロセスの停止に失敗しました"
    exit 1
else
    echo "✅ アプリを正常に停止しました！"
    echo "🌐 ポート8501が解放されました"
fi 