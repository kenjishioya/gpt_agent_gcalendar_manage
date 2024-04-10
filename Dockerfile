# ベースイメージとしてPython 3.9を使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonパッケージをインストール
# ここではstreamlitのみをインストールしていますが、
# 必要に応じて他のパッケージを追加してください
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# StreamlitのWebインターフェースを公開するためのポートを設定
EXPOSE 8501