# 都道府県データデモプログラム使用方法

このドキュメントでは、PostgreSQL学習プロジェクトの都道府県データデモプログラム（`prefecture_demo`）の詳細な使用方法を説明します。

## 概要

都道府県データデモプログラムは、PostgreSQLの基本的な操作を学習するためのデモンストレーションアプリケーションです。以下の機能を提供します：

- 都道府県テーブルの作成・削除
- CSVファイルからの都道府県データ読み込み
- データベースへの一括データ挿入
- 面積・人口ランキングの表示
- データ重複チェック機能

## 前提条件

### コンテナ環境で実行する場合
```bash
# Docker Composeでコンテナを起動
docker compose up -d

# コンテナが正常に起動していることを確認
docker compose ps
```

### ホスト環境で実行する場合
```bash
# ホスト環境のセットアップ（初回のみ）
./scripts/setup_host.sh

# PostgreSQLコンテナが起動していることを確認
docker compose up -d db
```

## 基本的な使用方法

### コンテナ環境での実行

#### 通常実行
```bash
docker exec python_dev python scripts/run_container.py prefecture_demo
```

#### クリーンスタート（既存データを削除してから実行）
```bash
docker exec python_dev python scripts/run_container.py prefecture_demo --clean
```

### ホスト環境での実行

#### 通常実行
```bash
python scripts/run_host.py prefecture_demo
```

#### クリーンスタート（既存データを削除してから実行）
```bash
python scripts/run_host.py prefecture_demo --clean
```

## 実行結果の例

### 初回実行時
```
=== 都道府県データデモ ===

Connected to database: DatabaseConfig(host=db, port=5432, database=mydatabase, user=postgres)
テーブル作成中...
✓ prefecturesテーブルを作成しました
✓ インデックスを作成しました

CSVデータ読み込み中...
✓ 47件の都道府県データを読み込みました
✓ データバリデーション完了

データ挿入中...
✓ 47件のデータを挿入しました

=== 面積TOP3 ===
1位: 北海道 (83,424.44 km²)
2位: 岩手県 (15,275.01 km²)
3位: 福島県 (13,784.14 km²)

=== 人口TOP3 ===
1位: 東京都 (14,047,594 人)
2位: 神奈川県 (9,237,337 人)
3位: 大阪府 (8,837,685 人)

✓ デモ完了！
```

### 2回目実行時（データ重複チェック）
```
=== 都道府県データデモ ===

Connected to database: DatabaseConfig(host=db, port=5432, database=mydatabase, user=postgres)
テーブル作成中...
✓ prefecturesテーブルを作成しました
✓ インデックスを作成しました

既に47件のデータが存在します。
データ挿入をスキップします。

=== 面積TOP3 ===
1位: 北海道 (83,424.44 km²)
2位: 岩手県 (15,275.01 km²)
3位: 福島県 (13,784.14 km²)

=== 人口TOP3 ===
1位: 東京都 (14,047,594 人)
2位: 神奈川県 (9,237,337 人)
3位: 大阪府 (8,837,685 人)

✓ デモ完了！
```

### クリーンスタート実行時
```
=== 都道府県データデモ ===

Connected to database: DatabaseConfig(host=db, port=5432, database=mydatabase, user=postgres)
クリーンスタートモード: 既存テーブルを削除中...
✓ 既存テーブルを削除しました

テーブル作成中...
✓ prefecturesテーブルを作成しました
✓ インデックスを作成しました

CSVデータ読み込み中...
✓ 47件の都道府県データを読み込みました
✓ データバリデーション完了

データ挿入中...
✓ 47件のデータを挿入しました

=== 面積TOP3 ===
1位: 北海道 (83,424.44 km²)
2位: 岩手県 (15,275.01 km²)
3位: 福島県 (13,784.14 km²)

=== 人口TOP3 ===
1位: 東京都 (14,047,594 人)
2位: 神奈川県 (9,237,337 人)
3位: 大阪府 (8,837,685 人)

✓ デモ完了！
```

## データ構造

### CSVファイル
都道府県データは `test_data/prefectures/prefectures.csv` に格納されています。

**CSVファイルの列:**
- `id`: 都道府県ID（1-47）
- `name`: 都道府県名
- `furigana`: ふりがな
- `capital`: 県庁所在地
- `largest_city`: 最大都市
- `region`: 地方区分
- `population`: 人口
- `area`: 面積（km²）
- `ppa`: 人口密度（人/km²）
- `towns`: 市町村数
- `seats1`: 衆議院議席数
- `seats2`: 参議院議席数

