#!/usr/bin/env python3
"""コンテナ環境でのアプリケーション実行ランチャー

Usage:
    python scripts/run_container.py <app_name>
    
Available apps:
    - connection_test: データベース接続テスト  
    - task_demo: タスク管理デモ
"""

import os
import sys
import subprocess
from pathlib import Path


def setup_environment() -> None:
    """コンテナ環境の環境変数を設定"""
    env_vars = {
        'DB_HOST': 'db',
        'DB_PORT': '5432',
        'DB_NAME': 'mydatabase', 
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'mysecretpassword',
    }
    
    # PYTHONPATHの設定
    src_path = '/app/src'  # コンテナ内のパス
    env_vars['PYTHONPATH'] = src_path
    
    # 環境変数を設定
    os.environ.update(env_vars)
    print(f"Environment configured for container execution")
    print(f"Database: {env_vars['DB_HOST']}:{env_vars['DB_PORT']}")


def run_app(app_name: str) -> None:
    """指定されたアプリケーションを実行"""
    
    # 利用可能なアプリケーション
    available_apps = ['connection_test', 'task_demo']
    
    if app_name not in available_apps:
        print(f"Error: Unknown app '{app_name}'")
        print(f"Available apps: {', '.join(available_apps)}")
        sys.exit(1)
    
    # 環境設定
    setup_environment()
    
    # アプリケーションパスの取得（コンテナ内パス）
    app_path = f'/app/src/apps/{app_name}.py'
    
    if not Path(app_path).exists():
        print(f"Error: Application file not found: {app_path}")
        sys.exit(1)
    
    print(f"Running {app_name}...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Application failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def main() -> None:
    """メイン関数"""
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    
    app_name = sys.argv[1]
    run_app(app_name)


if __name__ == "__main__":
    main()