# googleカレンダーエージェント

## 使い方
チャット画面の入力フィールドから
「明日の予定を教えて。」
「予定を登録して。題名：{題名}、詳細：{詳細}、日時：{日時}。」
などを入力してgoogleカレンダーを操作する。

## 開発環境構築
以下の手順でローカル環境でアプリを起動できます。
1. dockerフォルダの.env.sampleファイルをコピーして、.envファイルを作成する。
※このアプリはOpenAIのAPIを使用します。起動にはAPI keyが必要です。
2. 以下のコマンドでアプリを起動する。
```
cd docker
docker-compose up
```