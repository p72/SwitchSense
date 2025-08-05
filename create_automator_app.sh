#!/bin/bash

# Automatorアプリケーションを作成するスクリプト
# このスクリプトを実行すると、デスクトップにアプリが作成されます

echo "🖥️ SwitchBot Temperature Monitor のデスクトップアプリを作成します..."

# 現在のディレクトリを取得
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Automatorワークフローを作成
cat > /tmp/SwitchSense.workflow << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>AMApplicationBuild</key>
    <string>512</string>
    <key>AMApplicationVersion</key>
    <string>1.0</string>
    <key>AMDocumentVersion</key>
    <string>2</string>
    <key>actions</key>
    <array>
        <dict>
            <key>action</key>
            <dict>
                <key>AMAccepts</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Optional</key>
                    <true/>
                    <key>Types</key>
                    <array>
                        <string>com.apple.applescript.object</string>
                    </array>
                </dict>
                <key>AMActionVersion</key>
                <string>1.0</string>
                <key>AMApplication</key>
                <array>
                    <string>Run Shell Script</string>
                </array>
                <key>AMParameterProperties</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <dict/>
                    <key>CheckedForUserOnly</key>
                    <dict/>
                    <key>inputMethod</key>
                    <dict/>
                    <key>shell</key>
                    <dict/>
                    <key>source</key>
                    <dict/>
                </dict>
                <key>AMProvides</key>
                <dict>
                    <key>Container</key>
                    <string>List</string>
                    <key>Types</key>
                    <array>
                        <string>com.apple.applescript.object</string>
                    </array>
                </dict>
                <key>ActionBundlePath</key>
                <string>/System/Library/Automator/Run Shell Script.action</string>
                <key>ActionName</key>
                <string>Run Shell Script</string>
                <key>ActionParameters</key>
                <dict>
                    <key>COMMAND_STRING</key>
                    <string>cd "$CURRENT_DIR"
source .venv/bin/activate
python -m streamlit run app.py --server.port 8501</string>
                    <key>CheckedForUserOnly</key>
                    <false/>
                    <key>inputMethod</key>
                    <integer>0</integer>
                    <key>shell</key>
                    <string>/bin/bash</string>
                    <key>source</key>
                    <string>COMMAND_STRING</string>
                </dict>
                <key>BundleIdentifier</key>
                <string>com.apple.Automator.RunShellScript</string>
                <key>CFBundleVersion</key>
                <string>1.0</string>
                <key>CanShowSelectedItemsWhenRun</key>
                <false/>
                <key>CanShowWhenRun</key>
                <true/>
                <key>Category</key>
                <array>
                    <string>AMCategoryUtilities</string>
                </array>
                <key>Class Name</key>
                <string>AMRunShellScriptAction</string>
                <key>InputUUID</key>
                <string>B5A0C8C0-8B8B-4B8B-8B8B-8B8B8B8B8B8B</string>
                <key>Keywords</key>
                <array>
                    <string>Run</string>
                    <string>Shell</string>
                    <string>Script</string>
                    <string>Unix</string>
                    <string>Command</string>
                    <string>Terminal</string>
                    <string>Bash</string>
                    <string>Zsh</string>
                </array>
                <key>OutputUUID</key>
                <string>B5A0C8C0-8B8B-4B8B-8B8B-8B8B8B8B8B8B</string>
                <key>UUID</key>
                <string>B5A0C8C0-8B8B-4B8B-8B8B-8B8B8B8B8B8B</string>
                <key>UnlocalizedApplications</key>
                <array>
                    <string>Automator</string>
                </array>
                <key>arguments</key>
                <dict>
                    <key>0</key>
                    <dict>
                        <key>name</key>
                        <string>COMMAND_STRING</string>
                        <key>required</key>
                        <string>0</string>
                        <key>type</key>
                        <string>0</string>
                        <key>uuid</key>
                        <string>B5A0C8C0-8B8B-4B8B-8B8B-8B8B8B8B8B8B</string>
                        <key>value</key>
                        <string>cd "$CURRENT_DIR"
source .venv/bin/activate
python -m streamlit run app.py --server.port 8501</string>
                    </dict>
                </dict>
            </dict>
            <key>isViewVisible</key>
            <true/>
            <key>location</key>
            <dict>
                <key>x</key>
                <integer>100</integer>
                <key>y</key>
                <integer>100</integer>
            </dict>
            <key>size</key>
            <dict>
                <key>width</key>
                <integer>200</integer>
                <key>height</key>
                <integer>100</integer>
            </dict>
        </dict>
    </array>
    <key>connectors</key>
    <dict/>
    <key>workflowType</key>
    <string>Application</string>
</dict>
</plist>
EOF

# 現在のディレクトリをワークフローに埋め込む
sed -i '' "s|\$CURRENT_DIR|$CURRENT_DIR|g" /tmp/SwitchSense.workflow

# デスクトップにコピー
cp /tmp/SwitchSense.workflow ~/Desktop/SwitchSense.app

echo "✅ デスクトップに SwitchSense.app を作成しました！"
echo "🖱️ ダブルクリックでアプリを起動できます〜！"
echo "🌐 ブラウザで http://localhost:8501 にアクセスしてください" 