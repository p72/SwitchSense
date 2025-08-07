# 🌡️ SwitchBot Temperature Monitor

SwitchBotの温度計デバイスをモニタリングし、リモコン操作もできるStreamlitアプリやで〜！✨

## 🛠️ 開発経緯

**最初に Replitでプロトタイプを作成、その後、Cursorで編集　Claude Sonnet 4で作成**

このプロジェクトは、Replitでプロトタイプを作成し、その後Cursorで本格的な開発を行いました。Claude Sonnet 4を使用して、SwitchBot APIとの連携や美しいUIの実装を行っています。

## 📋 機能

### 🌡️ 温度監視機能
- 🌡️ リアルタイム温度表示（摂氏・華氏）
- 💧 湿度表示
- 🔋 バッテリー残量表示（色分け）
- 🔄 自動更新機能（5-60秒間隔）
- 📱 美しいカード形式のWebインターフェース

### 📺 リモコン操作機能
- 📺 **テレビ制御** - 電源、音量、チャンネル操作
- ❄️ **エアコン制御** - 電源ON/OFF、温度設定、モード変更
- 💡 **照明制御** - 電源、明るさ調整
- 🔧 **その他のデバイス** - 汎用制御

### 🏠 統合管理機能
- 🌡️ **温度計デバイス監視** - リアルタイム温度・湿度・バッテリー表示
- 📱 **デバイス分類** - 自動的にデバイスをカテゴリ別に分類
- 🔄 **リアルタイム更新** - 手動・自動更新機能
- 📊 **デバイス集計** - サイドバーでデバイス数の確認
- 🔧 **Hub Mini表示** - 操作対象外デバイスの情報表示

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

### 🏠 統合ダッシュボード（メイン）

```bash
streamlit run SwitchbotMoniter.py --server.port 8502
```

**URL**: `http://localhost:8502`

## 📁 ファイル構成

```
SwitchSense/
├── SwitchbotMoniter.py     # 🏠 統合ダッシュボード（メイン）
├── switchbot_api.py        # 🔌 SwitchBot APIクライアント
├── test_ir_control.py      # 🎮 IRリモコン操作テスト
├── .env                    # ⚙️ 環境変数設定
├── .gitignore              # 🚫 Git除外設定
├── .gitmessage             # コミットテンプレート
├── pyproject.toml          # ⚙️ プロジェクト設定
├── uv.lock                 # 🔒 依存関係ロック
├── replit.md               # 📖 技術仕様書（英語）
├── replit_ja.md            # 📖 技術仕様書（日本語）
└── README.md               # 📖 このファイル
```

## 🎯 対応デバイス

### 🌡️ 温度監視対応デバイス
- SwitchBot Meter
- SwitchBot Meter Plus  
- SwitchBot Outdoor Meter
- その他のMeter系デバイス

### 📺 リモコン操作対応デバイス
- **物理デバイス**: SwitchBot Bot、SwitchBot Curtain、SwitchBot Light
- **仮想IRリモコン**: テレビ、エアコン、照明（Hub Mini経由）

### 🔧 情報表示デバイス
- **Hub Mini** - 操作対象外、情報表示のみ

## 🔧 トラブルシューティング

### よくある問題

1. **認証情報が見つからない**
   - `.env`ファイルが正しく設定されているか確認
   - SwitchBotアプリでAPI認証情報を取得済みか確認

2. **デバイスが見つからない**
   - SwitchBotデバイスがオンラインか確認
   - 温度計デバイス（Meter、Meter Plus、Outdoor Meter）が登録されているか確認
   - リモコン操作の場合、Hub Miniが設定されているか確認

3. **APIエラー**
   - インターネット接続を確認
   - API認証情報が正しいか確認
   - API制限に達していないか確認

4. **リモコン操作ができない**
   - Hub Miniがオンラインか確認
   - 仮想IRリモコンが正しく設定されているか確認
   - デバイスが制御可能な状態か確認

5. **温度計が表示されない**
   - デバイスタイプが`Meter`系か確認
   - デバイスがオンラインか確認
   - API認証情報が正しいか確認

6. **Hub Miniが表示されない**
   - Hub Miniがオンラインか確認
   - デバイスタイプが`Hub Mini`か確認
   - API認証情報が正しいか確認



### 🎮 IRリモコン操作テスト

```bash
python test_ir_control.py
```

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**使用した生成AIモデル**: Claude Sonnet 4 