### データベーステーブル構造

#### prefectures テーブル
```sql
CREATE TABLE prefectures (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    name_kana VARCHAR(20) NOT NULL,
    capital VARCHAR(20) NOT NULL,
    largest_city VARCHAR(20) NOT NULL,
    region VARCHAR(10) NOT NULL,
    population INTEGER NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    population_density DECIMAL(8,1) NOT NULL,
    municipalities_count SMALLINT NOT NULL,
    lower_house_seats SMALLINT NOT NULL,
    upper_house_seats SMALLINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 作成されるインデックス
- `idx_prefectures_population`: 人口による降順インデックス
- `idx_prefectures_area`: 面積による降順インデックス
- `idx_prefectures_density`: 人口密度による降順インデックス
- `idx_prefectures_region`: 地方区分によるインデックス

## コマンドラインオプション

### --clean
既存のprefecturesテーブルを削除してからプログラムを実行します。

**使用場面:**
- テーブル構造を変更した後の再初期化
- データの完全リセット
- テスト目的での初期状態復元

## トラブルシューティング

### よくあるエラーと対処法

#### 1. CSVファイルが見つからない
```
CSVファイルの読み込みに失敗: CSV file not found: /path/to/prefectures.csv
```
**対処法:** 
- コンテナ環境: `docker compose down && docker compose up -d` でコンテナを再起動
- ホスト環境: `test_data/prefectures/prefectures.csv` ファイルの存在確認

#### 2. データベース接続エラー
```
Error connecting to PostgreSQL: connection failed
```
**対処法:**
- PostgreSQLコンテナが起動していることを確認: `docker compose ps`
- コンテナを再起動: `docker compose restart db`

#### 3. 権限エラー
```
Permission denied
```
**対処法:**
- 環境変数の確認: `USER_ID` と `GROUP_ID` が正しく設定されているか確認
- ファイルの権限確認: `ls -la test_data/prefectures/`

#### 4. テーブル作成エラー
```
Error creating tables: relation "prefectures" already exists
```
**対処法:**
- `--clean` オプションを使用してテーブルを削除してから実行
- または手動でテーブルを削除: `psql -h localhost -p 5555 -U postgres -d mydatabase -c "DROP TABLE IF EXISTS prefectures CASCADE;"`

## 学習のポイント

このデモプログラムでは以下のPostgreSQLの概念を学習できます：

### 1. DDL（Data Definition Language）
- `CREATE TABLE`: テーブル作成
- `CREATE INDEX`: インデックス作成
- `DROP TABLE`: テーブル削除

### 2. DML（Data Manipulation Language）
- `INSERT`: データ挿入（バッチ挿入）
- `SELECT`: データ取得
- `ORDER BY`: ソート
- `LIMIT`: 件数制限

### 3. データ型
- `SMALLINT`: 小さな整数
- `INTEGER`: 整数
- `DECIMAL`: 固定精度小数
- `VARCHAR`: 可変長文字列
- `TIMESTAMP`: タイムスタンプ

### 4. インデックス
- パフォーマンス向上のためのインデックス設計
- 降順インデックスの活用

### 5. Python-PostgreSQL連携
- psycopg2を使用したデータベース接続
- トランザクション処理
- バッチ挿入処理
- エラーハンドリング

## 拡張アイデア

このデモプログラムを基に、以下のような拡張を試すことができます：

1. **地方別集計機能**: 地方ごとの人口・面積合計を表示
2. **人口密度ランキング**: 人口密度のTOP/BOTTOMを表示
3. **統計計算**: 平均値、中央値、標準偏差の計算
4. **グラフ化**: matplotlib を使用した可視化
5. **Webインターフェース**: Flask を使用したWeb画面作成

## 関連ファイル

- `src/common/prefecture_manager.py`: 都道府県データ管理クラス
- `src/common/csv_loader.py`: CSVデータ読み込みクラス
- `src/apps/prefecture_demo.py`: メインアプリケーション
- `test_data/prefectures/prefectures.csv`: 都道府県データファイル
- `scripts/run_container.py`: コンテナ実行ランチャー
- `scripts/run_host.py`: ホスト実行ランチャー