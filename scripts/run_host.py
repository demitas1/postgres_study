#!/usr/bin/env python3
"""ホスト環境でのアプリケーション実行ランチャー

Usage:
    python scripts/run_host.py <app_name>
    
Available apps:
    - connection_test: データベース接続テスト
    - task_demo: タスク管理デモ
    - prefecture_demo: 都道府県データデモ
"""

import os
import sys
import subprocess
from pathlib import Path


def setup_environment() -> None:
    """ホスト環境の環境変数を設定"""
    env_vars = {
        'DB_HOST': '127.0.0.1',
        'DB_PORT': '5555', 
        'DB_NAME': 'mydatabase',
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'mysecretpassword',
    }
    
    # PYTHONPATHの設定
    project_root = Path(__file__).parent.parent
    src_path = project_root / 'src'
    env_vars['PYTHONPATH'] = str(src_path)
    
    # 環境変数を設定
    os.environ.update(env_vars)
    print(f"Environment configured for host execution")
    print(f"Database: {env_vars['DB_HOST']}:{env_vars['DB_PORT']}")


def get_python_executable() -> Path:
    """venv内のPythonインタープリターのパスを取得"""
    project_root = Path(__file__).parent.parent
    venv_python = project_root / 'environments/host/venv/bin/python'
    
    if not venv_python.exists():
        print("Error: Virtual environment not found.")
        print("Please run: ./scripts/setup_host.sh")
        sys.exit(1)
    
    return venv_python


def run_app(app_name: str, app_args: list = None) -> None:
    """指定されたアプリケーションを実行"""
    
    # 利用可能なアプリケーション
    available_apps = ['connection_test', 'task_demo', 'prefecture_demo']
    
    if app_name not in available_apps:
        print(f"Error: Unknown app '{app_name}'")
        print(f"Available apps: {', '.join(available_apps)}")
        sys.exit(1)
    
    # 環境設定
    setup_environment()
    
    # アプリケーションパスの取得
    project_root = Path(__file__).parent.parent
    app_path = project_root / 'src/apps' / f'{app_name}.py'
    
    if not app_path.exists():
        print(f"Error: Application file not found: {app_path}")
        sys.exit(1)
    
    # venv内のPythonで実行
    venv_python = get_python_executable()
    
    print(f"Running {app_name}...")
    print("=" * 50)
    
    try:
        cmd = [str(venv_python), str(app_path)]
        if app_args:
            cmd.extend(app_args)
        result = subprocess.run(cmd, check=True, cwd=str(project_root))
    except subprocess.CalledProcessError as e:
        print(f"Application failed with exit code {e.returncode}")
        sys.exit(e.returncode)


def main() -> None:
    """メイン関数"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    app_name = sys.argv[1]
    app_args = sys.argv[2:] if len(sys.argv) > 2 else None
    run_app(app_name, app_args)


if __name__ == "__main__":
    main()