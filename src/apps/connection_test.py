"""PostgreSQL接続テストアプリケーション

データベース接続をテストし、usersテーブルのデータを表示します。
"""

import psycopg2
from psycopg2.extensions import connection

from common.database_config import DatabaseConfig


def test_connection() -> None:
    """データベース接続をテストし、usersテーブルの内容を表示"""
    
    # 環境に応じた設定を自動取得
    db_config = DatabaseConfig.from_environment()
    
    conn: connection = None
    try:
        # データベース接続
        print(f"Connecting to database: {db_config}")
        conn = psycopg2.connect(**db_config.to_connection_params())
        
        # カーソルの作成とクエリ実行
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            
            print("Connected to PostgreSQL successfully!")
            print("\nUsers in database:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created: {user[3]}")
    
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return
    
    finally:
        if conn:
            conn.close()
            print("\nConnection closed.")


if __name__ == "__main__":
    test_connection()