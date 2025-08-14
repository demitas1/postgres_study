# PostgreSQL study

PostgreSQLの基本操作を学習するためのプロジェクトです。DockerコンテナとPythonを使用して、データベース操作の実践的な学習ができます。

## 🌟 特徴

- **統合環境**: 同一コードをコンテナとホストの両方で実行可能
- **自動環境検出**: 実行環境を自動判定し、適切な接続設定を使用
- **SOLID原則**: コードはSOLID原則に基づいて設計
- **簡単セットアップ**: 一発で開発環境を構築

## 🚀 クイックスタート

### 1. 環境構築

```bash
# PostgreSQLコンテナを起動
./start.sh

# 環境が起動するまで少し待つ（初回は数分かかります）
```

### 2. アプリケーション実行

**🐳 コンテナ環境での実行:**
```bash
# 接続テスト
./test.sh

# タスク管理デモ
docker exec python_dev python scripts/run_container.py task_demo
```

**💻 ホスト環境での実行（新機能！）:**
```bash
# ホスト環境のセットアップ（初回のみ）
./scripts/setup_host.sh

# スクリプト経由での実行（推奨：自動でvenv使用）
python scripts/run_host.py connection_test
python scripts/run_host.py task_demo

# 直接実行したい場合（venvのアクティベーションが必要）
source ./environments/host/venv/bin/activate
python src/apps/connection_test.py
python src/apps/task_demo.py
deactivate
```

## 📋 利用可能なアプリケーション

| アプリケーション | 説明 |
|------------------|------|
| `connection_test` | データベース接続テスト、usersテーブルの内容を表示 |
| `task_demo` | TaskManagerを使用したCRUD操作のデモ |

## 🛠️ 管理コマンド

### 環境管理
```bash
# 環境を起動
./start.sh

# 環境を停止（データ保持）
./stop.sh

# 環境を停止＋データ削除
docker compose down -v --remove-orphans

# 完全クリーンアップ（pgdataも削除）
docker compose down -v --remove-orphans && sudo rm -rf pgdata

# ホスト用venvを再構築
rm -rf environments/host/venv && ./scripts/setup_host.sh
```

### データベース直接アクセス
```bash
# psql経由でデータベースに接続
psql -h localhost -p 5555 -U postgres -d mydatabase
# パスワード: mysecretpassword

# pgAdmin4（Web UI）でアクセス
# http://localhost:8080
# Email: admin@example.com
# Password: admin123
```

## 📊 データベース構成

### usersテーブル（初期データ）
```sql
mydatabase=# \d users
                                       Table "public.users"
  Column   |           Type           | Collation | Nullable |              Default              
-----------+--------------------------+-----------+----------+-----------------------------------
 id         | integer                  |           | not null | nextval('users_id_seq'::regclass)
 username   | character varying(100)   |           | not null | 
 email      | character varying(255)   |           | not null | 
 created_at | timestamp with time zone |           |          | CURRENT_TIMESTAMP

mydatabase=# select * from users;
 id | username  |      email       |          created_at           
----+-----------+------------------+-------------------------------
  1 | test_user | test@example.com | 2025-01-22 08:22:53.630195+00
  2 | demo_user | demo@example.com | 2025-01-22 08:22:53.630195+00
```

### tasksテーブル（動的作成）
`task_demo`アプリケーションが自動で作成するタスク管理用テーブルです。

## 🏗️ プロジェクト構造

```
postgres_study/
├── src/                    # 統合されたソースコード
│   ├── common/             # 共通ライブラリ
│   │   ├── database_config.py    # DB設定管理（環境自動検出）
│   │   └── task_manager.py       # CRUD操作クラス
│   └── apps/               # アプリケーション
│       ├── connection_test.py    # 接続テスト
│       └── task_demo.py          # タスク管理デモ
├── scripts/                # 実行・管理スクリプト
│   ├── setup_host.sh       # ホスト環境セットアップ
│   ├── run_host.py         # ホスト実行ランチャー
│   └── run_container.py    # コンテナ実行ランチャー
├── environments/           # 環境固有設定
│   ├── container/          # Docker設定
│   └── host/              # ホスト用venv
└── init/                   # DB初期化スクリプト
```

## 🔧 技術仕様

- **Python**: 3.11+
- **PostgreSQL**: 15
- **主要ライブラリ**: psycopg2-binary, SQLAlchemy
- **コンテナ**: Docker + Docker Compose
- **Web管理**: pgAdmin4

## 📚 学習内容

- PostgreSQLの基本的なCRUD操作
- Pythonでのデータベース接続（psycopg2）
- Dockerを使用した開発環境構築
- 環境に依存しないコード設計
- SOLID原則に基づいたクラス設計