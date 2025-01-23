import psycopg2
from psycopg2.extensions import connection

def test_connection():
    try:
        # データベース接続
        conn: connection = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="mysecretpassword",
            host="db",
            port="5432"
        )

        # カーソルの作成
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            print("Connected to PostgreSQL successfully!")
            print("\nUsers in database:")
            for user in users:
                print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_connection()
