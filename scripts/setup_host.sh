#!/bin/bash
set -e

echo "Setting up host environment for PostgreSQL study..."

# プロジェクトルートディレクトリに移動
cd "$(dirname "$0")/.."

# ホスト用venv作成・更新
VENV_DIR="environments/host/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi

# 依存関係インストール
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"

# requirements.txtが存在することを確認
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Creating from python/requirements.txt..."
    cp python/requirements.txt requirements.txt
fi

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Host environment setup completed!"
echo ""
echo "To run applications:"
echo "  python scripts/run_host.py connection_test"
echo "  python scripts/run_host.py task_demo"
echo ""