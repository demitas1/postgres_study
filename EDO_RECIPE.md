# 江戸料理レシピ検索デモプログラム使用方法

このドキュメントでは、PostgreSQL学習プロジェクトの江戸料理レシピ検索デモプログラム（`edo_recipe_demo`）の詳細な使用方法を説明します。

## 概要

江戸料理レシピ検索デモプログラムは、CODHの「江戸料理レシピデータセット」を基にしたPostgreSQL学習用のデモンストレーションアプリケーションです。以下の機能を提供します：

- 江戸料理レシピデータベースの自動構築
- 材料による検索機能
- 全文検索機能（レシピ名・説明文）
- 複合検索機能（材料+レシピ名）
- レシピ詳細情報の表示
- データベースの自動クリーンアップ

## データセットについて

### ソースデータ
- **データセット**: 『江戸料理レシピデータセット』（CODH作成）
- **原典**: 『万宝料理秘密箱 卵百珍』（江戸時代の料理書）
- **総レシピ数**: 107件
- **有効レシピ数**: 42件（現代レシピが存在するもの）
- **ライセンス**: クリエイティブ・コモンズ 表示 - 継承 4.0 国際 ライセンス（CC BY-SA）

### データ構造
各レシピには以下の情報が含まれます：
- **基本情報**: ID、名前、URL
- **翻刻テキスト**: 江戸時代の原文
- **現代語訳**: 現代日本語での翻訳
- **現代レシピ**: 現代風にアレンジされたレシピ（説明、材料、手順、コツ）

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

```bash
docker exec python_dev python scripts/run_container.py edo_recipe_demo
```

### ホスト環境での実行

```bash
python scripts/run_host.py edo_recipe_demo
```

## 実行結果の例

### 初回実行時の流れ

```
=== 江戸料理レシピ検索デモ ===

=== データベースセットアップ ===
Connected to database: DatabaseConfig(host=db, port=5432, database=mydatabase, user=postgres)
テーブル作成中...
✓ edo_recipesテーブルを作成しました
✓ recipe_ingredientsテーブルを作成しました
✓ recipe_instructionsテーブルを作成しました
✓ 検索用インデックスを作成しました

江戸料理レシピデータを読み込み中...
✓ 107件のレシピデータを読み込みました
✓ 42件の有効なレシピを検出しました

データベースに挿入中...
✓ 42件のレシピを登録しました

=== 材料検索デモ ===

'卵' を使ったレシピを検索中...
  • 金糸卵 (ID: 1)
    材料: 卵白: 2個, 瓶詰めうに: 小さじ1, （トッピング）瓶詰めうに: 適量...
  • 銀糸卵 (ID: 2)
    材料: 卵白: 2個, 塩: 少々, サラダ油: 適量...

'うに' を使ったレシピを検索中...
  • 金糸卵 (ID: 1)
    材料: 卵白: 2個, 瓶詰めうに: 小さじ1, （トッピング）瓶詰めうに: 適量...

=== 全文検索デモ ===

'卵' でレシピを全文検索中...
  • 金糸卵 (ID: 1, スコア: 0.456)
    説明: 旨味濃厚！ウニの金糸卵
考案：三ツ星たまごソムリエ友加里
金箔を、現代の高級食材でもあるウニで代用しました...

=== 複合検索デモ ===

レシピ名に'卵'、材料に'ウニ'を含むレシピを検索中...
  • 金糸卵 (ID: 1)
    材料: 卵白: 2個, 瓶詰めうに: 小さじ1, （トッピング）瓶詰めうに: 適量...
    説明: 旨味濃厚！ウニの金糸卵
考案：三ツ星たまごソムリエ友加里...

=== レシピ詳細表示例 ===

'有馬玉子' の詳細情報:
URL: https://codh.rois.ac.jp/edo-cooking/tamago-hyakuchin/recipe/062.html.ja
説明: 昆布の旨味たっぷり♪有馬玉子
考案：三ツ星たまごソムリエ友加里
昆布を山椒で代用し、塩昆布を使って簡単にしました...
材料数: 4種類
現代手順数: 6ステップ
コツ: クックパッド江戸ご飯のレシピ

=== データベースクリーンアップ ===
✓ 江戸料理レシピテーブルを削除しました

✓ 江戸料理レシピデモ完了！
```

## データベース設計

### テーブル構造

