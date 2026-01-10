#!/bin/bash

# 1. メッセージが空なら「Update」をデフォルトにする
MESSAGE=$1
if [ -z "$MESSAGE" ]; then
  MESSAGE="Update Pokedvisor: $(date +'%Y-%m-%d %H:%M:%S')"
fi

echo "🚀 アップロード準備中..."

# 2. 変更を追加（.gitignoreの設定を反映）
git add .

# 3. 確定（コミット）
git commit -m "$MESSAGE"

# 4. 送信（プッシュ）
echo "🛰️ GitHubへ送信中..."
git push origin main

echo "✅ すべての処理が完了しました！"
echo "🌐 公開URLを確認してください。"