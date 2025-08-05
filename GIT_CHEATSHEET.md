# 🐙 Git コマンドチートシート

## 📋 基本的なコマンド

### 初期化・設定
```bash
git init                    # リポジトリを初期化
git clone <url>            # リポジトリをクローン
git config --global user.name "名前"    # ユーザー名を設定
git config --global user.email "メール"  # メールアドレスを設定
```

### 状態確認
```bash
git st                     # ステータス確認（alias）
git status                 # ステータス確認
git log                    # コミット履歴を表示
git log --oneline          # コミット履歴を1行で表示
git last                   # 最新のコミットを表示（alias）
```

### ファイル操作
```bash
git add <ファイル名>        # ファイルをステージング
git add .                  # 全てのファイルをステージング
git rm <ファイル名>         # ファイルを削除
git mv <旧名> <新名>       # ファイル名を変更
```

### コミット
```bash
git ci                     # コミット（alias）
git commit                 # コミット
git commit -m "メッセージ"  # メッセージ付きでコミット
git commit --amend         # 直前のコミットを修正
```

### ブランチ操作
```bash
git br                     # ブランチ一覧表示（alias）
git branch                 # ブランチ一覧表示
git br <ブランチ名>        # ブランチを作成
git co <ブランチ名>        # ブランチを切り替え（alias）
git checkout <ブランチ名>   # ブランチを切り替え
git checkout -b <ブランチ名> # ブランチを作成して切り替え
```

### マージ・リベース
```bash
git merge <ブランチ名>      # ブランチをマージ
git rebase <ブランチ名>     # ブランチをリベース
git rebase --abort         # リベースを中止
```

### リモート操作
```bash
git remote add origin <url> # リモートリポジトリを追加
git push origin <ブランチ名> # プッシュ
git pull origin <ブランチ名> # プル
git fetch origin           # リモートの変更を取得
```

### 変更の取り消し
```bash
git unstage <ファイル名>    # ステージングを取り消し（alias）
git reset HEAD <ファイル名> # ステージングを取り消し
git checkout -- <ファイル名> # ファイルの変更を取り消し
git reset --hard HEAD      # 全ての変更を取り消し
```

## 🎯 便利なエイリアス

| エイリアス | コマンド | 説明 |
|-----------|----------|------|
| `git st` | `git status` | ステータス確認 |
| `git co` | `git checkout` | ブランチ切り替え |
| `git br` | `git branch` | ブランチ一覧 |
| `git ci` | `git commit` | コミット |
| `git unstage` | `git reset HEAD --` | ステージング取り消し |
| `git last` | `git log -1 HEAD` | 最新コミット表示 |

## 📝 コミットメッセージの種類

- **feat**: 新機能
- **fix**: バグ修正
- **docs**: ドキュメントのみの変更
- **style**: コードの意味に影響しない変更
- **refactor**: リファクタリング
- **perf**: パフォーマンス改善
- **test**: テストの追加・修正
- **chore**: ビルドプロセスや補助ツールの変更

## 🔧 トラブルシューティング

### よくある問題と解決方法

1. **コミットを取り消したい**
   ```bash
   git reset --soft HEAD~1  # コミットを取り消し、変更はステージング状態に
   git reset --hard HEAD~1  # コミットを取り消し、変更も削除
   ```

2. **間違ったブランチでコミットしてしまった**
   ```bash
   git cherry-pick <コミットハッシュ>  # 特定のコミットを適用
   ```

3. **マージコンフリクトが発生した**
   ```bash
   git status                    # コンフリクトファイルを確認
   # ファイルを編集してコンフリクトを解決
   git add <ファイル名>          # 解決したファイルを追加
   git commit                    # マージコミットを作成
   ```

4. **リモートの変更を強制的に上書きしたい**
   ```bash
   git push --force origin <ブランチ名>  # 注意: 危険な操作
   ```

## 🎨 カスタマイズ

### 色付きのログ表示
```bash
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

### 差分の表示
```bash
git diff                    # ステージングされていない変更
git diff --staged          # ステージングされた変更
git diff HEAD~1            # 直前のコミットとの差分
```

---

**使用した生成AIモデル**: Claude Sonnet 4 