#### 1. edo_recipes（メインテーブル）
```sql
CREATE TABLE edo_recipes (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    tips TEXT,
    original_text TEXT,
    modern_translation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. recipe_ingredients（材料テーブル）
```sql
CREATE TABLE recipe_ingredients (
    id SERIAL PRIMARY KEY,
    recipe_id SMALLINT REFERENCES edo_recipes(id) ON DELETE CASCADE,
    ingredient TEXT NOT NULL,
    sort_order SMALLINT NOT NULL
);
```

#### 3. recipe_instructions（手順テーブル）
```sql
CREATE TABLE recipe_instructions (
    id SERIAL PRIMARY KEY,
    recipe_id SMALLINT REFERENCES edo_recipes(id) ON DELETE CASCADE,
    instruction_type VARCHAR(20) NOT NULL,  -- 'modern', 'translation', 'original'
    instruction TEXT NOT NULL,
    step_number SMALLINT NOT NULL
);
```

### インデックス

検索パフォーマンスを向上させるため、以下のインデックスが自動作成されます：

```sql
-- 全文検索用インデックス（デフォルト設定を使用）
CREATE INDEX idx_recipes_name ON edo_recipes USING gin (to_tsvector('simple', name));
CREATE INDEX idx_recipes_description ON edo_recipes USING gin (to_tsvector('simple', description));
CREATE INDEX idx_ingredients_text ON recipe_ingredients USING gin (to_tsvector('simple', ingredient));

-- 結合クエリ最適化用インデックス
CREATE INDEX idx_ingredients_recipe_id ON recipe_ingredients(recipe_id);
CREATE INDEX idx_instructions_recipe_id ON recipe_instructions(recipe_id);
CREATE INDEX idx_instructions_type ON recipe_instructions(instruction_type);
```

## 検索機能詳細

### 1. 材料での検索
指定した材料を含むレシピを検索します。

**検索例:**
- "卵" → 卵を使用するレシピを検索
- "うに" → ウニを使用するレシピを検索
- "醤油" → 醤油を使用するレシピを検索

**技術的実装:**
```sql
SELECT DISTINCT r.id, r.name, array_agg(ri.ingredient ORDER BY ri.sort_order) as ingredients
FROM edo_recipes r
JOIN recipe_ingredients ri ON r.id = ri.recipe_id
WHERE ri.ingredient ILIKE '%検索語%'
GROUP BY r.id, r.name
ORDER BY r.name;
```

### 2. 全文検索
レシピ名や説明文に含まれるキーワードで検索します。PostgreSQLの全文検索機能を使用し、関連度スコアも表示されます。

**検索例:**
- "卵" → レシピ名や説明に「卵」が含まれるレシピ
- "濃厚" → 「濃厚」という表現が使われているレシピ
- "現代" → 現代風アレンジについて言及されているレシピ

**技術的実装:**
```sql
SELECT r.id, r.name, r.description,
       ts_rank(
           to_tsvector('simple', r.name || ' ' || COALESCE(r.description, '')),
           plainto_tsquery('simple', %s)
       ) as rank
FROM edo_recipes r
WHERE to_tsvector('simple', r.name || ' ' || COALESCE(r.description, '')) 
      @@ plainto_tsquery('simple', %s)
ORDER BY rank DESC;
```

### 3. 複合検索
レシピ名（または説明文）と材料の両方の条件を満たすレシピを検索します。

**検索例:**
- レシピ名に「卵」、材料に「ウニ」
- レシピ名に「濃厚」、材料に「卵白」
- レシピ名に「現代」、材料に「油」

**技術的実装:**
```sql
SELECT DISTINCT r.id, r.name, r.description, 
       array_agg(ri.ingredient ORDER BY ri.sort_order) as ingredients
FROM edo_recipes r
JOIN recipe_ingredients ri ON r.id = ri.recipe_id
WHERE (r.name ILIKE '%レシピキーワード%' OR r.description ILIKE '%レシピキーワード%')
  AND ri.ingredient ILIKE '%材料キーワード%'
GROUP BY r.id, r.name, r.description;
```

## アーキテクチャ設計

### SOLID原則に基づいた設計

#### 1. Single Responsibility Principle（単一責任原則）
各クラスは単一の責任を持ちます：

- **JsonRecipeLoader**: JSONデータの読み込み・変換のみ
- **EdoRecipeManager**: データベースのCRUD操作のみ
- **RecipeSearchService**: 検索機能のみ

#### 2. Open/Closed Principle（開放閉鎖原則）
新しい検索機能の追加が既存コードの修正なしで可能です。

#### 3. Interface Segregation Principle（インターフェース分離原則）
各クラスは必要な機能のみを公開しています。

#### 4. Dependency Inversion Principle（依存性逆転原則）
データベース設定は抽象化され、環境に依存しません。

### クラス構成

```
src/common/
├── database_config.py        # データベース設定管理
├── json_recipe_loader.py     # JSONデータ読み込み・変換
├── edo_recipe_manager.py     # レシピデータベース管理
└── recipe_search_service.py  # レシピ検索サービス

