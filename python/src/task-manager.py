import psycopg2
from psycopg2 import Error
from datetime import datetime

class TaskManager:
    def __init__(self, dbname="taskdb", user="postgres", password="your_password", host="localhost", port="5432"):
        try:
            self.conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            self._create_table()
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            raise

    def _create_table(self):
        """テーブルが存在しない場合、新規作成します"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        try:
            self.cur.execute(create_table_query)
            self.conn.commit()
        except Error as e:
            print(f"Error creating table: {e}")
            self.conn.rollback()

    def create_task(self, title, description=""):
        """新しいタスクを作成します"""
        insert_query = """
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING id;
        """
        try:
            self.cur.execute(insert_query, (title, description))
            task_id = self.cur.fetchone()[0]
            self.conn.commit()
            print(f"Task created successfully with ID: {task_id}")
            return task_id
        except Error as e:
            print(f"Error creating task: {e}")
            self.conn.rollback()
            return None

    def read_task(self, task_id=None):
        """タスクを読み取ります。IDが指定されていない場合は全タスクを取得します"""
        try:
            if task_id:
                self.cur.execute("SELECT * FROM tasks WHERE id = %s;", (task_id,))
                return self.cur.fetchone()
            else:
                self.cur.execute("SELECT * FROM tasks ORDER BY created_at DESC;")
                return self.cur.fetchall()
        except Error as e:
            print(f"Error reading task(s): {e}")
            return None

    def update_task(self, task_id, title=None, description=None, status=None):
        """タスクを更新します"""
        update_fields = []
        values = []

        if title:
            update_fields.append("title = %s")
            values.append(title)
        if description:
            update_fields.append("description = %s")
            values.append(description)
        if status:
            update_fields.append("status = %s")
            values.append(status)

        if not update_fields:
            return False

        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(task_id)

        update_query = f"""
        UPDATE tasks
        SET {", ".join(update_fields)}
        WHERE id = %s
        """

        try:
            self.cur.execute(update_query, values)
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error updating task: {e}")
            self.conn.rollback()
            return False

    def delete_task(self, task_id):
        """タスクを削除します"""
        try:
            self.cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
            self.conn.commit()
            return True
        except Error as e:
            print(f"Error deleting task: {e}")
            self.conn.rollback()
            return False

    def __del__(self):
        """デストラクタ: データベース接続を適切にクローズします"""
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

# 使用例
if __name__ == "__main__":
    # TaskManagerのインスタンスを作成
    task_manager = TaskManager(
        dbname="mydatabase",
        user="postgres",
        password="mysecretpassword",
        host="db",
        port="5432",
    )

    # タスクの作成
    task_id = task_manager.create_task(
        "PostgreSQLの学習",
        "基本的なCRUD操作を実装する"
    )

    # 全タスクの読み取り
    all_tasks = task_manager.read_task()
    print("\nAll tasks:")
    for task in all_tasks:
        print(task)

    # 特定のタスクの更新
    task_manager.update_task(
        task_id,
        status="in_progress"
    )

    # 更新されたタスクの確認
    updated_task = task_manager.read_task(task_id)
    print("\nUpdated task:")
    print(updated_task)

    # タスクの削除
    task_manager.delete_task(task_id)
