from sqlalchemy import create_engine, text

# データベース接続URL
DATABASE_URL = "postgresql://postgres:mysecretpassword@db:5432/mydatabase"

def test_connection():
    try:
        # エンジンの作成
        engine = create_engine(DATABASE_URL)

        # 接続テスト＆サンプルクエリの実行
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users"))
            users = result.fetchall()

            print("Connected to PostgreSQL successfully!")
            print("\nUsers in database:")
            for user in users:
                print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == "__main__":
    test_connection()