src/apps/
└── edo_recipe_demo.py        # デモアプリケーション
```

## トラブルシューティング

### よくあるエラーと対処法

#### 1. JSONファイルが見つからない
```
データ読み込みエラー: JSON file not found: /path/to/edo_recipes_all.json
```
**対処法:** 
- ファイルパスを確認: `test_data/edo_ryori/edo_recipes_all.json`
- コンテナ環境の場合、ボリュームマウントが正しいか確認

#### 2. データベース接続エラー
```
Error connecting to PostgreSQL: connection failed
```
**対処法:**
- PostgreSQLコンテナが起動していることを確認: `docker compose ps`
- コンテナを再起動: `docker compose restart db`

#### 3. テキスト検索設定エラー
```
text search configuration "japanese" does not exist
```
**対処法:**
- この問題は修正済みです（`simple`設定を使用するように変更）
- PostgreSQLのデフォルト設定で動作します

#### 4. 全文検索が動作しない
```
Error in fulltext search: function to_tsvector does not exist
```
**対処法:**
- PostgreSQLの全文検索拡張が有効か確認
- pg_trgm拡張がインストールされているか確認

#### 5. テーブル作成エラー
```
Error creating tables: permission denied
```
**対処法:**
- データベースユーザーの権限を確認
- 接続文字列が正しいか確認

## パフォーマンス最適化

### インデックスの活用
- 材料検索: GINインデックスによる高速テキスト検索
- 全文検索: PostgreSQLネイティブの全文検索インデックス
- 結合クエリ: 外部キーインデックスによる高速結合

### クエリ最適化
- LIMIT句による結果件数制限
- 配列集約（array_agg）による効率的なデータ取得
- 適切なORDER BY句による結果ソート

## 学習のポイント

このデモプログラムでは以下のPostgreSQLとPythonの概念を学習できます：

### PostgreSQL
1. **正規化設計**: 1対多の関係を持つテーブル設計
2. **全文検索**: to_tsvector、plainto_tsquery関数の使用
3. **GINインデックス**: テキスト検索用インデックス
4. **配列集約**: array_agg関数による結果集約
5. **外部キー制約**: CASCADE削除の活用

### Python
1. **SOLID原則**: 実践的なオブジェクト指向設計
2. **コンテキストマネージャー**: withステートメントの活用
3. **型ヒント**: 静的型チェックによる品質向上
4. **エラーハンドリング**: 適切な例外処理
5. **データ変換**: JSON→データベース形式への変換

## 拡張アイデア

このデモプログラムを基に、以下のような拡張を試すことができます：

1. **レシピ評価機能**: ユーザー評価・コメント機能の追加
2. **カテゴリ検索**: 料理のカテゴリによる分類・検索
3. **類似レシピ検索**: 機械学習による類似レシピ推薦
4. **画像管理**: レシピ画像の保存・表示機能
5. **Webインターフェース**: FlaskやDjangoを使用したWeb画面
6. **APIサーバー**: RESTful APIの提供
7. **エクスポート機能**: PDF、Excel形式でのレシピエクスポート

## ライセンスと謝辞

### データセット
- **『江戸料理レシピデータセット』**（CODH作成）
- **『日本古典籍データセット』**（国文研所蔵）を翻案
- **ライセンス**: クリエイティブ・コモンズ 表示 - 継承 4.0 国際 ライセンス（CC BY-SA）

### 提供元
- **ROIS-DS人文学オープンデータ共同利用センター（CODH）**
- URL: https://codh.rois.ac.jp/

利用時は適切な出典表示をお願いします：
```
『江戸料理レシピデータセット』（CODH作成） 『日本古典籍データセット』（国文研所蔵）を翻案
```

## 関連ファイル

- `src/common/json_recipe_loader.py`: JSONデータローダー
- `src/common/edo_recipe_manager.py`: レシピデータベース管理
- `src/common/recipe_search_service.py`: 検索サービス
- `src/apps/edo_recipe_demo.py`: メインデモアプリケーション
- `test_data/edo_ryori/edo_recipes_all.json`: 江戸料理レシピデータ
- `scripts/run_container.py`: コンテナ実行ランチャー
- `scripts/run_host.py`: ホスト実行ランチャー