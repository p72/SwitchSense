# 🌡️ SwitchBot Temperature Monitor

SwitchBotの温度計デバイスをモニタリングするStreamlitアプリやで〜！✨

## 📋 機能

- 🌡️ リアルタイム温度表示（摂氏・華氏）
- 💧 湿度表示
- 🔋 バッテリー残量表示
- 🔄 自動更新機能
- 📱 美しいWebインターフェース

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
# 仮想環境を使用
source .venv/bin/activate

# 依存関係をインストール
pip install requests streamlit python-dotenv
```

### 2. SwitchBot API認証情報の設定

1. **SwitchBotアプリ**を開く 📱
2. **設定 → アプリバージョン → 開発者オプション**に進む
3. **Open Token**と**Secret Key**を取得

### 3. 環境変数の設定

`.env`ファイルを編集して、実際の認証情報を設定してください：

```bash
# .env
SWITCHBOT_TOKEN=あなたの実際のトークン
SWITCHBOT_SECRET=あなたの実際のシークレット
```

## 🎮 アプリの起動

### 方法1: 簡単起動スクリプト（推奨）

```bash
python run_app.py
```

### 方法2: 直接起動

```bash
streamlit run app.py --server.port 8501
```

## 📁 ファイル構成

```
SwitchSense/
├── app.py              # メインアプリケーション
├── switchbot_api.py    # SwitchBot APIクライアント
├── .env                # 環境変数設定
├── run_app.py          # 起動スクリプト
├── pyproject.toml      # プロジェクト設定
└── README.md           # このファイル
```

## 🔧 トラブルシューティング

### よくある問題

1. **認証情報が見つからない**
   - `.env`ファイルが正しく設定されているか確認
   - SwitchBotアプリでAPI認証情報を取得済みか確認

2. **デバイスが見つからない**
   - SwitchBotデバイスがオンラインか確認
   - 温度計デバイス（Meter、Meter Plus、Outdoor Meter）が登録されているか確認

3. **APIエラー**
   - インターネット接続を確認
   - API認証情報が正しいか確認
   - API制限に達していないか確認

## 🎯 対応デバイス

- SwitchBot Meter
- SwitchBot Meter Plus  
- SwitchBot Outdoor Meter

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**使用した生成AIモデル**: Claude Sonnet 4 